from PIL import Image

img = Image.open("stego_output.png")
pixels = img.load()
width, height = img.size

bits = ''
for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        bits += str(r & 1)
        if len(bits) % 8 == 0 and len(bits) >= 40:  # 5 Zeichen * 8 Bits
            break
    if len(bits) >= 40:
        break

text = ''.join([chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)])
print("Extracted text:", text)
