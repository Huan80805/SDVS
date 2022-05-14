import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
import control_pb2
import control_pb2_grpc


def main(args):
    host = f"{args['ip']}:{args['port']}"
    print(host)
    command_type = ["TEST", "OD", "HPT", "PE"]
    mapping = {t:i for i, t in enumerate(command_type)}
    with grpc.insecure_channel(host) as channel:
        # parse command into integer 
        command = mapping[args["command"]]
        stub = control_pb2_grpc.sendControlStub(channel)
        request = control_pb2.controlRequest()
        request.command = command
        response = stub.process(request)
        if response.check == 0:
            print("command failed at remote")
        else:
            print("command succeeded")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.55.1")
    parser.add_argument("--port", type=int, default=8080)
    #type: test, object detection, hand pose tracking, pose estimation
    parser.add_argument("--command", type=str, 
                                    choices=["TEST", "OD", "HPT", "PE"], 
                                    help='type of algorithm')
    args = vars(parser.parse_args())
    main(args)
