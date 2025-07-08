from PIL import Image

payload = "Hello"  # Payload
binary = ''.join([format(ord(c), '08b') for c in payload])  # payload → Binary

img = Image.open("rickroll.png")
if img.mode != "RGB":
    img = img.convert("RGB")

pixels = img.load()
width, height = img.size

idx = 0
for y in range(height):
    for x in range(width):
        if idx >= len(binary):
            break
        r, g, b = pixels[x, y]
        r = (r & 0xFE) | int(binary[idx])  # LSB setzen
        pixels[x, y] = (r, g, b)
        idx += 1
    if idx >= len(binary):
        break

img.save("stego_output.png")
print("Text embedded.")
