import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse
import grpc
import control_pb2
import control_pb2_grpc
import multiprocessing as mp
from concurrent import futures
from gstream import gstreamer_camera, gstreamer_rtmpstream
from multiprocessing import Process
class sendControlServicer(control_pb2_grpc.sendControlServicer):
    def __init__(self):
        mode = ["TEST", "OD", "HPT", "PE"]
        self.mapping = {i:t for i,t in enumerate(mode)}
        #start default algorithm and rtmp streaming
        self.mode = "OD"
        self.q1 = mp.Queue(maxsize=100)
        print(f"start default streaming on {self.mode}")
        self.p1 = Process(target=gstreamer_camera, args=(self.q1,))
        self.p2 = Process(target=gstreamer_rtmpstream, args=(self.q1,self.mode))
        self.p1.start()
        self.p2.start()
    def process(self, request, context):
        command = request.command
        c = self.switch_mode(command)
        response = control_pb2.controlResponse()
        response.check = c
        return response
    def switch_mode(self, command):
        if command not in range(4):
            return 0
        else:
            pre_mode = self.mode
            self.mode = self.mapping[command]
            if self.mode == pre_mode:
                print(f"already in {self.mode} mode")
                return 1
            print(f"switching mode to {self.mode}")
            #change algorithm
            self.terminate()
            self.q1 = mp.Queue(maxsize=100)
            self.p1 = Process(target=gstreamer_camera, args=(self.q1,))
            self.p2 = Process(target=gstreamer_rtmpstream, args=(self.q1,self.mode))
            self.p1.start()
            self.p2.start()
            return 1
    def terminate(self):
        self.p1.terminate()
        self.p2.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8080, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = sendControlServicer()
    control_pb2_grpc.add_sendControlServicer_to_server(servicer, server)

    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        servicer.terminate()

