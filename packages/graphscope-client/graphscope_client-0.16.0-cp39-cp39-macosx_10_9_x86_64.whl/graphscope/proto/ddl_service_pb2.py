# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: graphscope/proto/ddl_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from graphscope.proto import graph_def_pb2 as graphscope_dot_proto_dot_graph__def__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"graphscope/proto/ddl_service.proto\x12\x15gs.rpc.ddl_service.v1\x1a graphscope/proto/graph_def.proto\"\x88\x05\n\x12\x42\x61tchSubmitRequest\x12\x16\n\x0e\x66ormat_version\x18\x01 \x01(\x05\x12\x17\n\x0fsimple_response\x18\x02 \x01(\x08\x12\x43\n\x05value\x18\x03 \x03(\x0b\x32\x34.gs.rpc.ddl_service.v1.BatchSubmitRequest.DDLRequest\x1a\xfb\x03\n\nDDLRequest\x12T\n\x1a\x63reate_vertex_type_request\x18\x01 \x01(\x0b\x32..gs.rpc.ddl_service.v1.CreateVertexTypeRequestH\x00\x12P\n\x18\x63reate_edge_type_request\x18\x02 \x01(\x0b\x32,.gs.rpc.ddl_service.v1.CreateEdgeTypeRequestH\x00\x12J\n\x15\x61\x64\x64_edge_kind_request\x18\x03 \x01(\x0b\x32).gs.rpc.ddl_service.v1.AddEdgeKindRequestH\x00\x12P\n\x18remove_edge_kind_request\x18\x04 \x01(\x0b\x32,.gs.rpc.ddl_service.v1.RemoveEdgeKindRequestH\x00\x12P\n\x18\x64rop_vertex_type_request\x18\x05 \x01(\x0b\x32,.gs.rpc.ddl_service.v1.DropVertexTypeRequestH\x00\x12L\n\x16\x64rop_edge_type_request\x18\x06 \x01(\x0b\x32*.gs.rpc.ddl_service.v1.DropEdgeTypeRequestH\x00\x42\x07\n\x05value\"Z\n\x13\x42\x61tchSubmitResponse\x12\x16\n\x0e\x66ormat_version\x18\x01 \x01(\x05\x12+\n\tgraph_def\x18\x02 \x01(\x0b\x32\x18.gs.rpc.graph.GraphDefPb\"D\n\x17\x43reateVertexTypeRequest\x12)\n\x08type_def\x18\x01 \x01(\x0b\x32\x17.gs.rpc.graph.TypeDefPb\"B\n\x15\x43reateEdgeTypeRequest\x12)\n\x08type_def\x18\x01 \x01(\x0b\x32\x17.gs.rpc.graph.TypeDefPb\"\\\n\x12\x41\x64\x64\x45\x64geKindRequest\x12\x12\n\nedge_label\x18\x01 \x01(\t\x12\x18\n\x10src_vertex_label\x18\x02 \x01(\t\x12\x18\n\x10\x64st_vertex_label\x18\x03 \x01(\t\"_\n\x15RemoveEdgeKindRequest\x12\x12\n\nedge_label\x18\x01 \x01(\t\x12\x18\n\x10src_vertex_label\x18\x02 \x01(\t\x12\x18\n\x10\x64st_vertex_label\x18\x03 \x01(\t\"&\n\x15\x44ropVertexTypeRequest\x12\r\n\x05label\x18\x01 \x01(\t\"$\n\x13\x44ropEdgeTypeRequest\x12\r\n\x05label\x18\x01 \x01(\t\"!\n\x12GetGraphDefRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"B\n\x13GetGraphDefResponse\x12+\n\tgraph_def\x18\x01 \x01(\x0b\x32\x18.gs.rpc.graph.GraphDefPb2\xd7\x01\n\tClientDdl\x12\x64\n\x0b\x62\x61tchSubmit\x12).gs.rpc.ddl_service.v1.BatchSubmitRequest\x1a*.gs.rpc.ddl_service.v1.BatchSubmitResponse\x12\x64\n\x0bgetGraphDef\x12).gs.rpc.ddl_service.v1.GetGraphDefRequest\x1a*.gs.rpc.ddl_service.v1.GetGraphDefResponseB$\n com.alibaba.graphscope.proto.ddlP\x01\x62\x06proto3')



_BATCHSUBMITREQUEST = DESCRIPTOR.message_types_by_name['BatchSubmitRequest']
_BATCHSUBMITREQUEST_DDLREQUEST = _BATCHSUBMITREQUEST.nested_types_by_name['DDLRequest']
_BATCHSUBMITRESPONSE = DESCRIPTOR.message_types_by_name['BatchSubmitResponse']
_CREATEVERTEXTYPEREQUEST = DESCRIPTOR.message_types_by_name['CreateVertexTypeRequest']
_CREATEEDGETYPEREQUEST = DESCRIPTOR.message_types_by_name['CreateEdgeTypeRequest']
_ADDEDGEKINDREQUEST = DESCRIPTOR.message_types_by_name['AddEdgeKindRequest']
_REMOVEEDGEKINDREQUEST = DESCRIPTOR.message_types_by_name['RemoveEdgeKindRequest']
_DROPVERTEXTYPEREQUEST = DESCRIPTOR.message_types_by_name['DropVertexTypeRequest']
_DROPEDGETYPEREQUEST = DESCRIPTOR.message_types_by_name['DropEdgeTypeRequest']
_GETGRAPHDEFREQUEST = DESCRIPTOR.message_types_by_name['GetGraphDefRequest']
_GETGRAPHDEFRESPONSE = DESCRIPTOR.message_types_by_name['GetGraphDefResponse']
BatchSubmitRequest = _reflection.GeneratedProtocolMessageType('BatchSubmitRequest', (_message.Message,), {

  'DDLRequest' : _reflection.GeneratedProtocolMessageType('DDLRequest', (_message.Message,), {
    'DESCRIPTOR' : _BATCHSUBMITREQUEST_DDLREQUEST,
    '__module__' : 'graphscope.proto.ddl_service_pb2'
    # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.BatchSubmitRequest.DDLRequest)
    })
  ,
  'DESCRIPTOR' : _BATCHSUBMITREQUEST,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.BatchSubmitRequest)
  })
