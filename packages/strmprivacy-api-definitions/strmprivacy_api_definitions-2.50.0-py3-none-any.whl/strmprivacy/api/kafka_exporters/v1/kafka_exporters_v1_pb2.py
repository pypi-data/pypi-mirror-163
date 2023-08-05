# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: strmprivacy/api/kafka_exporters/v1/kafka_exporters_v1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from strmprivacy.api.entities.v1 import entities_v1_pb2 as strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;strmprivacy/api/kafka_exporters/v1/kafka_exporters_v1.proto\x12\"strmprivacy.api.kafka_exporters.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a-strmprivacy/api/entities/v1/entities_v1.proto\"L\n\x19ListKafkaExportersRequest\x12\x16\n\nbilling_id\x18\x01 \x01(\tB\x02\x18\x01\x12\x17\n\nproject_id\x18\x02 \x01(\tB\x03\xe0\x41\x03\"a\n\x1aListKafkaExportersResponse\x12\x43\n\x0fkafka_exporters\x18\x01 \x03(\x0b\x32*.strmprivacy.api.entities.v1.KafkaExporter\"u\n\x1a\x44\x65leteKafkaExporterRequest\x12?\n\x03ref\x18\x01 \x01(\x0b\x32-.strmprivacy.api.entities.v1.KafkaExporterRefB\x03\xe0\x41\x02\x12\x16\n\trecursive\x18\x02 \x01(\x08\x42\x03\xe0\x41\x02\"\x1d\n\x1b\x44\x65leteKafkaExporterResponse\"e\n\x1a\x43reateKafkaExporterRequest\x12G\n\x0ekafka_exporter\x18\x01 \x01(\x0b\x32*.strmprivacy.api.entities.v1.KafkaExporterB\x03\xe0\x41\x02\"a\n\x1b\x43reateKafkaExporterResponse\x12\x42\n\x0ekafka_exporter\x18\x01 \x01(\x0b\x32*.strmprivacy.api.entities.v1.KafkaExporter\"Z\n\x17GetKafkaExporterRequest\x12?\n\x03ref\x18\x01 \x01(\x0b\x32-.strmprivacy.api.entities.v1.KafkaExporterRefB\x03\xe0\x41\x02\"^\n\x18GetKafkaExporterResponse\x12\x42\n\x0ekafka_exporter\x18\x01 \x01(\x0b\x32*.strmprivacy.api.entities.v1.KafkaExporter2\xef\x04\n\x15KafkaExportersService\x12\x93\x01\n\x12ListKafkaExporters\x12=.strmprivacy.api.kafka_exporters.v1.ListKafkaExportersRequest\x1a>.strmprivacy.api.kafka_exporters.v1.ListKafkaExportersResponse\x12\x8d\x01\n\x10GetKafkaExporter\x12;.strmprivacy.api.kafka_exporters.v1.GetKafkaExporterRequest\x1a<.strmprivacy.api.kafka_exporters.v1.GetKafkaExporterResponse\x12\x96\x01\n\x13\x44\x65leteKafkaExporter\x12>.strmprivacy.api.kafka_exporters.v1.DeleteKafkaExporterRequest\x1a?.strmprivacy.api.kafka_exporters.v1.DeleteKafkaExporterResponse\x12\x96\x01\n\x13\x43reateKafkaExporter\x12>.strmprivacy.api.kafka_exporters.v1.CreateKafkaExporterRequest\x1a?.strmprivacy.api.kafka_exporters.v1.CreateKafkaExporterResponseB~\n%io.strmprivacy.api.kafka_exporters.v1P\x01ZSgithub.com/strmprivacy/api-definitions-go/v2/api/kafka_exporters/v1;kafka_exportersb\x06proto3')



_LISTKAFKAEXPORTERSREQUEST = DESCRIPTOR.message_types_by_name['ListKafkaExportersRequest']
_LISTKAFKAEXPORTERSRESPONSE = DESCRIPTOR.message_types_by_name['ListKafkaExportersResponse']
_DELETEKAFKAEXPORTERREQUEST = DESCRIPTOR.message_types_by_name['DeleteKafkaExporterRequest']
_DELETEKAFKAEXPORTERRESPONSE = DESCRIPTOR.message_types_by_name['DeleteKafkaExporterResponse']
_CREATEKAFKAEXPORTERREQUEST = DESCRIPTOR.message_types_by_name['CreateKafkaExporterRequest']
_CREATEKAFKAEXPORTERRESPONSE = DESCRIPTOR.message_types_by_name['CreateKafkaExporterResponse']
_GETKAFKAEXPORTERREQUEST = DESCRIPTOR.message_types_by_name['GetKafkaExporterRequest']
_GETKAFKAEXPORTERRESPONSE = DESCRIPTOR.message_types_by_name['GetKafkaExporterResponse']
ListKafkaExportersRequest = _reflection.GeneratedProtocolMessageType('ListKafkaExportersRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTKAFKAEXPORTERSREQUEST,
  '__module__' : 'strmprivacy.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.kafka_exporters.v1.ListKafkaExportersRequest)
  })
_sym_db.RegisterMessage(ListKafkaExportersRequest)

ListKafkaExportersResponse = _reflection.GeneratedProtocolMessageType('ListKafkaExportersResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTKAFKAEXPORTERSRESPONSE,
  '__module__' : 'strmprivacy.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.kafka_exporters.v1.ListKafkaExportersResponse)
  })
