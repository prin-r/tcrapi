from app.merkle.smt import Smt, sha3
from app.db import db, Leaf, Node
from datetime import datetime


def create_tree(keys, values):
    if len(keys) != len(values):
        raise ValueError("Key's length is not equal to Value")
    smt1 = Smt()
    try:
        for i in range(0, len(keys), 1):
            smt1.insert(keys[i], values[i])

        for i in range(0, len(keys), 1):
            if (
                db.session.query(Leaf)
                .filter_by(root_hash=hex(smt1.root), key=hex(keys[i]))
                .first()
                is None
            ):
                leaf = Leaf(
                    root_hash=hex(smt1.root),
                    key=hex(keys[i]),
                    value=values[i],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                db.session.add(leaf)

        for key, (left, right) in (smt1.hashes).items():
            if db.session.query(Node).filter_by(hash=hex(key)).first() is None:
                node = Node(
                    hash=hex(key),
                    left_hash=hex(left),
                    right_hash=hex(right),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                db.session.add(node)

        db.session.commit()
    except Exception as e:
        print(str(e))
        db.session.rollback()
    return hex(smt1.root)


def get_proof(key, root):
    if isinstance(key, str):
        key = int(key, 16)
    if isinstance(root, str):
        root = int(root, 16)

    mask = 0
    proof = []

    current_root = root
    for level in range(159, -1, -1):
        row = db.session.query(Node).filter_by(hash=hex(current_root)).first()
        left = int(row.left_hash, 16)
        right = int(row.right_hash, 16)

        if key & (1 << level) == 0:
            if right == 0:
                mask |= 1 << level
            else:
                proof.append(right)
            current_root = left
        else:
            if left == 0:
                mask |= 1 << level
            else:
                proof.append(left)
            current_root = right

    proof = [
        "0x" + each.to_bytes(32, "big").hex()
        for each in [mask] + list(reversed(proof))
    ]
    return proof


def verify_proof(key, val, proof, root):
    if isinstance(key, str):
        key = int(key, 16)

    current_leaf = val
    proof_index = 1

    mask = proof[0]
    if isinstance(mask, str):
        mask = int(mask, 16)

    for level in range(160):
        if mask & (1 << level) > 0:
            another_leaf = 0
        else:
            another_leaf = proof[proof_index]
            if isinstance(another_leaf, str):
                another_leaf = int(another_leaf, 16)

            proof_index += 1

        if key & (1 << level) == 0:
            left_leaf = current_leaf
            right_leaf = another_leaf
        else:
            left_leaf = another_leaf
            right_leaf = current_leaf

        current_leaf = sha3(left_leaf, right_leaf)
    return hex(current_leaf) == root
