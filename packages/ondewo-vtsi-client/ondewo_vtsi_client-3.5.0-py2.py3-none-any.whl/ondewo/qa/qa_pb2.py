# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ondewo/qa/qa.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ondewo.nlu import session_pb2 as ondewo_dot_nlu_dot_session__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12ondewo/qa/qa.proto\x12\tondewo.qa\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x18ondewo/nlu/session.proto\"\xfb\x01\n\x10GetAnswerRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12#\n\x04text\x18\x02 \x01(\x0b\x32\x15.ondewo.nlu.TextInput\x12\x17\n\x0fmax_num_answers\x18\x03 \x01(\x05\x12\x18\n\x10threshold_reader\x18\x04 \x01(\x02\x12\x1b\n\x13threshold_retriever\x18\x05 \x01(\x02\x12\x19\n\x11threshold_overall\x18\x06 \x01(\x02\x12\x19\n\x11reader_model_name\x18\x07 \x01(\t\x12(\n\nurl_filter\x18\x08 \x01(\x0b\x32\x14.ondewo.qa.UrlFilter\"K\n\x11GetAnswerResponse\x12\x36\n\x0cquery_result\x18\x02 \x01(\x0b\x32 .ondewo.nlu.DetectIntentResponse\"(\n\x11RunScraperRequest\x12\x13\n\x0bproject_ids\x18\x01 \x03(\t\"\xa2\x01\n\x12RunScraperResponse\x12J\n\x12scraper_containers\x18\x01 \x03(\x0b\x32..ondewo.qa.RunScraperResponse.ScraperContainer\x1a@\n\x10ScraperContainer\x12\x16\n\x0e\x63ontainer_name\x18\x01 \x01(\t\x12\x14\n\x0c\x63ontainer_id\x18\x02 \x01(\t\"3\n\x13RunTrainingResponse\x12\n\n\x02\x66\x31\x18\x01 \x01(\x02\x12\x10\n\x08\x61\x63\x63uracy\x18\x02 \x01(\x02\"_\n\tUrlFilter\x12\x16\n\x0e\x61llowed_values\x18\x01 \x03(\t\x12\x1c\n\x14regex_filter_include\x18\x02 \x01(\t\x12\x1c\n\x14regex_filter_exclude\x18\x03 \x01(\t\"1\n\x16GetServerStateResponse\x12\x17\n\x0fserver_is_ready\x18\x01 \x01(\x08\"-\n\x16ListProjectIdsResponse\x12\x13\n\x0bproject_ids\x18\x01 \x03(\t\"-\n\x17GetProjectConfigRequest\x12\x12\n\nproject_id\x18\x01 \x01(\t\"5\n\x18GetProjectConfigResponse\x12\x19\n\x11\x63onfig_serialized\x18\x01 \x01(\t\",\n\x15UpdateDatabaseRequest\x12\x13\n\x0bproject_ids\x18\x01 \x03(\t\"0\n\x16UpdateDatabaseResponse\x12\x16\n\x0e\x65rror_messages\x18\x01 \x03(\t2\xe0\x05\n\x02QA\x12V\n\tGetAnswer\x12\x1b.ondewo.qa.GetAnswerRequest\x1a\x1c.ondewo.qa.GetAnswerResponse\"\x0e\x82\xd3\xe4\x93\x02\x08\"\x03/qa:\x01*\x12\x61\n\nRunScraper\x12\x1c.ondewo.qa.RunScraperRequest\x1a\x1d.ondewo.qa.RunScraperResponse\"\x16\x82\xd3\xe4\x93\x02\x10\x12\x0e/qa:RunScraper\x12q\n\x0eUpdateDatabase\x12 .ondewo.qa.UpdateDatabaseRequest\x1a!.ondewo.qa.UpdateDatabaseResponse\"\x1a\x82\xd3\xe4\x93\x02\x14\x12\x12/qa:UpdateDatabase\x12^\n\x0bRunTraining\x12\x16.google.protobuf.Empty\x1a\x1e.ondewo.qa.RunTrainingResponse\"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/qa:RunTraining\x12g\n\x0eGetServerState\x12\x16.google.protobuf.Empty\x1a!.ondewo.qa.GetServerStateResponse\"\x1a\x82\xd3\xe4\x93\x02\x14\x12\x12/qa:GetServerState\x12g\n\x0eListProjectIds\x12\x16.google.protobuf.Empty\x1a!.ondewo.qa.ListProjectIdsResponse\"\x1a\x82\xd3\xe4\x93\x02\x14\x12\x12/qa:ListProjectIds\x12z\n\x10GetProjectConfig\x12\".ondewo.qa.GetProjectConfigRequest\x1a#.ondewo.qa.GetProjectConfigResponse\"\x1d\x82\xd3\xe4\x93\x02\x17\x12\x15/qa:ListProjectConfigb\x06proto3')



