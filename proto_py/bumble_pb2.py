# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bumble.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x62umble.proto\"L\n\rrequest_proto\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\x0e\n\x06is_enc\x18\x02 \x01(\x08\x12\r\n\x05nonce\x18\x03 \x01(\x0c\x12\x0c\n\x04\x62ody\x18\x04 \x01(\x0c\"P\n\x0eresponse_proto\x12\x0e\n\x06is_enc\x18\x01 \x01(\x08\x12\r\n\x05nonce\x18\x02 \x01(\x0c\x12\x0c\n\x04\x62ody\x18\x03 \x01(\x0c\x12\x11\n\tsignature\x18\x04 \x01(\x0c\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bumble_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST_PROTO._serialized_start=16
  _REQUEST_PROTO._serialized_end=92
  _RESPONSE_PROTO._serialized_start=94
  _RESPONSE_PROTO._serialized_end=174
# @@protoc_insertion_point(module_scope)