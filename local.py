import os
import helper
from merkle import merkle

tree = merkle.CompactMerkleTree()
print(tree)
print(tree.tree_size)
print(tree.root_hash())
tree.append(b"hello")
afterOne = tree.root_hash()
tree.append(b"cruel")
tree.append(b"world")
print(tree.tree_size)
print(tree.root_hash())

