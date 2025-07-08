from stego_embed import *

# Real payload
payload = "Hello"

# Turn to bytes
payload_bytes = string_to_bytes(payload)

#  Base64 encode the bytes
encoded = encode_payload(payload_bytes)

# Convert Base64 string to bytes
encoded_bytes = string_to_bytes(encoded)

#  Bitstring for embedding
bitstring = to_bitstring(encoded_bytes)

#  Embed
embed_payload_in_lsb("rickroll.png", bitstring, "stego_output.png")

# Logs
print(encoded)
print(f"Encoded base64 payload: {encoded}")
print(f"Byte length: {len(encoded_bytes)}")
