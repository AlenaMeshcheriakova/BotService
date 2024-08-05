from typing import Optional

import grpc
from src.grpc.word_service import word_service_pb2_grpc


class GRPCClientWordManager:
    def __init__(self, server_address: str):
        self.server_address = server_address
        self.channel: Optional[grpc.Channel] = None
        self.stub: Optional[word_service_pb2_grpc.WordServiceStub] = None

    def _create_channel(self) -> grpc.Channel:
        if self.channel is None:
            self.channel = grpc.insecure_channel(self.server_address)
        return self.channel

    def get_stub(self) -> word_service_pb2_grpc.WordServiceStub:
        if self.stub is None:
            self.stub = word_service_pb2_grpc.WordServiceStub(self._create_channel())
        return self.stub

    def close(self) -> None:
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None

    def __enter__(self) -> 'GRPCClientWordManager':
        # Optionally, you can initialize or open resources here
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Cleanup resources here
        self.close()