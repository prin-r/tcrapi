from eth_utils import keccak


def sha3(left, right):
    if left == 0 and right == 0:
        return 0

    s = b""
    for each in (left, right):
        s += each.to_bytes(32, "big")
    hash_hex = keccak(primitive=s).hex()
    return int(hash_hex, 16)


class Smt(object):
    def __init__(self):
        self.root = 0
        self.hashes = {0: (0, 0)}

    def insert(self, key, val):
        if isinstance(key, str):
            key = int(key, 16)

        self.root = self._insert(key, val, self.root, 0)

    def _insert(self, key, val, current_root, current_level):
        if current_level == 160:
            return val

        left, right = self.hashes[current_root]
        if key & (1 << (159 - current_level)) == 0:
            left = self._insert(key, val, left, current_level + 1)
        else:
            right = self._insert(key, val, right, current_level + 1)

        new_root = sha3(left, right)
        self.hashes[new_root] = (left, right)
        return new_root