_GETANSWERREQUEST = DESCRIPTOR.message_types_by_name['GetAnswerRequest']
_GETANSWERRESPONSE = DESCRIPTOR.message_types_by_name['GetAnswerResponse']
_RUNSCRAPERREQUEST = DESCRIPTOR.message_types_by_name['RunScraperRequest']
_RUNSCRAPERRESPONSE = DESCRIPTOR.message_types_by_name['RunScraperResponse']
_RUNSCRAPERRESPONSE_SCRAPERCONTAINER = _RUNSCRAPERRESPONSE.nested_types_by_name['ScraperContainer']
_RUNTRAININGRESPONSE = DESCRIPTOR.message_types_by_name['RunTrainingResponse']
_URLFILTER = DESCRIPTOR.message_types_by_name['UrlFilter']
_GETSERVERSTATERESPONSE = DESCRIPTOR.message_types_by_name['GetServerStateResponse']
_LISTPROJECTIDSRESPONSE = DESCRIPTOR.message_types_by_name['ListProjectIdsResponse']
_GETPROJECTCONFIGREQUEST = DESCRIPTOR.message_types_by_name['GetProjectConfigRequest']
_GETPROJECTCONFIGRESPONSE = DESCRIPTOR.message_types_by_name['GetProjectConfigResponse']
_UPDATEDATABASEREQUEST = DESCRIPTOR.message_types_by_name['UpdateDatabaseRequest']
_UPDATEDATABASERESPONSE = DESCRIPTOR.message_types_by_name['UpdateDatabaseResponse']
GetAnswerRequest = _reflection.GeneratedProtocolMessageType('GetAnswerRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETANSWERREQUEST,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.GetAnswerRequest)
  })
_sym_db.RegisterMessage(GetAnswerRequest)

GetAnswerResponse = _reflection.GeneratedProtocolMessageType('GetAnswerResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETANSWERRESPONSE,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.GetAnswerResponse)
  })
_sym_db.RegisterMessage(GetAnswerResponse)

RunScraperRequest = _reflection.GeneratedProtocolMessageType('RunScraperRequest', (_message.Message,), {
  'DESCRIPTOR' : _RUNSCRAPERREQUEST,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.RunScraperRequest)
  })
_sym_db.RegisterMessage(RunScraperRequest)

RunScraperResponse = _reflection.GeneratedProtocolMessageType('RunScraperResponse', (_message.Message,), {

  'ScraperContainer' : _reflection.GeneratedProtocolMessageType('ScraperContainer', (_message.Message,), {
    'DESCRIPTOR' : _RUNSCRAPERRESPONSE_SCRAPERCONTAINER,
    '__module__' : 'ondewo.qa.qa_pb2'
    # @@protoc_insertion_point(class_scope:ondewo.qa.RunScraperResponse.ScraperContainer)
    })
  ,
  'DESCRIPTOR' : _RUNSCRAPERRESPONSE,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.RunScraperResponse)
  })
_sym_db.RegisterMessage(RunScraperResponse)
_sym_db.RegisterMessage(RunScraperResponse.ScraperContainer)

RunTrainingResponse = _reflection.GeneratedProtocolMessageType('RunTrainingResponse', (_message.Message,), {
  'DESCRIPTOR' : _RUNTRAININGRESPONSE,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.RunTrainingResponse)
  })
_sym_db.RegisterMessage(RunTrainingResponse)

UrlFilter = _reflection.GeneratedProtocolMessageType('UrlFilter', (_message.Message,), {
  'DESCRIPTOR' : _URLFILTER,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.UrlFilter)
  })
_sym_db.RegisterMessage(UrlFilter)

GetServerStateResponse = _reflection.GeneratedProtocolMessageType('GetServerStateResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSERVERSTATERESPONSE,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.GetServerStateResponse)
  })
_sym_db.RegisterMessage(GetServerStateResponse)

ListProjectIdsResponse = _reflection.GeneratedProtocolMessageType('ListProjectIdsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTPROJECTIDSRESPONSE,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.ListProjectIdsResponse)
  })
