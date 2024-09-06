import uuid

from cfg.сonfig import settings
from src.dto.learning_set import LearningSet
from src.grpc.mapping_helper import learning_set_to_protobuf, learning_set_from_protobuf
from src.grpc.process_service import process_service_pb2
from src.grpc.process_service.client_process_manager import GRPCClientProcessManager
from src.log.logger import log_decorator, logger
from src.model.user_action_enum import UserActionEnum
from src.model.word_type_enum import WordTypeEnum


class ProcessService:

    server_address = settings.get_GRPC_conn

    @staticmethod
    @log_decorator(my_logger=logger)
    def start_learning_process(user_name: str, word_type: WordTypeEnum) -> LearningSet:
        with GRPCClientProcessManager(ProcessService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = process_service_pb2.StartLearningProcessRequest(
                user_name=user_name,
                word_type=word_type
            )
            protobuf_learning_set = stub.start_learning_process(request)
            response = learning_set_from_protobuf(protobuf_learning_set)
            return response

    @staticmethod
    @log_decorator(my_logger=logger)
    def get_learning_set(user_name: str, word_type: WordTypeEnum) -> LearningSet:
        with GRPCClientProcessManager(ProcessService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = process_service_pb2.StartLearningProcessRequest(
                user_name=user_name,
                word_type=word_type
            )
            protobuf_learning_set = stub.get_learning_set(request)
            response = learning_set_from_protobuf(protobuf_learning_set)
            return response

    @staticmethod
    @log_decorator(my_logger=logger)
    def update_learning_progress(user_id: uuid.UUID, word_id: uuid.UUID, german_word: str,
                                 user_action: UserActionEnum, word_type: WordTypeEnum) -> None:
        with GRPCClientProcessManager(ProcessService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = process_service_pb2.UpdateLearningProgressRequest(
                user_id=str(user_id),
                word_id=str(word_id),
                german_word=german_word,
                user_action=user_action,
                word_type=word_type
            )
            response = stub.update_learning_progress(request)
            return response

    @staticmethod
    @log_decorator(my_logger=logger)
    def add_learning_set_to_cash(learning_set: LearningSet) -> None:
        with GRPCClientProcessManager(ProcessService.server_address) as user_manager:
            stub = user_manager.get_stub()
            request = learning_set_to_protobuf(learning_set)
            response = stub.add_learning_set_to_cash(request)
            return response


def main():
    pass

if __name__ == '__main__':
    main()
