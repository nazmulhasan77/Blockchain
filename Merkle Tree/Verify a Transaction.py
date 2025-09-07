import hashlib

# Hashing function
def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Build Merkle Tree and return all layers
def build_merkle_tree(transactions):
    tree = [[hash_data(tx) for tx in transactions]]  # bottom layer
    while len(tree[-1]) > 1:
        layer = tree[-1]
        if len(layer) % 2 != 0:
            layer.append(layer[-1])  # duplicate last if odd
        new_layer = []
        for i in range(0, len(layer), 2):
            new_layer.append(hash_data(layer[i] + layer[i+1]))
        tree.append(new_layer)
    return tree

# Print Merkle Tree nicely
def print_merkle_tree(tree):
    print("\nMerkle Tree Layers:")
    for i, layer in enumerate(tree):
        print(f"Layer {i} ({len(layer)} nodes):")
        for j, node in enumerate(layer):
            print(f"  Node {j}: {node}")
        print()

# Generate Merkle Proof for a transaction
def get_proof(transactions, tx_index):
    tree = build_merkle_tree(transactions)
    proof = []
    index = tx_index
    path = []  # for showing verification path
    for layer in tree[:-1]:  # skip root
        sibling_index = index + 1 if index % 2 == 0 else index - 1
        proof.append(layer[sibling_index])
        path.append((layer[index], layer[sibling_index]))  # (current, sibling)
        index = index // 2
    return proof, path

# Verify a transaction using proof
def verify_transaction(tx, proof, merkle_root):
    current_hash = hash_data(tx)
    print("\nVerification Path:")
    for i, sibling_hash in enumerate(proof):
        print(f"Step {i+1}: hash({current_hash} + {sibling_hash})")
        current_hash = hash_data(current_hash + sibling_hash)
    print("Computed Root:", current_hash)
    print("Merkle Root:   ", merkle_root)
    return current_hash == merkle_root

# Example transactions
transactions = ["tx1", "tx2", "tx3", "tx4"]

# Build tree and get Merkle Root
tree = build_merkle_tree(transactions)
merkle_root = tree[-1][0]

# Print tree
print_merkle_tree(tree)
print("Merkle Root:", merkle_root)

# Transaction to verify
tx_index = 0  # "tx1"
proof, path = get_proof(transactions, tx_index)

# Print Merkle Proof
print("\nMerkle Proof for transaction 'tx1':")
for i, p in enumerate(proof):
    print(f"Sibling at step {i+1}: {p}")

# Print path of transaction to root
print("\nTransaction Path to Root:")
for i, (current, sibling) in enumerate(path):
    print(f"Step {i+1}: Current={current}, Sibling={sibling}")

# Verify transaction
is_valid = verify_transaction("txdf1", proof, merkle_root)
print("\nTransaction 'txdf1' Valid:", is_valid)
