import uuid

from src.dto.schema import UserCreateTelegramDTO, UserCreateFullDTO
from src.grpc.mapping_helper import convert_proto_to_pydantic
from src.grpc.user_service import user_service_pb2
from src.grpc.user_service.client_user_manager import GRPCClientUserManager
from src.log.logger import log_decorator, CustomLogger

class UserService:

    # TODO: Place it to env settings
    server_address = 'localhost:50051'  # Replace with your gRPC server address

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_user_by_id(user_id: uuid.UUID) -> UserCreateFullDTO:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserIdRequest(
                user_id=str(user_id)
            )
            response = stub.get_user_by_id(request)
            dto = convert_proto_to_pydantic(response, UserCreateFullDTO)
            return dto

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_user_by_name(user_name: str) -> UserCreateFullDTO:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserNameRequest(
                user_name=user_name
            )
            response = stub.get_user_by_name(request)
            dto = convert_proto_to_pydantic(response, UserCreateFullDTO)
            return dto

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_user_id_by_name(user_name: str) -> uuid.UUID:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserNameRequest(
                user_name=user_name
            )
            response = stub.get_user_id_by_name(request)
            return response.user_id

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_user_training_length(user_name: str, new_training_length: int) -> None:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserTrainingLengthRequest(
                user_name=user_name,
                training_length=new_training_length
            )
            stub.update_user_training_length(request)

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def is_user_created(user_name: str) -> bool:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserNameRequest(
                user_name=user_name
            )
            response = stub.is_user_created(request)
            return response.result


    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_user_by_DTO(new_user: UserCreateTelegramDTO) -> None:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserCreateTelegramDTORequest(
                id=str(uuid.uuid4()),
                user_name=new_user.user_name,
                training_length=new_user.training_length,
                telegram_user_id=new_user.telegram_user_id,
                hashed_password=new_user.hashed_password,
                email=new_user.email
            )
            response = stub.create_user_by_DTO(request)

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_user(name: str, email: str, password: str, telegram_id: str, training_length: int = 10) -> None:
        with GRPCClientUserManager(UserService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = user_service_pb2.UserRequest(
                name=name,
                email=email,
                password=password,
                telegram_id=telegram_id,
                training_length=training_length
            )
            stub.create_user(request)

def main():
    res = UserService.get_user_by_name('newGrpcUser')
    print(res)

if __name__ == '__main__':
    main()
