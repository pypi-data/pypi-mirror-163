# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ondewo.s2t import speech_to_text_pb2 as ondewo_dot_s2t_dot_speech__to__text__pb2


class Speech2TextStub(object):
    """endpoints of speech-to-text service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TranscribeFile = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/TranscribeFile',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeFileRequest.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeFileResponse.FromString,
                )
        self.TranscribeStream = channel.stream_stream(
                '/ondewo.s2t.Speech2Text/TranscribeStream',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeStreamRequest.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeStreamResponse.FromString,
                )
        self.GetS2tPipeline = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/GetS2tPipeline',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.FromString,
                )
        self.CreateS2tPipeline = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/CreateS2tPipeline',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.FromString,
                )
        self.DeleteS2tPipeline = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/DeleteS2tPipeline',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.UpdateS2tPipeline = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/UpdateS2tPipeline',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.ListS2tPipelines = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/ListS2tPipelines',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tPipelinesRequest.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tPipelinesResponse.FromString,
                )
        self.ListS2tLanguages = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/ListS2tLanguages',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguagesRequest.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguagesResponse.FromString,
                )
        self.ListS2tDomains = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/ListS2tDomains',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tDomainsRequest.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tDomainsResponse.FromString,
                )
        self.GetServiceInfo = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/GetServiceInfo',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.S2TGetServiceInfoResponse.FromString,
                )
        self.ListS2tLanguageModels = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/ListS2tLanguageModels',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguageModelsRequest.SerializeToString,
                response_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguageModelsResponse.FromString,
                )
        self.CreateUserLanguageModel = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/CreateUserLanguageModel',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.CreateUserLanguageModelRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.DeleteUserLanguageModel = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/DeleteUserLanguageModel',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.DeleteUserLanguageModelRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.AddDataToUserLanguageModel = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/AddDataToUserLanguageModel',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.AddDataToUserLanguageModelRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.TrainUserLanguageModel = channel.unary_unary(
                '/ondewo.s2t.Speech2Text/TrainUserLanguageModel',
                request_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TrainUserLanguageModelRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class Speech2TextServicer(object):
    """endpoints of speech-to-text service
    """

    def TranscribeFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TranscribeStream(self, request_iterator, context):
        """Transcribes an audio stream.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetS2tPipeline(self, request, context):
        """Gets a speech to text pipeline corresponding to the id specified in S2tPipelineId. If no corresponding id is
        found, raises ModuleNotFoundError in server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateS2tPipeline(self, request, context):
        """Creates a new speech to text pipeline from a Speech2TextConfig and registers the new pipeline in the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteS2tPipeline(self, request, context):
        """Deletes a pipeline corresponding to the id parsed in S2TPipelineId. If no corresponding id is
        found, raises ModuleNotFoundError in server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateS2tPipeline(self, request, context):
        """Updates a pipeline with the id specified in Speech2TextConfig with the new config. If no corresponding id is
        found, raises ModuleNotFoundError in server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListS2tPipelines(self, request, context):
        """Lists all speech to text pipelines.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListS2tLanguages(self, request, context):
        """Returns a message containing a list of all languages for which there exist pipelines.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListS2tDomains(self, request, context):
        """Returns a message containing a list of all domains for which there exist pipelines.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServiceInfo(self, request, context):
        """Returns a message containing the version of the running speech to text server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListS2tLanguageModels(self, request, context):
        """Given a list of pipeline ids, returns a list of LanguageModelPipelineId messages containing the pipeline
        id and a list of the language models loaded in the pipeline.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateUserLanguageModel(self, request, context):
        """Create a user language model.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUserLanguageModel(self, request, context):
        """Delete a user language model.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddDataToUserLanguageModel(self, request, context):
        """Add data to a user language model.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TrainUserLanguageModel(self, request, context):
        """Train a user language model.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_Speech2TextServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TranscribeFile': grpc.unary_unary_rpc_method_handler(
                    servicer.TranscribeFile,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeFileRequest.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeFileResponse.SerializeToString,
            ),
            'TranscribeStream': grpc.stream_stream_rpc_method_handler(
                    servicer.TranscribeStream,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeStreamRequest.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeStreamResponse.SerializeToString,
            ),
            'GetS2tPipeline': grpc.unary_unary_rpc_method_handler(
                    servicer.GetS2tPipeline,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.SerializeToString,
            ),
            'CreateS2tPipeline': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateS2tPipeline,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.SerializeToString,
            ),
            'DeleteS2tPipeline': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteS2tPipeline,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'UpdateS2tPipeline': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateS2tPipeline,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ListS2tPipelines': grpc.unary_unary_rpc_method_handler(
                    servicer.ListS2tPipelines,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tPipelinesRequest.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tPipelinesResponse.SerializeToString,
            ),
            'ListS2tLanguages': grpc.unary_unary_rpc_method_handler(
                    servicer.ListS2tLanguages,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguagesRequest.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguagesResponse.SerializeToString,
            ),
            'ListS2tDomains': grpc.unary_unary_rpc_method_handler(
                    servicer.ListS2tDomains,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tDomainsRequest.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tDomainsResponse.SerializeToString,
            ),
            'GetServiceInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServiceInfo,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.S2TGetServiceInfoResponse.SerializeToString,
            ),
            'ListS2tLanguageModels': grpc.unary_unary_rpc_method_handler(
                    servicer.ListS2tLanguageModels,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguageModelsRequest.FromString,
                    response_serializer=ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguageModelsResponse.SerializeToString,
            ),
            'CreateUserLanguageModel': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateUserLanguageModel,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.CreateUserLanguageModelRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'DeleteUserLanguageModel': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteUserLanguageModel,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.DeleteUserLanguageModelRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'AddDataToUserLanguageModel': grpc.unary_unary_rpc_method_handler(
                    servicer.AddDataToUserLanguageModel,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.AddDataToUserLanguageModelRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'TrainUserLanguageModel': grpc.unary_unary_rpc_method_handler(
                    servicer.TrainUserLanguageModel,
                    request_deserializer=ondewo_dot_s2t_dot_speech__to__text__pb2.TrainUserLanguageModelRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ondewo.s2t.Speech2Text', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Speech2Text(object):
    """endpoints of speech-to-text service
    """

    @staticmethod
    def TranscribeFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/TranscribeFile',
            ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeFileRequest.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TranscribeStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/ondewo.s2t.Speech2Text/TranscribeStream',
            ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeStreamRequest.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.TranscribeStreamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetS2tPipeline(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/GetS2tPipeline',
            ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateS2tPipeline(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/CreateS2tPipeline',
            ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteS2tPipeline(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/DeleteS2tPipeline',
            ondewo_dot_s2t_dot_speech__to__text__pb2.S2tPipelineId.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateS2tPipeline(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/UpdateS2tPipeline',
            ondewo_dot_s2t_dot_speech__to__text__pb2.Speech2TextConfig.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListS2tPipelines(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/ListS2tPipelines',
            ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tPipelinesRequest.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tPipelinesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListS2tLanguages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/ListS2tLanguages',
            ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguagesRequest.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguagesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListS2tDomains(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/ListS2tDomains',
            ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tDomainsRequest.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tDomainsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetServiceInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/GetServiceInfo',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.S2TGetServiceInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListS2tLanguageModels(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/ListS2tLanguageModels',
            ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguageModelsRequest.SerializeToString,
            ondewo_dot_s2t_dot_speech__to__text__pb2.ListS2tLanguageModelsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateUserLanguageModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/CreateUserLanguageModel',
            ondewo_dot_s2t_dot_speech__to__text__pb2.CreateUserLanguageModelRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteUserLanguageModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/DeleteUserLanguageModel',
            ondewo_dot_s2t_dot_speech__to__text__pb2.DeleteUserLanguageModelRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddDataToUserLanguageModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/AddDataToUserLanguageModel',
            ondewo_dot_s2t_dot_speech__to__text__pb2.AddDataToUserLanguageModelRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TrainUserLanguageModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.s2t.Speech2Text/TrainUserLanguageModel',
            ondewo_dot_s2t_dot_speech__to__text__pb2.TrainUserLanguageModelRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
