from PIL import Image
import base64

def extract_payload_from_lsb(image_path: str, byte_length: int) -> bytes:
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    bits = ''
    needed_bits = byte_length * 8

    for y in range(height):
        for x in range(width):
            if len(bits) >= needed_bits:
                break
            r, g, b = pixels[x, y]
            bits += str(r & 1)
        if len(bits) >= needed_bits:
            break

    # Convert bits to bytes
    payload_bytes = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return payload_bytes

# === USAGE ===
extracted_bytes = extract_payload_from_lsb("stego_output.png", byte_length=8)
print("Extracted raw:", extracted_bytes)
print("As string:", extracted_bytes.decode(errors="replace"))

decoded = base64.b64decode(extracted_bytes)
print("✅ Extracted text:", decoded.decode())
