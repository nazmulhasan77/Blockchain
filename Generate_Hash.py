import hashlib

data = "Blockchain"

hash_object = hashlib.sha256(data.encode())
hash_hex=hash_object.hexdigest()

print("Input : ", data)
print("Hash Object: ", hash_object)
print("SHA 256 Hash: ", hash_hex)

# Output:
# Hash Object:  <sha256 _hashlib.HASH object @ 0x0000024A55A899F0>
# SHA 256 Hash:  625da44e4eaf58d61cf048d168aa6f5e492dea166d8bb54ec06c30de07db57e1