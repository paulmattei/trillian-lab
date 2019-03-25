import grpc
import trillian_admin_api_pb2
import trillian_admin_api_pb2_grpc
from google.protobuf.json_format import MessageToJson
import json
from merkle import merkle
from collections import namedtuple

def listTrees(ip_address):

    with grpc.insecure_channel(ip_address + ":8090") as channel:
        stub = trillian_admin_api_pb2_grpc.TrillianAdminStub(channel)
        response_protobuf = stub.ListTrees(trillian_admin_api_pb2.ListTreesRequest())

    response_json = (MessageToJson(response_protobuf))
    response_dict = json.loads(response_json)

    trees = []
    for tree in response_dict["tree"]:
        trees.append((tree["treeId"]))
    return trees


def addLogEntry(ip_address, log_id, leaf_data, metadata="00:00:00"):

    with grpc.insecure_channel(ip_address + ":8090") as channel:
        stub = trillian_log_api_pb2_grpc.TrillianLogStub(channel)
        response_protobuf = stub.QueueLeaf(trillian_log_api_pb2.QueueLeafRequest(
            log_id=log_id, 
            leaf=trillian_log_api_pb2.LogLeaf(
                leaf_value = leaf_data.encode(),
                extra_data = metadata.encode()
        )))

    response_json = (MessageToJson(response_protobuf))
    response_dict = json.loads(response_json)
    return response_dict


def getInclusionProofByLeafHash(ip_address, log_id, leaf_hash, tree_size):

    leaf_hash = base64.decodestring(leaf_hash.encode())
    with grpc.insecure_channel(ip_address + ":8090") as channel:
        stub = trillian_log_api_pb2_grpc.TrillianLogStub(channel)
        response_protobuf = stub.GetInclusionProofByHash(trillian_log_api_pb2.GetInclusionProofByHashRequest( 
            log_id = log_id,
            leaf_hash = [leaf_hash],
            tree_size = tree_szie
        ))
    response_json = (MessageToJson(response_protobuf))
    response_dict = json.loads(response_json)
    return response_dict


def verifyInclusionProof(leaf_hash, leaf_index, proof, tree_size, root_hash):
    verifier = merkle.MerkleVerifier()
    sth = namedtuple("STH", ["sha256_root_hash", "tree_size"])

    return verifier.verify_leaf_hash_inclusion(leaf_hash, leaf_index, proof, sth(root_hash, tree_size))
