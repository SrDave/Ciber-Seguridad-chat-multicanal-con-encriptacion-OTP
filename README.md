# CIFRADO OTP
### El cifrador One-Time Pad (OTP) es un cifrador incondicionalmente seguro y que tiene una implementación muy sencilla. De hecho, se basa en el uso de XOR y, para ello, puede hacer uso de la siguiente función escrita en Python:
""" def xor_bytes(key_stream, message):
length = min(len(key_stream), len(message))
return bytes([key_stream[i] ^ message[i] for i in range(length)]) """
