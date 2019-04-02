import grpc
import hashlib
import trillian_admin_api_pb2
import trillian_admin_api_pb2_grpc
import trillian_log_api_pb2
import trillian_log_api_pb2_grpc
import base64
from google.protobuf.json_format import MessageToJson
import json
import struct
from merkle import merkle
from collections import namedtuple


def listTrees(ip_address):

    with grpc.insecure_channel(ip_address) as channel:
        stub = trillian_admin_api_pb2_grpc.TrillianAdminStub(channel)
        response_protobuf = stub.ListTrees(trillian_admin_api_pb2.ListTreesRequest(show_deleted=False))

    response_json = (MessageToJson(response_protobuf))
    response_dict = json.loads(response_json)

    trees = []
    for tree in response_dict["tree"]:
        trees.append((tree["treeId"]))
    return trees


def addLogEntry(ip_address, log_id, leaf_data, metadata=b"00:00:00"):

    with grpc.insecure_channel(ip_address) as channel:
        stub = trillian_log_api_pb2_grpc.TrillianLogStub(channel)
        return stub.QueueLeaf(trillian_log_api_pb2.QueueLeafRequest(
            log_id=log_id,
            leaf=trillian_log_api_pb2.LogLeaf(
                leaf_value=leaf_data,
                extra_data=metadata
        )))


def getLeafHash(leaf_data):
    hasher = hashlib.sha256()
    hasher.update(b"\x00" + leaf_data)
    return hasher.digest()


def getInclusionProofByLeafHash(ip_address, log_id, leaf_hash, tree_size):

    with grpc.insecure_channel(ip_address) as channel:
        stub = trillian_log_api_pb2_grpc.TrillianLogStub(channel)
        response_protobuf = stub.GetInclusionProofByHash(trillian_log_api_pb2.GetInclusionProofByHashRequest(
            log_id=log_id,
            leaf_hash=leaf_hash,
            tree_size=tree_size
        ))
    response_json = (MessageToJson(response_protobuf))
    response_dict = json.loads(response_json)
    return response_dict


def verifyInclusionProof(leaf_hash, leaf_index, proof, log_root):
    # TODO: should check signature here
    decoded_root = base64.b64decode(log_root)
    _, tree_size, hash_size = struct.unpack('>HQB', decoded_root[:11])
    root_hash = struct.unpack('>{}s'.format(hash_size), decoded_root[11:11+hash_size])[0]
    return verifyInclusionProof2(leaf_hash, leaf_index, proof, tree_size, root_hash)


def verifyInclusionProof2(leaf_hash, leaf_index, proof, tree_size, root_hash):
    verifier = merkle.MerkleVerifier()
    sth = namedtuple("STH", ["sha256_root_hash", "tree_size"])

    proof_hashes = [base64.b64decode(h) for h in proof]

    return verifier.verify_leaf_hash_inclusion(leaf_hash, leaf_index, proof_hashes, sth(root_hash, tree_size))
