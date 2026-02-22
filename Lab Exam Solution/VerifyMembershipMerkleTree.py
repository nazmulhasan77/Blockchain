import hashlib

def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()


def build_merkle_tree(transactions):
    tree = [[hash_data(tx) for tx in transactions]]
    while len(tree[-1]) > 1:
        layer = tree[-1]
        if len(layer) % 2 != 0:
            layer.append(layer[-1])
        new_layer = []
        for i in range(0, len(layer), 2):
            new_layer.append(hash_data(layer[i] + layer[i+1]))
        tree.append(new_layer)
    return tree

def print_merkle_tree(tree):
    print("\nMerkle Tree Layers:")
    for i, layer in enumerate(tree):
        print(f"Layer {i} ({len(layer)} nodes):")
        for j, node in enumerate(layer):
            print(f"  Node {j}: {node}")
        print()

def get_proof(transactions, tx_index):
    tree = build_merkle_tree(transactions)
    proof = []
    index = tx_index
    path = []
    for layer in tree[:-1]:
        sibling_index = index + 1 if index % 2 == 0 else index - 1
        if sibling_index < len(layer):
            proof.append(layer[sibling_index])
            path.append((layer[index], layer[sibling_index]))
        index //= 2
    return proof, path

def verify_transaction(tx, proof, merkle_root):
    current_hash = hash_data(tx)
    print("\nVerification Path:")
    for i, sibling_hash in enumerate(proof):
        if i % 2 == 0:  
            current_hash = hash_data(current_hash + sibling_hash)
        else:           
            current_hash = hash_data(sibling_hash + current_hash)
        print(f"Step {i+1}: {current_hash}")
    print("Computed Root:", current_hash)
    print("Merkle Root:  ", merkle_root)
    return current_hash == merkle_root

transactions = []
n = int(input("Enter number of transactions: "))
for i in range(n):
    tx = input(f"Enter transaction {i+1}: ")
    transactions.append(tx)

tree = build_merkle_tree(transactions)
merkle_root = tree[-1][0]


print_merkle_tree(tree)
print("Merkle Root:", merkle_root)


tx_to_verify = input("\nEnter a transaction to verify: ")

if tx_to_verify in transactions:
    tx_index = transactions.index(tx_to_verify)
    proof, path = get_proof(transactions, tx_index)

    print("\nMerkle Proof for transaction:", tx_to_verify)
    for i, p in enumerate(proof):
        print(f"Sibling at step {i+1}: {p}")

    is_valid = verify_transaction(tx_to_verify, proof, merkle_root)
    print("\nTransaction Valid")
else:
    print("\nTransaction not found in list")