_sym_db.RegisterMessage(BatchSubmitRequest)
_sym_db.RegisterMessage(BatchSubmitRequest.DDLRequest)

BatchSubmitResponse = _reflection.GeneratedProtocolMessageType('BatchSubmitResponse', (_message.Message,), {
  'DESCRIPTOR' : _BATCHSUBMITRESPONSE,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.BatchSubmitResponse)
  })
_sym_db.RegisterMessage(BatchSubmitResponse)

CreateVertexTypeRequest = _reflection.GeneratedProtocolMessageType('CreateVertexTypeRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEVERTEXTYPEREQUEST,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.CreateVertexTypeRequest)
  })
_sym_db.RegisterMessage(CreateVertexTypeRequest)

CreateEdgeTypeRequest = _reflection.GeneratedProtocolMessageType('CreateEdgeTypeRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEEDGETYPEREQUEST,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.CreateEdgeTypeRequest)
  })
_sym_db.RegisterMessage(CreateEdgeTypeRequest)

AddEdgeKindRequest = _reflection.GeneratedProtocolMessageType('AddEdgeKindRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDEDGEKINDREQUEST,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.AddEdgeKindRequest)
  })
_sym_db.RegisterMessage(AddEdgeKindRequest)

RemoveEdgeKindRequest = _reflection.GeneratedProtocolMessageType('RemoveEdgeKindRequest', (_message.Message,), {
  'DESCRIPTOR' : _REMOVEEDGEKINDREQUEST,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.RemoveEdgeKindRequest)
  })
_sym_db.RegisterMessage(RemoveEdgeKindRequest)

DropVertexTypeRequest = _reflection.GeneratedProtocolMessageType('DropVertexTypeRequest', (_message.Message,), {
  'DESCRIPTOR' : _DROPVERTEXTYPEREQUEST,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.DropVertexTypeRequest)
  })
_sym_db.RegisterMessage(DropVertexTypeRequest)

DropEdgeTypeRequest = _reflection.GeneratedProtocolMessageType('DropEdgeTypeRequest', (_message.Message,), {
  'DESCRIPTOR' : _DROPEDGETYPEREQUEST,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.DropEdgeTypeRequest)
  })
_sym_db.RegisterMessage(DropEdgeTypeRequest)

GetGraphDefRequest = _reflection.GeneratedProtocolMessageType('GetGraphDefRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETGRAPHDEFREQUEST,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.GetGraphDefRequest)
  })
_sym_db.RegisterMessage(GetGraphDefRequest)

GetGraphDefResponse = _reflection.GeneratedProtocolMessageType('GetGraphDefResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETGRAPHDEFRESPONSE,
  '__module__' : 'graphscope.proto.ddl_service_pb2'
  # @@protoc_insertion_point(class_scope:gs.rpc.ddl_service.v1.GetGraphDefResponse)
  })
_sym_db.RegisterMessage(GetGraphDefResponse)

_CLIENTDDL = DESCRIPTOR.services_by_name['ClientDdl']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n com.alibaba.graphscope.proto.ddlP\001'
  _BATCHSUBMITREQUEST._serialized_start=96
  _BATCHSUBMITREQUEST._serialized_end=744
  _BATCHSUBMITREQUEST_DDLREQUEST._serialized_start=237
  _BATCHSUBMITREQUEST_DDLREQUEST._serialized_end=744
  _BATCHSUBMITRESPONSE._serialized_start=746
  _BATCHSUBMITRESPONSE._serialized_end=836
  _CREATEVERTEXTYPEREQUEST._serialized_start=838
  _CREATEVERTEXTYPEREQUEST._serialized_end=906
  _CREATEEDGETYPEREQUEST._serialized_start=908
  _CREATEEDGETYPEREQUEST._serialized_end=974
  _ADDEDGEKINDREQUEST._serialized_start=976
  _ADDEDGEKINDREQUEST._serialized_end=1068
  _REMOVEEDGEKINDREQUEST._serialized_start=1070
  _REMOVEEDGEKINDREQUEST._serialized_end=1165
  _DROPVERTEXTYPEREQUEST._serialized_start=1167
  _DROPVERTEXTYPEREQUEST._serialized_end=1205
  _DROPEDGETYPEREQUEST._serialized_start=1207
  _DROPEDGETYPEREQUEST._serialized_end=1243
  _GETGRAPHDEFREQUEST._serialized_start=1245
  _GETGRAPHDEFREQUEST._serialized_end=1278
  _GETGRAPHDEFRESPONSE._serialized_start=1280
  _GETGRAPHDEFRESPONSE._serialized_end=1346
  _CLIENTDDL._serialized_start=1349
  _CLIENTDDL._serialized_end=1564
# @@protoc_insertion_point(module_scope)
