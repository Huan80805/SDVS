# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import control_pb2 as control__pb2


class sendControlStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.process = channel.unary_unary(
                '/sendControl/process',
                request_serializer=control__pb2.controlRequest.SerializeToString,
                response_deserializer=control__pb2.controlResponse.FromString,
                )


class sendControlServicer(object):
    """Missing associated documentation comment in .proto file."""

    def process(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_sendControlServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'process': grpc.unary_unary_rpc_method_handler(
                    servicer.process,
                    request_deserializer=control__pb2.controlRequest.FromString,
                    response_serializer=control__pb2.controlResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sendControl', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class sendControl(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def process(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sendControl/process',
            control__pb2.controlRequest.SerializeToString,
            control__pb2.controlResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)