import base64
import hashlib
import helper
import struct


# 1) Get the Tree ID
# ./provision_tree.sh example-config.sh
tree_id = 1087559795015764672

# 2) Get the IP address
# kubectl port-forward service/trillian-log-service 35791:8090
ip_address = '127.0.0.1:35791'



value1 = b'123456789011'
value2 = b'123456789022'

def setup():
    response = helper.addLogEntry(ip_address, tree_id, value1)
    hash1 = res['queuedLeaf']['leaf']['leafIdentityHash']

    res = helper.addLogEntry(ip_address, tree_id, value2)
    hash2 = res['queuedLeaf']['leaf']['leafIdentityHash']

    print(res)



hash1 = helper.getLeafHash(value1)

res = helper.getInclusionProofByLeafHash(ip_address, tree_id, hash1, 4)
tree_root = res['signedLogRoot']['logRoot']
proof = res['proof'][0]
leaf_index = proof['leafIndex'] if 'leafIndex' in proof else 0
proof_hashes = proof['hashes']

helper.verifyInclusionProof(hash1, leaf_index, proof_hashes, tree_root)

print("Proof verified")
