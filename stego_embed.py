import base64
from PIL import Image

def read_payload_from_file(filepath: str) -> str:
    """Reads the payload from a file and returns it as a string."""
    with open(filepath, "r") as f:
        return f.read()


def string_to_bytes(data: str) -> bytes:
    """Turns string into actual bytes (not bits)."""
    return data.encode('utf-8')

def to_bitstring(data: str | bytes) -> str:
    """Converts string or bytes to a string of bits."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ''.join(format(b, '08b') for b in data)

def encode_payload(payload: str | bytes) -> str:
    """Encodes payload using Base64. Accepts str or bytes, returns Base64 string."""
    if isinstance(payload, str):
        payload = payload.encode('utf-8')
    return base64.b64encode(payload).decode('utf-8')

def embed_payload_in_lsb(image_path: str, bitstring: str, output_path: str) -> None:
    """Versteckt Payload in den LSBs eines PNG-Bildes."""
    if not image_path or not bitstring or not output_path:
        raise ValueError("Image path, payload, and output path cannot be empty.")

    if not bitstring:
        raise ValueError("Payload cannot be empty.")

    if not image_path.lower().endswith('.png'):
        raise ValueError("Image must be a PNG file.")

    if not output_path.lower().endswith('.png'):
        raise ValueError("Output file must be a PNG file.")


    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")

    pixels = img.load()
    width, height = img.size

    idx = 0
    for y in range(height):
        for x in range(width):
            if idx >= len(bitstring):
                break
            r, g, b = pixels[x, y]
            r = (r & 0xFE) | int(bitstring[idx])  # LSB setzen
            pixels[x, y] = (r, g, b)
            idx += 1
        if idx >= len(bitstring):
            break

    img.save(output_path)
    print("Text embedded.")

def embed_payload_in_exif(image_path: str, payload: bytes, output_path: str) -> None:
    """(Optional) Versteckt Payload in EXIF-Feldern des Bildes."""


def add_custom_header(payload: bytes) -> bytes:
    """Fügt Magic Bytes und Payload-Länge hinzu (für späteres Decoding)."""
