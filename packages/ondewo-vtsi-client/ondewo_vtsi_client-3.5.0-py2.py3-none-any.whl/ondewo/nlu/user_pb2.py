# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ondewo/nlu/user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from ondewo.nlu import project_role_pb2 as ondewo_dot_nlu_dot_project__role__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15ondewo/nlu/user.proto\x12\nondewo.nlu\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a\x1dondewo/nlu/project_role.proto\"Y\n\x04User\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x03 \x01(\t\x12\x16\n\x0eserver_role_id\x18\x06 \x01(\r\x12\x12\n\nuser_email\x18\x07 \x01(\t\"\xb7\x01\n\x08UserInfo\x12\x1e\n\x04user\x18\x01 \x01(\x0b\x32\x10.ondewo.nlu.User\x12=\n\rproject_roles\x18\x02 \x03(\x0b\x32&.ondewo.nlu.UserInfo.ProjectRolesEntry\x1aL\n\x11ProjectRolesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.ondewo.nlu.ProjectRole:\x02\x38\x01\"E\n\x11\x43reateUserRequest\x12\x1e\n\x04user\x18\x01 \x01(\x0b\x32\x10.ondewo.nlu.User\x12\x10\n\x08password\x18\x03 \x01(\t\"v\n\x11UpdateUserRequest\x12\x1e\n\x04user\x18\x01 \x01(\x0b\x32\x10.ondewo.nlu.User\x12\x10\n\x08password\x18\x04 \x01(\t\x12/\n\x0bupdate_mask\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"L\n\x0eGetUserRequest\x12\x11\n\x07user_id\x18\x01 \x01(\tH\x00\x12\x14\n\nuser_email\x18\x03 \x01(\tH\x00\x42\x11\n\x0fuser_identifier\"$\n\x11\x44\x65leteUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"&\n\x10ListUsersRequest\x12\x12\n\npage_token\x18\x01 \x01(\t\"M\n\x11ListUsersResponse\x12\x1f\n\x05users\x18\x01 \x03(\x0b\x32\x10.ondewo.nlu.User\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"U\n\x15ListUserInfosResponse\x12#\n\x05users\x18\x01 \x03(\x0b\x32\x14.ondewo.nlu.UserInfo\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"@\n\nServerRole\x12\x0f\n\x07role_id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0bpermissions\x18\x03 \x03(\t\"?\n\x17\x43reateServerRoleRequest\x12$\n\x04role\x18\x01 \x01(\x0b\x32\x16.ondewo.nlu.ServerRole\"p\n\x17UpdateServerRoleRequest\x12$\n\x04role\x18\x01 \x01(\x0b\x32\x16.ondewo.nlu.ServerRole\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"*\n\x17\x44\x65leteServerRoleRequest\x12\x0f\n\x07role_id\x18\x01 \x01(\r\"X\n\x14GetServerRoleRequest\x12\x11\n\x07role_id\x18\x01 \x01(\rH\x00\x12\x13\n\trole_name\x18\x02 \x01(\tH\x00\x42\x18\n\x16server_role_identifier\",\n\x16ListServerRolesRequest\x12\x12\n\npage_token\x18\x01 \x01(\t\"`\n\x17ListServerRolesResponse\x12,\n\x0cserver_roles\x18\x01 \x03(\x0b\x32\x16.ondewo.nlu.ServerRole\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"2\n\x1cListServerPermissionsRequest\x12\x12\n\npage_token\x18\x01 \x01(\t\"M\n\x1dListServerPermissionsResponse\x12\x13\n\x0bpermissions\x18\x01 \x03(\t\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"4\n\x0cLoginRequest\x12\x12\n\nuser_email\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"C\n\rLoginResponse\x12\x1e\n\x04user\x18\x01 \x01(\x0b\x32\x10.ondewo.nlu.User\x12\x12\n\nauth_token\x18\x02 \x01(\t*w\n\x11\x44\x65\x66\x61ultServerRole\x12\x16\n\x12SERVER_UNSPECIFIED\x10\x00\x12\x0f\n\x0bSERVER_USER\x10\x01\x12\x12\n\x0eSERVER_MANAGER\x10\x02\x12\x10\n\x0cSERVER_ADMIN\x10\x03\x12\x13\n\x0fSERVER_INACTIVE\x10\x04\x32\xa3\x0c\n\x05Users\x12S\n\nCreateUser\x12\x1d.ondewo.nlu.CreateUserRequest\x1a\x10.ondewo.nlu.User\"\x14\x82\xd3\xe4\x93\x02\x0e\"\t/v2/users:\x01*\x12^\n\x07GetUser\x12\x1a.ondewo.nlu.GetUserRequest\x1a\x10.ondewo.nlu.User\"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/v2/users/{user_identifier=*}\x12k\n\x0bGetUserInfo\x12\x1a.ondewo.nlu.GetUserRequest\x1a\x14.ondewo.nlu.UserInfo\"*\x82\xd3\xe4\x93\x02$\x12\"/v2/user_infos/{user_identifier=*}\x12g\n\nDeleteUser\x12\x1a.ondewo.nlu.GetUserRequest\x1a\x16.google.protobuf.Empty\"%\x82\xd3\xe4\x93\x02\x1f*\x1d/v2/users/{user_identifier=*}\x12S\n\nUpdateUser\x12\x1d.ondewo.nlu.UpdateUserRequest\x1a\x10.ondewo.nlu.User\"\x14\x82\xd3\xe4\x93\x02\x0e\x32\t/v2/users:\x01*\x12[\n\tListUsers\x12\x1c.ondewo.nlu.ListUsersRequest\x1a\x1d.ondewo.nlu.ListUsersResponse\"\x11\x82\xd3\xe4\x93\x02\x0b\x12\t/v2/users\x12i\n\rListUserInfos\x12\x1c.ondewo.nlu.ListUsersRequest\x1a!.ondewo.nlu.ListUserInfosResponse\"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/v2/users_infos\x12l\n\x10\x43reateServerRole\x12#.ondewo.nlu.CreateServerRoleRequest\x1a\x16.ondewo.nlu.ServerRole\"\x1b\x82\xd3\xe4\x93\x02\x15\"\x10/v2/server_roles:\x01*\x12o\n\rGetServerRole\x12 .ondewo.nlu.GetServerRoleRequest\x1a\x16.ondewo.nlu.ServerRole\"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/v2/server_roles/{role_id=*}\x12u\n\x10\x44\x65leteServerRole\x12#.ondewo.nlu.DeleteServerRoleRequest\x1a\x16.google.protobuf.Empty\"$\x82\xd3\xe4\x93\x02\x1e*\x1c/v2/server_roles/{role_id=*}\x12l\n\x10UpdateServerRole\x12#.ondewo.nlu.UpdateServerRoleRequest\x1a\x16.ondewo.nlu.ServerRole\"\x1b\x82\xd3\xe4\x93\x02\x15\x32\x10/v2/server_roles:\x01*\x12t\n\x0fListServerRoles\x12\".ondewo.nlu.ListServerRolesRequest\x1a#.ondewo.nlu.ListServerRolesResponse\"\x18\x82\xd3\xe4\x93\x02\x12\x12\x10/v2/server_roles\x12\x8c\x01\n\x15ListServerPermissions\x12(.ondewo.nlu.ListServerPermissionsRequest\x1a).ondewo.nlu.ListServerPermissionsResponse\"\x1e\x82\xd3\xe4\x93\x02\x18\x12\x16/v2/server_permissions\x12R\n\x05Login\x12\x18.ondewo.nlu.LoginRequest\x1a\x19.ondewo.nlu.LoginResponse\"\x14\x82\xd3\xe4\x93\x02\x0e\"\t/v2/login:\x01*\x12U\n\nCheckLogin\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x17\x82\xd3\xe4\x93\x02\x11*\x0f/v2/check_loginb\x06proto3')

