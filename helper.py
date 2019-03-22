import grpc
import trillian_admin_api_pb2
import trillian_admin_api_pb2_grpc
from google.protobuf.json_format import MessageToJson
import json

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