_sym_db.RegisterMessage(ListProjectIdsResponse)

GetProjectConfigRequest = _reflection.GeneratedProtocolMessageType('GetProjectConfigRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPROJECTCONFIGREQUEST,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.GetProjectConfigRequest)
  })
_sym_db.RegisterMessage(GetProjectConfigRequest)

GetProjectConfigResponse = _reflection.GeneratedProtocolMessageType('GetProjectConfigResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETPROJECTCONFIGRESPONSE,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.GetProjectConfigResponse)
  })
_sym_db.RegisterMessage(GetProjectConfigResponse)

UpdateDatabaseRequest = _reflection.GeneratedProtocolMessageType('UpdateDatabaseRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDATABASEREQUEST,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.UpdateDatabaseRequest)
  })
_sym_db.RegisterMessage(UpdateDatabaseRequest)

UpdateDatabaseResponse = _reflection.GeneratedProtocolMessageType('UpdateDatabaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDATABASERESPONSE,
  '__module__' : 'ondewo.qa.qa_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.qa.UpdateDatabaseResponse)
  })
_sym_db.RegisterMessage(UpdateDatabaseResponse)

_QA = DESCRIPTOR.services_by_name['QA']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _QA.methods_by_name['GetAnswer']._options = None
  _QA.methods_by_name['GetAnswer']._serialized_options = b'\202\323\344\223\002\010\"\003/qa:\001*'
  _QA.methods_by_name['RunScraper']._options = None
  _QA.methods_by_name['RunScraper']._serialized_options = b'\202\323\344\223\002\020\022\016/qa:RunScraper'
  _QA.methods_by_name['UpdateDatabase']._options = None
  _QA.methods_by_name['UpdateDatabase']._serialized_options = b'\202\323\344\223\002\024\022\022/qa:UpdateDatabase'
  _QA.methods_by_name['RunTraining']._options = None
  _QA.methods_by_name['RunTraining']._serialized_options = b'\202\323\344\223\002\021\022\017/qa:RunTraining'
  _QA.methods_by_name['GetServerState']._options = None
  _QA.methods_by_name['GetServerState']._serialized_options = b'\202\323\344\223\002\024\022\022/qa:GetServerState'
  _QA.methods_by_name['ListProjectIds']._options = None
  _QA.methods_by_name['ListProjectIds']._serialized_options = b'\202\323\344\223\002\024\022\022/qa:ListProjectIds'
  _QA.methods_by_name['GetProjectConfig']._options = None
  _QA.methods_by_name['GetProjectConfig']._serialized_options = b'\202\323\344\223\002\027\022\025/qa:ListProjectConfig'
  _GETANSWERREQUEST._serialized_start=119
  _GETANSWERREQUEST._serialized_end=370
  _GETANSWERRESPONSE._serialized_start=372
  _GETANSWERRESPONSE._serialized_end=447
  _RUNSCRAPERREQUEST._serialized_start=449
  _RUNSCRAPERREQUEST._serialized_end=489
  _RUNSCRAPERRESPONSE._serialized_start=492
  _RUNSCRAPERRESPONSE._serialized_end=654
  _RUNSCRAPERRESPONSE_SCRAPERCONTAINER._serialized_start=590
  _RUNSCRAPERRESPONSE_SCRAPERCONTAINER._serialized_end=654
  _RUNTRAININGRESPONSE._serialized_start=656
  _RUNTRAININGRESPONSE._serialized_end=707
  _URLFILTER._serialized_start=709
  _URLFILTER._serialized_end=804
  _GETSERVERSTATERESPONSE._serialized_start=806
  _GETSERVERSTATERESPONSE._serialized_end=855
  _LISTPROJECTIDSRESPONSE._serialized_start=857
  _LISTPROJECTIDSRESPONSE._serialized_end=902
  _GETPROJECTCONFIGREQUEST._serialized_start=904
  _GETPROJECTCONFIGREQUEST._serialized_end=949
  _GETPROJECTCONFIGRESPONSE._serialized_start=951
  _GETPROJECTCONFIGRESPONSE._serialized_end=1004
  _UPDATEDATABASEREQUEST._serialized_start=1006
  _UPDATEDATABASEREQUEST._serialized_end=1050
  _UPDATEDATABASERESPONSE._serialized_start=1052
  _UPDATEDATABASERESPONSE._serialized_end=1100
  _QA._serialized_start=1103
  _QA._serialized_end=1839
# @@protoc_insertion_point(module_scope)