_DEFAULTSERVERROLE = DESCRIPTOR.enum_types_by_name['DefaultServerRole']
DefaultServerRole = enum_type_wrapper.EnumTypeWrapper(_DEFAULTSERVERROLE)
SERVER_UNSPECIFIED = 0
SERVER_USER = 1
SERVER_MANAGER = 2
SERVER_ADMIN = 3
SERVER_INACTIVE = 4


_USER = DESCRIPTOR.message_types_by_name['User']
_USERINFO = DESCRIPTOR.message_types_by_name['UserInfo']
_USERINFO_PROJECTROLESENTRY = _USERINFO.nested_types_by_name['ProjectRolesEntry']
_CREATEUSERREQUEST = DESCRIPTOR.message_types_by_name['CreateUserRequest']
_UPDATEUSERREQUEST = DESCRIPTOR.message_types_by_name['UpdateUserRequest']
_GETUSERREQUEST = DESCRIPTOR.message_types_by_name['GetUserRequest']
_DELETEUSERREQUEST = DESCRIPTOR.message_types_by_name['DeleteUserRequest']
_LISTUSERSREQUEST = DESCRIPTOR.message_types_by_name['ListUsersRequest']
_LISTUSERSRESPONSE = DESCRIPTOR.message_types_by_name['ListUsersResponse']
_LISTUSERINFOSRESPONSE = DESCRIPTOR.message_types_by_name['ListUserInfosResponse']
_SERVERROLE = DESCRIPTOR.message_types_by_name['ServerRole']
_CREATESERVERROLEREQUEST = DESCRIPTOR.message_types_by_name['CreateServerRoleRequest']
_UPDATESERVERROLEREQUEST = DESCRIPTOR.message_types_by_name['UpdateServerRoleRequest']
_DELETESERVERROLEREQUEST = DESCRIPTOR.message_types_by_name['DeleteServerRoleRequest']
_GETSERVERROLEREQUEST = DESCRIPTOR.message_types_by_name['GetServerRoleRequest']
_LISTSERVERROLESREQUEST = DESCRIPTOR.message_types_by_name['ListServerRolesRequest']
_LISTSERVERROLESRESPONSE = DESCRIPTOR.message_types_by_name['ListServerRolesResponse']
_LISTSERVERPERMISSIONSREQUEST = DESCRIPTOR.message_types_by_name['ListServerPermissionsRequest']
_LISTSERVERPERMISSIONSRESPONSE = DESCRIPTOR.message_types_by_name['ListServerPermissionsResponse']
_LOGINREQUEST = DESCRIPTOR.message_types_by_name['LoginRequest']
_LOGINRESPONSE = DESCRIPTOR.message_types_by_name['LoginResponse']
User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.User)
  })
