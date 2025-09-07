# “Encrypt” with private key , “Decrypt” with public key

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# ------------------ Generate Keys ------------------
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# ------------------ Message ------------------
message = b"This is a secret message"

# ------------------ 'Encrypt' with Private Key (Sign) ------------------
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print("Signature (hex):", signature.hex())

# ------------------ 'Decrypt' with Public Key (Verify) ------------------
try:
    public_key.verify(
        signature,   # "decrypted" here means verification
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("✅ Signature is valid!")
except Exception:
    print("❌ Signature is invalid!")
