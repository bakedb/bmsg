# https://stuvel.eu/python-rsa-doc/usage.html for docs
# Parts of this file are vibe coded
import rsa

def generate_keys(length):
    public_key, private_key = rsa.newkeys(length)
    return public_key, private_key

def return_keys(key):
    if key is None:
        raise ValueError("The key cannot be None.")
        
    key = str(key)
    parts = [int(part.strip()) for part in key.split(",") if part.strip()]
    
    if len(parts) == 2:
        # Public key: modulus, exponent
        return rsa.PublicKey(parts[0], parts[1])
    elif len(parts) == 4:
        # Private key: modulus, exponent, d, q
        return rsa.PrivateKey(parts[0], parts[1], parts[2], parts[3], parts[3])
    elif len(parts) == 5:
        # Private key: modulus, exponent, d, p, q
        return rsa.PrivateKey(parts[0], parts[1], parts[2], parts[3], parts[4])
    else:
        raise ValueError(f"Invalid key format. Expected 2 values for public key, 4 or 5 for private key, got {len(parts)}.")

def encrypt(message, public_key):
    message = str(message)
    encoded = message.encode('utf8')
    enc_message = rsa.encrypt(encoded, public_key)
    return enc_message

def decrypt(message, private_key):
    # Convert string back to bytes if needed
    if isinstance(message, str):
        if message.startswith("b'") and message.endswith("'"):
            import ast
            message = ast.literal_eval(message)
        else:
            message = message.encode('latin1')  # Use latin1 to preserve byte values
    dec_message = rsa.decrypt(message, private_key)
    return dec_message.decode('utf-8')