_sym_db.RegisterMessage(User)

UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), {

  'ProjectRolesEntry' : _reflection.GeneratedProtocolMessageType('ProjectRolesEntry', (_message.Message,), {
    'DESCRIPTOR' : _USERINFO_PROJECTROLESENTRY,
    '__module__' : 'ondewo.nlu.user_pb2'
    # @@protoc_insertion_point(class_scope:ondewo.nlu.UserInfo.ProjectRolesEntry)
    })
  ,
  'DESCRIPTOR' : _USERINFO,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.UserInfo)
  })
_sym_db.RegisterMessage(UserInfo)
_sym_db.RegisterMessage(UserInfo.ProjectRolesEntry)

CreateUserRequest = _reflection.GeneratedProtocolMessageType('CreateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUSERREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.CreateUserRequest)
  })
_sym_db.RegisterMessage(CreateUserRequest)

UpdateUserRequest = _reflection.GeneratedProtocolMessageType('UpdateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.UpdateUserRequest)
  })
_sym_db.RegisterMessage(UpdateUserRequest)

GetUserRequest = _reflection.GeneratedProtocolMessageType('GetUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.GetUserRequest)
  })
_sym_db.RegisterMessage(GetUserRequest)

DeleteUserRequest = _reflection.GeneratedProtocolMessageType('DeleteUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEUSERREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.DeleteUserRequest)
  })
_sym_db.RegisterMessage(DeleteUserRequest)

ListUsersRequest = _reflection.GeneratedProtocolMessageType('ListUsersRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTUSERSREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListUsersRequest)
  })
_sym_db.RegisterMessage(ListUsersRequest)

ListUsersResponse = _reflection.GeneratedProtocolMessageType('ListUsersResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTUSERSRESPONSE,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListUsersResponse)
  })
_sym_db.RegisterMessage(ListUsersResponse)

ListUserInfosResponse = _reflection.GeneratedProtocolMessageType('ListUserInfosResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTUSERINFOSRESPONSE,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListUserInfosResponse)
  })
_sym_db.RegisterMessage(ListUserInfosResponse)

ServerRole = _reflection.GeneratedProtocolMessageType('ServerRole', (_message.Message,), {
  'DESCRIPTOR' : _SERVERROLE,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ServerRole)
  })
