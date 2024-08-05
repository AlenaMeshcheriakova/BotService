from typing import Optional

import grpc
from src.grpc.process_service import process_service_pb2_grpc


class GRPCClientProcessManager:
    def __init__(self, server_address: str):
        self.server_address = server_address
        self.channel: Optional[grpc.Channel] = None
        self.stub: Optional[process_service_pb2_grpc.ProcessServiceStub] = None

    def _create_channel(self) -> grpc.Channel:
        if self.channel is None:
            self.channel = grpc.insecure_channel(self.server_address)
        return self.channel

    def get_stub(self) -> process_service_pb2_grpc.ProcessServiceStub:
        if self.stub is None:
            self.stub = process_service_pb2_grpc.ProcessServiceStub(self._create_channel())
        return self.stub

    def close(self) -> None:
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None

    def __enter__(self) -> 'GRPCClientProcessManager':
        # Optionally, you can initialize or open resources here
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Cleanup resources here
        self.close()

def main():
    pass

if __name__ == '__main__':
    main()

