# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bookstore.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x62ookstore.proto\x12\tbookstore\"(\n\x13SetSuccessorRequest\x12\x11\n\tsuccessor\x18\x01 \x01(\x05\"\'\n\x14SetSuccessorResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\",\n\x12SetHeadNodeRequest\x12\x16\n\x0ehead_node_port\x18\x01 \x01(\x05\"&\n\x13SetHeadNodeResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x14\n\x12\x44\x65\x63lareHeadRequest\"&\n\x13\x44\x65\x63lareHeadResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x14\n\x12\x44\x65\x63lareTailRequest\"&\n\x13\x44\x65\x63lareTailResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x12\n\x10UnsetHeadRequest\"$\n\x11UnsetHeadResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x12\n\x10UnsetTailRequest\"$\n\x11UnsetTailResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x13\n\x11\x44\x65leteDataRequest\"%\n\x12\x44\x65leteDataResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"(\n\x13\x43onfirmWriteRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\"\'\n\x14\x43onfirmWriteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"9\n\x15WriteOperationRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x01\"K\n\x16WriteOperationResponse\x12\x11\n\tbook_name\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x0f\n\x07success\x18\x03 \x01(\x08\"?\n\x17UpdateDataStatusRequest\x12\x12\n\nbook_names\x18\x01 \x03(\t\x12\x10\n\x08statuses\x18\x02 \x03(\t\"+\n\x18UpdateDataStatusResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\".\n\x19\x43onfirmTransactionRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\"-\n\x1a\x43onfirmTransactionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\'\n\x12\x43onfirmReadRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\"&\n\x13\x43onfirmReadResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\")\n\x14ReadOperationRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\"&\n\x15ReadOperationResponse\x12\r\n\x05price\x18\x01 \x01(\x01\"\x16\n\x14ListOperationRequest\"&\n\x15ListOperationResponse\x12\r\n\x05\x62ooks\x18\x01 \x03(\t\"\x13\n\x11\x44\x61taStatusRequest\")\n\x12\x44\x61taStatusResponse\x12\x13\n\x0b\x64\x61ta_status\x18\x01 \x03(\t\"$\n\x11SetTimeoutRequest\x12\x0f\n\x07timeout\x18\x01 \x01(\r\"%\n\x12SetTimeoutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\" \n\x13LocalStorePsRequest\x12\t\n\x01k\x18\x01 \x01(\r\"\'\n\x14LocalStorePsResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x14\n\x12\x43reateChainRequest\"7\n\x13\x43reateChainResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x12\n\x10ListChainRequest\"\"\n\x11ListChainResponse\x12\r\n\x05\x63hain\x18\x01 \x01(\t\"\x12\n\x10ListBooksRequest\"3\n\x11ListBooksResponse\x12\x1e\n\x05\x62ooks\x18\x01 \x03(\x0b\x32\x0f.bookstore.Book\"#\n\x04\x42ook\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x01\"0\n\x0e\x44\x61taItemStatus\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08is_dirty\x18\x02 \x01(\x08\"\x14\n\x12RestoreHeadRequest\"7\n\x13RestoreHeadResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1b\n\x19GetLocalDataStoresRequest\"1\n\x1aGetLocalDataStoresResponse\x12\x13\n\x0b\x64\x61ta_stores\x18\x01 \x03(\x05\" \n\x0fSetChainRequest\x12\r\n\x05\x63hain\x18\x01 \x03(\x05\"#\n\x10SetChainResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\x95\n\n\tDataStore\x12O\n\x0cSetSuccessor\x12\x1e.bookstore.SetSuccessorRequest\x1a\x1f.bookstore.SetSuccessorResponse\x12L\n\x0bSetHeadNode\x12\x1d.bookstore.SetHeadNodeRequest\x1a\x1e.bookstore.SetHeadNodeResponse\x12L\n\x0b\x44\x65\x63lareHead\x12\x1d.bookstore.DeclareHeadRequest\x1a\x1e.bookstore.DeclareHeadResponse\x12L\n\x0b\x44\x65\x63lareTail\x12\x1d.bookstore.DeclareTailRequest\x1a\x1e.bookstore.DeclareTailResponse\x12\x46\n\tUnsetHead\x12\x1b.bookstore.UnsetHeadRequest\x1a\x1c.bookstore.UnsetHeadResponse\x12\x46\n\tUnsetTail\x12\x1b.bookstore.UnsetHeadRequest\x1a\x1c.bookstore.UnsetHeadResponse\x12I\n\nDeleteData\x12\x1c.bookstore.DeleteDataRequest\x1a\x1d.bookstore.DeleteDataResponse\x12O\n\x0c\x43onfirmWrite\x12\x1e.bookstore.ConfirmWriteRequest\x1a\x1f.bookstore.ConfirmWriteResponse\x12U\n\x0eWriteOperation\x12 .bookstore.WriteOperationRequest\x1a!.bookstore.WriteOperationResponse\x12[\n\x10UpdateDataStatus\x12\".bookstore.UpdateDataStatusRequest\x1a#.bookstore.UpdateDataStatusResponse\x12\x61\n\x12\x43onfirmTransaction\x12$.bookstore.ConfirmTransactionRequest\x1a%.bookstore.ConfirmTransactionResponse\x12L\n\x0b\x43onfirmRead\x12\x1d.bookstore.ConfirmReadRequest\x1a\x1e.bookstore.ConfirmReadResponse\x12R\n\rReadOperation\x12\x1f.bookstore.ReadOperationRequest\x1a .bookstore.ReadOperationResponse\x12R\n\rListOperation\x12\x1f.bookstore.ListOperationRequest\x1a .bookstore.ListOperationResponse\x12I\n\nDataStatus\x12\x1c.bookstore.DataStatusRequest\x1a\x1d.bookstore.DataStatusResponse\x12I\n\nSetTimeout\x12\x1c.bookstore.SetTimeoutRequest\x1a\x1d.bookstore.SetTimeoutResponse2\x90\x08\n\tBookStore\x12O\n\x0cLocalStorePs\x12\x1e.bookstore.LocalStorePsRequest\x1a\x1f.bookstore.LocalStorePsResponse\x12L\n\x0b\x43reateChain\x12\x1d.bookstore.CreateChainRequest\x1a\x1e.bookstore.CreateChainResponse\x12L\n\x0bRemoveChain\x12\x1d.bookstore.CreateChainRequest\x1a\x1e.bookstore.CreateChainResponse\x12\x46\n\tListChain\x12\x1b.bookstore.ListChainRequest\x1a\x1c.bookstore.ListChainResponse\x12U\n\x0eWriteOperation\x12 .bookstore.WriteOperationRequest\x1a!.bookstore.WriteOperationResponse\x12N\n\tListBooks\x12\x1f.bookstore.ListOperationRequest\x1a .bookstore.ListOperationResponse\x12R\n\rReadOperation\x12\x1f.bookstore.ReadOperationRequest\x1a .bookstore.ReadOperationResponse\x12I\n\nSetTimeout\x12\x1c.bookstore.SetTimeoutRequest\x1a\x1d.bookstore.SetTimeoutResponse\x12I\n\nDataStatus\x12\x1c.bookstore.DataStatusRequest\x1a\x1d.bookstore.DataStatusResponse\x12G\n\nRemoveHead\x12\x1b.bookstore.ListChainRequest\x1a\x1c.bookstore.ListChainResponse\x12L\n\x0bRestoreHead\x12\x1d.bookstore.RestoreHeadRequest\x1a\x1e.bookstore.RestoreHeadResponse\x12\x61\n\x12GetLocalDataStores\x12$.bookstore.GetLocalDataStoresRequest\x1a%.bookstore.GetLocalDataStoresResponse\x12\x43\n\x08SetChain\x12\x1a.bookstore.SetChainRequest\x1a\x1b.bookstore.SetChainResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bookstore_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SETSUCCESSORREQUEST._serialized_start=30
  _SETSUCCESSORREQUEST._serialized_end=70
  _SETSUCCESSORRESPONSE._serialized_start=72
  _SETSUCCESSORRESPONSE._serialized_end=111
  _SETHEADNODEREQUEST._serialized_start=113
  _SETHEADNODEREQUEST._serialized_end=157
  _SETHEADNODERESPONSE._serialized_start=159
  _SETHEADNODERESPONSE._serialized_end=197
  _DECLAREHEADREQUEST._serialized_start=199
  _DECLAREHEADREQUEST._serialized_end=219
  _DECLAREHEADRESPONSE._serialized_start=221
  _DECLAREHEADRESPONSE._serialized_end=259
  _DECLARETAILREQUEST._serialized_start=261
  _DECLARETAILREQUEST._serialized_end=281
  _DECLARETAILRESPONSE._serialized_start=283
  _DECLARETAILRESPONSE._serialized_end=321
  _UNSETHEADREQUEST._serialized_start=323
  _UNSETHEADREQUEST._serialized_end=341
  _UNSETHEADRESPONSE._serialized_start=343
  _UNSETHEADRESPONSE._serialized_end=379
  _UNSETTAILREQUEST._serialized_start=381
  _UNSETTAILREQUEST._serialized_end=399
  _UNSETTAILRESPONSE._serialized_start=401
  _UNSETTAILRESPONSE._serialized_end=437
  _DELETEDATAREQUEST._serialized_start=439
  _DELETEDATAREQUEST._serialized_end=458
  _DELETEDATARESPONSE._serialized_start=460
  _DELETEDATARESPONSE._serialized_end=497
  _CONFIRMWRITEREQUEST._serialized_start=499
  _CONFIRMWRITEREQUEST._serialized_end=539
  _CONFIRMWRITERESPONSE._serialized_start=541
  _CONFIRMWRITERESPONSE._serialized_end=580
  _WRITEOPERATIONREQUEST._serialized_start=582
  _WRITEOPERATIONREQUEST._serialized_end=639
  _WRITEOPERATIONRESPONSE._serialized_start=641
  _WRITEOPERATIONRESPONSE._serialized_end=716
  _UPDATEDATASTATUSREQUEST._serialized_start=718
  _UPDATEDATASTATUSREQUEST._serialized_end=781
  _UPDATEDATASTATUSRESPONSE._serialized_start=783
  _UPDATEDATASTATUSRESPONSE._serialized_end=826
  _CONFIRMTRANSACTIONREQUEST._serialized_start=828
  _CONFIRMTRANSACTIONREQUEST._serialized_end=874
  _CONFIRMTRANSACTIONRESPONSE._serialized_start=876
  _CONFIRMTRANSACTIONRESPONSE._serialized_end=921
  _CONFIRMREADREQUEST._serialized_start=923
  _CONFIRMREADREQUEST._serialized_end=962
  _CONFIRMREADRESPONSE._serialized_start=964
  _CONFIRMREADRESPONSE._serialized_end=1002
  _READOPERATIONREQUEST._serialized_start=1004
  _READOPERATIONREQUEST._serialized_end=1045
  _READOPERATIONRESPONSE._serialized_start=1047
  _READOPERATIONRESPONSE._serialized_end=1085
  _LISTOPERATIONREQUEST._serialized_start=1087
  _LISTOPERATIONREQUEST._serialized_end=1109
  _LISTOPERATIONRESPONSE._serialized_start=1111
  _LISTOPERATIONRESPONSE._serialized_end=1149
  _DATASTATUSREQUEST._serialized_start=1151
  _DATASTATUSREQUEST._serialized_end=1170
  _DATASTATUSRESPONSE._serialized_start=1172
  _DATASTATUSRESPONSE._serialized_end=1213
  _SETTIMEOUTREQUEST._serialized_start=1215
  _SETTIMEOUTREQUEST._serialized_end=1251
  _SETTIMEOUTRESPONSE._serialized_start=1253
  _SETTIMEOUTRESPONSE._serialized_end=1290
  _LOCALSTOREPSREQUEST._serialized_start=1292
  _LOCALSTOREPSREQUEST._serialized_end=1324
  _LOCALSTOREPSRESPONSE._serialized_start=1326
  _LOCALSTOREPSRESPONSE._serialized_end=1365
  _CREATECHAINREQUEST._serialized_start=1367
  _CREATECHAINREQUEST._serialized_end=1387
  _CREATECHAINRESPONSE._serialized_start=1389
  _CREATECHAINRESPONSE._serialized_end=1444
  _LISTCHAINREQUEST._serialized_start=1446
  _LISTCHAINREQUEST._serialized_end=1464
  _LISTCHAINRESPONSE._serialized_start=1466
  _LISTCHAINRESPONSE._serialized_end=1500
  _LISTBOOKSREQUEST._serialized_start=1502
  _LISTBOOKSREQUEST._serialized_end=1520
  _LISTBOOKSRESPONSE._serialized_start=1522
  _LISTBOOKSRESPONSE._serialized_end=1573
  _BOOK._serialized_start=1575
  _BOOK._serialized_end=1610
  _DATAITEMSTATUS._serialized_start=1612
  _DATAITEMSTATUS._serialized_end=1660
  _RESTOREHEADREQUEST._serialized_start=1662
  _RESTOREHEADREQUEST._serialized_end=1682
  _RESTOREHEADRESPONSE._serialized_start=1684
  _RESTOREHEADRESPONSE._serialized_end=1739
  _GETLOCALDATASTORESREQUEST._serialized_start=1741
  _GETLOCALDATASTORESREQUEST._serialized_end=1768
  _GETLOCALDATASTORESRESPONSE._serialized_start=1770
  _GETLOCALDATASTORESRESPONSE._serialized_end=1819
  _SETCHAINREQUEST._serialized_start=1821
  _SETCHAINREQUEST._serialized_end=1853
  _SETCHAINRESPONSE._serialized_start=1855
  _SETCHAINRESPONSE._serialized_end=1890
  _DATASTORE._serialized_start=1893
  _DATASTORE._serialized_end=3194
  _BOOKSTORE._serialized_start=3197
  _BOOKSTORE._serialized_end=4237
# @@protoc_insertion_point(module_scope)