_sym_db.RegisterMessage(ServerRole)

CreateServerRoleRequest = _reflection.GeneratedProtocolMessageType('CreateServerRoleRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATESERVERROLEREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.CreateServerRoleRequest)
  })
_sym_db.RegisterMessage(CreateServerRoleRequest)

UpdateServerRoleRequest = _reflection.GeneratedProtocolMessageType('UpdateServerRoleRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATESERVERROLEREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.UpdateServerRoleRequest)
  })
_sym_db.RegisterMessage(UpdateServerRoleRequest)

DeleteServerRoleRequest = _reflection.GeneratedProtocolMessageType('DeleteServerRoleRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETESERVERROLEREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.DeleteServerRoleRequest)
  })
_sym_db.RegisterMessage(DeleteServerRoleRequest)

GetServerRoleRequest = _reflection.GeneratedProtocolMessageType('GetServerRoleRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSERVERROLEREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.GetServerRoleRequest)
  })
_sym_db.RegisterMessage(GetServerRoleRequest)

ListServerRolesRequest = _reflection.GeneratedProtocolMessageType('ListServerRolesRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTSERVERROLESREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListServerRolesRequest)
  })
_sym_db.RegisterMessage(ListServerRolesRequest)

ListServerRolesResponse = _reflection.GeneratedProtocolMessageType('ListServerRolesResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSERVERROLESRESPONSE,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListServerRolesResponse)
  })
_sym_db.RegisterMessage(ListServerRolesResponse)

ListServerPermissionsRequest = _reflection.GeneratedProtocolMessageType('ListServerPermissionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTSERVERPERMISSIONSREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListServerPermissionsRequest)
  })
_sym_db.RegisterMessage(ListServerPermissionsRequest)

ListServerPermissionsResponse = _reflection.GeneratedProtocolMessageType('ListServerPermissionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSERVERPERMISSIONSRESPONSE,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListServerPermissionsResponse)
  })
_sym_db.RegisterMessage(ListServerPermissionsResponse)

LoginRequest = _reflection.GeneratedProtocolMessageType('LoginRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOGINREQUEST,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.LoginRequest)
  })
_sym_db.RegisterMessage(LoginRequest)

LoginResponse = _reflection.GeneratedProtocolMessageType('LoginResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOGINRESPONSE,
  '__module__' : 'ondewo.nlu.user_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.LoginResponse)
  })
_sym_db.RegisterMessage(LoginResponse)

