import hashlib
def mine_block(data,difficulty):
    nonce=0
    prefix="0"*difficulty

    while True:
        text=data + str(nonce)
        hash_val=hashlib.sha256(text.encode()).hexdigest()

        if hash_val.startswith(prefix):
            return nonce,hash_val
        nonce=nonce+1

data = "block Data"
difficulty = 4

nonce, hash_val = mine_block(data,difficulty)

print(data)
print(hash_val)
print(nonce)