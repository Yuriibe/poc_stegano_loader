def read_payload_from_file(filepath: str) -> bytes:
    """Liest eine Binärdatei ein (z.. Shellcode-Datei)."""
    with open(filepath, "rb") as f:
        return f.read()

def string_to_bytes(data: str) -> bytes:
    """Takes ."""
    return data.encode()  # oder z.B. base64.b64decode(data)

def encode_payload(payload: bytes) -> str:
    """Optional: Base64-kodieren oder XOR-verschlüsseln."""

def embed_payload_in_lsb(image_path: str, payload: bytes, output_path: str) -> None:
    """Versteckt Payload in den LSBs eines PNG-Bildes."""

def embed_payload_in_exif(image_path: str, payload: bytes, output_path: str) -> None:
    """(Optional) Versteckt Payload in EXIF-Feldern des Bildes."""

def add_custom_header(payload: bytes) -> bytes:
    """Fügt Magic Bytes und Payload-Länge hinzu (für späteres Decoding)."""
