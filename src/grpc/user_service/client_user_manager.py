from typing import Optional

import grpc
from src.grpc.user_service import user_service_pb2_grpc


class GRPCClientUserManager:
    def __init__(self, server_address: str):
        self.server_address = server_address
        self.channel: Optional[grpc.Channel] = None
        self.stub: Optional[user_service_pb2_grpc.UserServiceGRPCStub] = None

    def _create_channel(self) -> grpc.Channel:
        if self.channel is None:
            self.channel = grpc.insecure_channel(self.server_address)
        return self.channel

    def get_stub(self) -> user_service_pb2_grpc.UserServiceGRPCStub:
        if self.stub is None:
            self.stub = user_service_pb2_grpc.UserServiceGRPCStub(self._create_channel())
        return self.stub

    def close(self) -> None:
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None

    def __enter__(self) -> 'GRPCClientUserManager':
        # Optionally, you can initialize or open resources here
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Cleanup resources here
        self.close()


def main():
    pass
    # res = UserService.is_user_created('newGrpcUser')
    # print(res)

if __name__ == '__main__':
    main()