_USERS = DESCRIPTOR.services_by_name['Users']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERINFO_PROJECTROLESENTRY._options = None
  _USERINFO_PROJECTROLESENTRY._serialized_options = b'8\001'
  _USERS.methods_by_name['CreateUser']._options = None
  _USERS.methods_by_name['CreateUser']._serialized_options = b'\202\323\344\223\002\016\"\t/v2/users:\001*'
  _USERS.methods_by_name['GetUser']._options = None
  _USERS.methods_by_name['GetUser']._serialized_options = b'\202\323\344\223\002\037\022\035/v2/users/{user_identifier=*}'
  _USERS.methods_by_name['GetUserInfo']._options = None
  _USERS.methods_by_name['GetUserInfo']._serialized_options = b'\202\323\344\223\002$\022\"/v2/user_infos/{user_identifier=*}'
  _USERS.methods_by_name['DeleteUser']._options = None
  _USERS.methods_by_name['DeleteUser']._serialized_options = b'\202\323\344\223\002\037*\035/v2/users/{user_identifier=*}'
  _USERS.methods_by_name['UpdateUser']._options = None
  _USERS.methods_by_name['UpdateUser']._serialized_options = b'\202\323\344\223\002\0162\t/v2/users:\001*'
  _USERS.methods_by_name['ListUsers']._options = None
  _USERS.methods_by_name['ListUsers']._serialized_options = b'\202\323\344\223\002\013\022\t/v2/users'
  _USERS.methods_by_name['ListUserInfos']._options = None
  _USERS.methods_by_name['ListUserInfos']._serialized_options = b'\202\323\344\223\002\021\022\017/v2/users_infos'
  _USERS.methods_by_name['CreateServerRole']._options = None
  _USERS.methods_by_name['CreateServerRole']._serialized_options = b'\202\323\344\223\002\025\"\020/v2/server_roles:\001*'
  _USERS.methods_by_name['GetServerRole']._options = None
  _USERS.methods_by_name['GetServerRole']._serialized_options = b'\202\323\344\223\002\036\022\034/v2/server_roles/{role_id=*}'
  _USERS.methods_by_name['DeleteServerRole']._options = None
  _USERS.methods_by_name['DeleteServerRole']._serialized_options = b'\202\323\344\223\002\036*\034/v2/server_roles/{role_id=*}'
  _USERS.methods_by_name['UpdateServerRole']._options = None
  _USERS.methods_by_name['UpdateServerRole']._serialized_options = b'\202\323\344\223\002\0252\020/v2/server_roles:\001*'
  _USERS.methods_by_name['ListServerRoles']._options = None
  _USERS.methods_by_name['ListServerRoles']._serialized_options = b'\202\323\344\223\002\022\022\020/v2/server_roles'
  _USERS.methods_by_name['ListServerPermissions']._options = None
  _USERS.methods_by_name['ListServerPermissions']._serialized_options = b'\202\323\344\223\002\030\022\026/v2/server_permissions'
  _USERS.methods_by_name['Login']._options = None
  _USERS.methods_by_name['Login']._serialized_options = b'\202\323\344\223\002\016\"\t/v2/login:\001*'
  _USERS.methods_by_name['CheckLogin']._options = None
  _USERS.methods_by_name['CheckLogin']._serialized_options = b'\202\323\344\223\002\021*\017/v2/check_login'
  _DEFAULTSERVERROLE._serialized_start=1728
  _DEFAULTSERVERROLE._serialized_end=1847
  _USER._serialized_start=161
  _USER._serialized_end=250
  _USERINFO._serialized_start=253
  _USERINFO._serialized_end=436
  _USERINFO_PROJECTROLESENTRY._serialized_start=360
  _USERINFO_PROJECTROLESENTRY._serialized_end=436
  _CREATEUSERREQUEST._serialized_start=438
  _CREATEUSERREQUEST._serialized_end=507
  _UPDATEUSERREQUEST._serialized_start=509
  _UPDATEUSERREQUEST._serialized_end=627
  _GETUSERREQUEST._serialized_start=629
  _GETUSERREQUEST._serialized_end=705
  _DELETEUSERREQUEST._serialized_start=707
  _DELETEUSERREQUEST._serialized_end=743
  _LISTUSERSREQUEST._serialized_start=745
  _LISTUSERSREQUEST._serialized_end=783
  _LISTUSERSRESPONSE._serialized_start=785
  _LISTUSERSRESPONSE._serialized_end=862
  _LISTUSERINFOSRESPONSE._serialized_start=864
  _LISTUSERINFOSRESPONSE._serialized_end=949
  _SERVERROLE._serialized_start=951
  _SERVERROLE._serialized_end=1015
  _CREATESERVERROLEREQUEST._serialized_start=1017
  _CREATESERVERROLEREQUEST._serialized_end=1080
  _UPDATESERVERROLEREQUEST._serialized_start=1082
  _UPDATESERVERROLEREQUEST._serialized_end=1194
  _DELETESERVERROLEREQUEST._serialized_start=1196
  _DELETESERVERROLEREQUEST._serialized_end=1238
  _GETSERVERROLEREQUEST._serialized_start=1240
  _GETSERVERROLEREQUEST._serialized_end=1328
  _LISTSERVERROLESREQUEST._serialized_start=1330
  _LISTSERVERROLESREQUEST._serialized_end=1374
  _LISTSERVERROLESRESPONSE._serialized_start=1376
  _LISTSERVERROLESRESPONSE._serialized_end=1472
  _LISTSERVERPERMISSIONSREQUEST._serialized_start=1474
  _LISTSERVERPERMISSIONSREQUEST._serialized_end=1524
  _LISTSERVERPERMISSIONSRESPONSE._serialized_start=1526
  _LISTSERVERPERMISSIONSRESPONSE._serialized_end=1603
  _LOGINREQUEST._serialized_start=1605
  _LOGINREQUEST._serialized_end=1657
  _LOGINRESPONSE._serialized_start=1659
  _LOGINRESPONSE._serialized_end=1726
  _USERS._serialized_start=1850
  _USERS._serialized_end=3421
# @@protoc_insertion_point(module_scope)