_sym_db.RegisterMessage(ListKafkaExportersResponse)

DeleteKafkaExporterRequest = _reflection.GeneratedProtocolMessageType('DeleteKafkaExporterRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEKAFKAEXPORTERREQUEST,
  '__module__' : 'strmprivacy.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.kafka_exporters.v1.DeleteKafkaExporterRequest)
  })
_sym_db.RegisterMessage(DeleteKafkaExporterRequest)

DeleteKafkaExporterResponse = _reflection.GeneratedProtocolMessageType('DeleteKafkaExporterResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEKAFKAEXPORTERRESPONSE,
  '__module__' : 'strmprivacy.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.kafka_exporters.v1.DeleteKafkaExporterResponse)
  })
_sym_db.RegisterMessage(DeleteKafkaExporterResponse)

CreateKafkaExporterRequest = _reflection.GeneratedProtocolMessageType('CreateKafkaExporterRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEKAFKAEXPORTERREQUEST,
  '__module__' : 'strmprivacy.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.kafka_exporters.v1.CreateKafkaExporterRequest)
  })
_sym_db.RegisterMessage(CreateKafkaExporterRequest)

CreateKafkaExporterResponse = _reflection.GeneratedProtocolMessageType('CreateKafkaExporterResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEKAFKAEXPORTERRESPONSE,
  '__module__' : 'strmprivacy.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.kafka_exporters.v1.CreateKafkaExporterResponse)
  })
_sym_db.RegisterMessage(CreateKafkaExporterResponse)

GetKafkaExporterRequest = _reflection.GeneratedProtocolMessageType('GetKafkaExporterRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETKAFKAEXPORTERREQUEST,
  '__module__' : 'strmprivacy.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.kafka_exporters.v1.GetKafkaExporterRequest)
  })
_sym_db.RegisterMessage(GetKafkaExporterRequest)

GetKafkaExporterResponse = _reflection.GeneratedProtocolMessageType('GetKafkaExporterResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETKAFKAEXPORTERRESPONSE,
  '__module__' : 'strmprivacy.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.kafka_exporters.v1.GetKafkaExporterResponse)
  })
_sym_db.RegisterMessage(GetKafkaExporterResponse)

_KAFKAEXPORTERSSERVICE = DESCRIPTOR.services_by_name['KafkaExportersService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%io.strmprivacy.api.kafka_exporters.v1P\001ZSgithub.com/strmprivacy/api-definitions-go/v2/api/kafka_exporters/v1;kafka_exporters'
  _LISTKAFKAEXPORTERSREQUEST.fields_by_name['billing_id']._options = None
  _LISTKAFKAEXPORTERSREQUEST.fields_by_name['billing_id']._serialized_options = b'\030\001'
  _LISTKAFKAEXPORTERSREQUEST.fields_by_name['project_id']._options = None
  _LISTKAFKAEXPORTERSREQUEST.fields_by_name['project_id']._serialized_options = b'\340A\003'
  _DELETEKAFKAEXPORTERREQUEST.fields_by_name['ref']._options = None
  _DELETEKAFKAEXPORTERREQUEST.fields_by_name['ref']._serialized_options = b'\340A\002'
  _DELETEKAFKAEXPORTERREQUEST.fields_by_name['recursive']._options = None
  _DELETEKAFKAEXPORTERREQUEST.fields_by_name['recursive']._serialized_options = b'\340A\002'
  _CREATEKAFKAEXPORTERREQUEST.fields_by_name['kafka_exporter']._options = None
  _CREATEKAFKAEXPORTERREQUEST.fields_by_name['kafka_exporter']._serialized_options = b'\340A\002'
  _GETKAFKAEXPORTERREQUEST.fields_by_name['ref']._options = None
  _GETKAFKAEXPORTERREQUEST.fields_by_name['ref']._serialized_options = b'\340A\002'
  _LISTKAFKAEXPORTERSREQUEST._serialized_start=179
  _LISTKAFKAEXPORTERSREQUEST._serialized_end=255
  _LISTKAFKAEXPORTERSRESPONSE._serialized_start=257
  _LISTKAFKAEXPORTERSRESPONSE._serialized_end=354
  _DELETEKAFKAEXPORTERREQUEST._serialized_start=356
  _DELETEKAFKAEXPORTERREQUEST._serialized_end=473
  _DELETEKAFKAEXPORTERRESPONSE._serialized_start=475
  _DELETEKAFKAEXPORTERRESPONSE._serialized_end=504
  _CREATEKAFKAEXPORTERREQUEST._serialized_start=506
  _CREATEKAFKAEXPORTERREQUEST._serialized_end=607
  _CREATEKAFKAEXPORTERRESPONSE._serialized_start=609
  _CREATEKAFKAEXPORTERRESPONSE._serialized_end=706
  _GETKAFKAEXPORTERREQUEST._serialized_start=708
  _GETKAFKAEXPORTERREQUEST._serialized_end=798
  _GETKAFKAEXPORTERRESPONSE._serialized_start=800
  _GETKAFKAEXPORTERRESPONSE._serialized_end=894
  _KAFKAEXPORTERSSERVICE._serialized_start=897
  _KAFKAEXPORTERSSERVICE._serialized_end=1520
# @@protoc_insertion_point(module_scope)
