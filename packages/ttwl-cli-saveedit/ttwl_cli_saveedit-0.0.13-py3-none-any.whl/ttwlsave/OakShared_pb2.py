# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: OakShared.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='OakShared.proto',
  package='OakSave',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0fOakShared.proto\x12\x07OakSave\"\'\n\x04Vec3\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"=\n\x14GameStatSaveGameData\x12\x12\n\nstat_value\x18\x01 \x01(\x05\x12\x11\n\tstat_path\x18\x02 \x01(\t\"T\n\x19InventoryCategorySaveData\x12%\n\x1d\x62\x61se_category_definition_hash\x18\x01 \x01(\r\x12\x10\n\x08quantity\x18\x02 \x01(\x05\">\n\x12OakSDUSaveGameData\x12\x11\n\tsdu_level\x18\x01 \x01(\x05\x12\x15\n\rsdu_data_path\x18\x02 \x01(\t\"c\n!RegisteredDownloadableEntitlement\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08\x63onsumed\x18\x02 \x01(\r\x12\x12\n\nregistered\x18\x03 \x01(\x08\x12\x0c\n\x04seen\x18\x04 \x01(\x08\"\xa6\x01\n\"RegisteredDownloadableEntitlements\x12%\n\x1d\x65ntitlement_source_asset_path\x18\x01 \x01(\t\x12\x17\n\x0f\x65ntitlement_ids\x18\x02 \x03(\x03\x12@\n\x0c\x65ntitlements\x18\x03 \x03(\x0b\x32*.OakSave.RegisteredDownloadableEntitlement\"T\n\x19\x43hallengeStatSaveGameData\x12\x1a\n\x12\x63urrent_stat_value\x18\x01 \x01(\x05\x12\x1b\n\x13\x63hallenge_stat_path\x18\x02 \x01(\t\"B\n\x1eOakChallengeRewardSaveGameData\x12 \n\x18\x63hallenge_reward_claimed\x18\x01 \x01(\x08\"\xc3\x02\n\x15\x43hallengeSaveGameData\x12\x17\n\x0f\x63ompleted_count\x18\x01 \x01(\x05\x12\x11\n\tis_active\x18\x02 \x01(\x08\x12\x1b\n\x13\x63urrently_completed\x18\x03 \x01(\x08\x12 \n\x18\x63ompleted_progress_level\x18\x04 \x01(\x05\x12\x18\n\x10progress_counter\x18\x05 \x01(\x05\x12?\n\x13stat_instance_state\x18\x06 \x03(\x0b\x32\".OakSave.ChallengeStatSaveGameData\x12\x1c\n\x14\x63hallenge_class_path\x18\x07 \x01(\t\x12\x46\n\x15\x63hallenge_reward_info\x18\x08 \x03(\x0b\x32\'.OakSave.OakChallengeRewardSaveGameData\"\xeb\x01\n\x0bOakMailItem\x12\x16\n\x0email_item_type\x18\x01 \x01(\r\x12\x1b\n\x13sender_display_name\x18\x02 \x01(\t\x12\x0f\n\x07subject\x18\x03 \x01(\t\x12\x0c\n\x04\x62ody\x18\x04 \x01(\t\x12\x1a\n\x12gear_serial_number\x18\x05 \x01(\t\x12\x11\n\tmail_guid\x18\x06 \x01(\t\x12\x11\n\tdate_sent\x18\x07 \x01(\x03\x12\x17\n\x0f\x65xpiration_date\x18\x08 \x01(\x03\x12\x16\n\x0e\x66rom_player_id\x18\t \x01(\t\x12\x15\n\rhas_been_read\x18\n \x01(\x08\"P\n\x1cOakCustomizationSaveGameData\x12\x0e\n\x06is_new\x18\x01 \x01(\x08\x12 \n\x18\x63ustomization_asset_path\x18\x02 \x01(\t\"T\n!OakInventoryCustomizationPartInfo\x12\x1f\n\x17\x63ustomization_part_hash\x18\x01 \x01(\r\x12\x0e\n\x06is_new\x18\x02 \x01(\x08\"M\n\x1fOakProfileCustomizationLinkData\x12\x1a\n\x12\x63ustomization_name\x18\x01 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x02 \x01(\x08\"\xf8\x01\n\'InventoryBalanceStateInitializationData\x12\x12\n\ngame_stage\x18\x01 \x01(\x05\x12\x16\n\x0einventory_data\x18\x02 \x01(\t\x12\x1e\n\x16inventory_balance_data\x18\x03 \x01(\t\x12\x19\n\x11manufacturer_data\x18\x04 \x01(\t\x12\x11\n\tpart_list\x18\x05 \x03(\t\x12\x19\n\x11generic_part_list\x18\x06 \x03(\t\x12\x17\n\x0f\x61\x64\x64itional_data\x18\x07 \x01(\x0c\x12\x1f\n\x17\x63ustomization_part_list\x18\x08 \x03(\t\"\xb6\x01\n\x1cOakInventoryItemSaveGameData\x12\x1a\n\x12item_serial_number\x18\x01 \x01(\x0c\x12\x1a\n\x12pickup_order_index\x18\x02 \x01(\x05\x12\r\n\x05\x66lags\x18\x03 \x01(\x05\x12O\n\x15\x64\x65velopment_save_data\x18\x05 \x01(\x0b\x32\x30.OakSave.InventoryBalanceStateInitializationDatab\x06proto3')
)




_VEC3 = _descriptor.Descriptor(
  name='Vec3',
  full_name='OakSave.Vec3',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='OakSave.Vec3.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='OakSave.Vec3.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='z', full_name='OakSave.Vec3.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=67,
)


_GAMESTATSAVEGAMEDATA = _descriptor.Descriptor(
  name='GameStatSaveGameData',
  full_name='OakSave.GameStatSaveGameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stat_value', full_name='OakSave.GameStatSaveGameData.stat_value', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stat_path', full_name='OakSave.GameStatSaveGameData.stat_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=130,
)


_INVENTORYCATEGORYSAVEDATA = _descriptor.Descriptor(
  name='InventoryCategorySaveData',
  full_name='OakSave.InventoryCategorySaveData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_category_definition_hash', full_name='OakSave.InventoryCategorySaveData.base_category_definition_hash', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='quantity', full_name='OakSave.InventoryCategorySaveData.quantity', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=132,
  serialized_end=216,
)


_OAKSDUSAVEGAMEDATA = _descriptor.Descriptor(
  name='OakSDUSaveGameData',
  full_name='OakSave.OakSDUSaveGameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sdu_level', full_name='OakSave.OakSDUSaveGameData.sdu_level', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sdu_data_path', full_name='OakSave.OakSDUSaveGameData.sdu_data_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=218,
  serialized_end=280,
)


_REGISTEREDDOWNLOADABLEENTITLEMENT = _descriptor.Descriptor(
  name='RegisteredDownloadableEntitlement',
  full_name='OakSave.RegisteredDownloadableEntitlement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='OakSave.RegisteredDownloadableEntitlement.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='consumed', full_name='OakSave.RegisteredDownloadableEntitlement.consumed', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='registered', full_name='OakSave.RegisteredDownloadableEntitlement.registered', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seen', full_name='OakSave.RegisteredDownloadableEntitlement.seen', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=282,
  serialized_end=381,
)


_REGISTEREDDOWNLOADABLEENTITLEMENTS = _descriptor.Descriptor(
  name='RegisteredDownloadableEntitlements',
  full_name='OakSave.RegisteredDownloadableEntitlements',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='entitlement_source_asset_path', full_name='OakSave.RegisteredDownloadableEntitlements.entitlement_source_asset_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entitlement_ids', full_name='OakSave.RegisteredDownloadableEntitlements.entitlement_ids', index=1,
      number=2, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entitlements', full_name='OakSave.RegisteredDownloadableEntitlements.entitlements', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=384,
  serialized_end=550,
)


_CHALLENGESTATSAVEGAMEDATA = _descriptor.Descriptor(
  name='ChallengeStatSaveGameData',
  full_name='OakSave.ChallengeStatSaveGameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_stat_value', full_name='OakSave.ChallengeStatSaveGameData.current_stat_value', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='challenge_stat_path', full_name='OakSave.ChallengeStatSaveGameData.challenge_stat_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=552,
  serialized_end=636,
)


_OAKCHALLENGEREWARDSAVEGAMEDATA = _descriptor.Descriptor(
  name='OakChallengeRewardSaveGameData',
  full_name='OakSave.OakChallengeRewardSaveGameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='challenge_reward_claimed', full_name='OakSave.OakChallengeRewardSaveGameData.challenge_reward_claimed', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=638,
  serialized_end=704,
)


_CHALLENGESAVEGAMEDATA = _descriptor.Descriptor(
  name='ChallengeSaveGameData',
  full_name='OakSave.ChallengeSaveGameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='completed_count', full_name='OakSave.ChallengeSaveGameData.completed_count', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_active', full_name='OakSave.ChallengeSaveGameData.is_active', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='currently_completed', full_name='OakSave.ChallengeSaveGameData.currently_completed', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='completed_progress_level', full_name='OakSave.ChallengeSaveGameData.completed_progress_level', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='progress_counter', full_name='OakSave.ChallengeSaveGameData.progress_counter', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stat_instance_state', full_name='OakSave.ChallengeSaveGameData.stat_instance_state', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='challenge_class_path', full_name='OakSave.ChallengeSaveGameData.challenge_class_path', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='challenge_reward_info', full_name='OakSave.ChallengeSaveGameData.challenge_reward_info', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=707,
  serialized_end=1030,
)


_OAKMAILITEM = _descriptor.Descriptor(
  name='OakMailItem',
  full_name='OakSave.OakMailItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mail_item_type', full_name='OakSave.OakMailItem.mail_item_type', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sender_display_name', full_name='OakSave.OakMailItem.sender_display_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='subject', full_name='OakSave.OakMailItem.subject', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='body', full_name='OakSave.OakMailItem.body', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gear_serial_number', full_name='OakSave.OakMailItem.gear_serial_number', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mail_guid', full_name='OakSave.OakMailItem.mail_guid', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_sent', full_name='OakSave.OakMailItem.date_sent', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expiration_date', full_name='OakSave.OakMailItem.expiration_date', index=7,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_player_id', full_name='OakSave.OakMailItem.from_player_id', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_been_read', full_name='OakSave.OakMailItem.has_been_read', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1033,
  serialized_end=1268,
)


_OAKCUSTOMIZATIONSAVEGAMEDATA = _descriptor.Descriptor(
  name='OakCustomizationSaveGameData',
  full_name='OakSave.OakCustomizationSaveGameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_new', full_name='OakSave.OakCustomizationSaveGameData.is_new', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='customization_asset_path', full_name='OakSave.OakCustomizationSaveGameData.customization_asset_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1270,
  serialized_end=1350,
)


_OAKINVENTORYCUSTOMIZATIONPARTINFO = _descriptor.Descriptor(
  name='OakInventoryCustomizationPartInfo',
  full_name='OakSave.OakInventoryCustomizationPartInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customization_part_hash', full_name='OakSave.OakInventoryCustomizationPartInfo.customization_part_hash', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_new', full_name='OakSave.OakInventoryCustomizationPartInfo.is_new', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1352,
  serialized_end=1436,
)


_OAKPROFILECUSTOMIZATIONLINKDATA = _descriptor.Descriptor(
  name='OakProfileCustomizationLinkData',
  full_name='OakSave.OakProfileCustomizationLinkData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customization_name', full_name='OakSave.OakProfileCustomizationLinkData.customization_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='active', full_name='OakSave.OakProfileCustomizationLinkData.active', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1438,
  serialized_end=1515,
)


_INVENTORYBALANCESTATEINITIALIZATIONDATA = _descriptor.Descriptor(
  name='InventoryBalanceStateInitializationData',
  full_name='OakSave.InventoryBalanceStateInitializationData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_stage', full_name='OakSave.InventoryBalanceStateInitializationData.game_stage', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inventory_data', full_name='OakSave.InventoryBalanceStateInitializationData.inventory_data', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inventory_balance_data', full_name='OakSave.InventoryBalanceStateInitializationData.inventory_balance_data', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='manufacturer_data', full_name='OakSave.InventoryBalanceStateInitializationData.manufacturer_data', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='part_list', full_name='OakSave.InventoryBalanceStateInitializationData.part_list', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='generic_part_list', full_name='OakSave.InventoryBalanceStateInitializationData.generic_part_list', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='additional_data', full_name='OakSave.InventoryBalanceStateInitializationData.additional_data', index=6,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='customization_part_list', full_name='OakSave.InventoryBalanceStateInitializationData.customization_part_list', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1518,
  serialized_end=1766,
)


_OAKINVENTORYITEMSAVEGAMEDATA = _descriptor.Descriptor(
  name='OakInventoryItemSaveGameData',
  full_name='OakSave.OakInventoryItemSaveGameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='item_serial_number', full_name='OakSave.OakInventoryItemSaveGameData.item_serial_number', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pickup_order_index', full_name='OakSave.OakInventoryItemSaveGameData.pickup_order_index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='flags', full_name='OakSave.OakInventoryItemSaveGameData.flags', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='development_save_data', full_name='OakSave.OakInventoryItemSaveGameData.development_save_data', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1769,
  serialized_end=1951,
)

_REGISTEREDDOWNLOADABLEENTITLEMENTS.fields_by_name['entitlements'].message_type = _REGISTEREDDOWNLOADABLEENTITLEMENT
_CHALLENGESAVEGAMEDATA.fields_by_name['stat_instance_state'].message_type = _CHALLENGESTATSAVEGAMEDATA
_CHALLENGESAVEGAMEDATA.fields_by_name['challenge_reward_info'].message_type = _OAKCHALLENGEREWARDSAVEGAMEDATA
_OAKINVENTORYITEMSAVEGAMEDATA.fields_by_name['development_save_data'].message_type = _INVENTORYBALANCESTATEINITIALIZATIONDATA
DESCRIPTOR.message_types_by_name['Vec3'] = _VEC3
DESCRIPTOR.message_types_by_name['GameStatSaveGameData'] = _GAMESTATSAVEGAMEDATA
DESCRIPTOR.message_types_by_name['InventoryCategorySaveData'] = _INVENTORYCATEGORYSAVEDATA
DESCRIPTOR.message_types_by_name['OakSDUSaveGameData'] = _OAKSDUSAVEGAMEDATA
DESCRIPTOR.message_types_by_name['RegisteredDownloadableEntitlement'] = _REGISTEREDDOWNLOADABLEENTITLEMENT
DESCRIPTOR.message_types_by_name['RegisteredDownloadableEntitlements'] = _REGISTEREDDOWNLOADABLEENTITLEMENTS
DESCRIPTOR.message_types_by_name['ChallengeStatSaveGameData'] = _CHALLENGESTATSAVEGAMEDATA
DESCRIPTOR.message_types_by_name['OakChallengeRewardSaveGameData'] = _OAKCHALLENGEREWARDSAVEGAMEDATA
DESCRIPTOR.message_types_by_name['ChallengeSaveGameData'] = _CHALLENGESAVEGAMEDATA
DESCRIPTOR.message_types_by_name['OakMailItem'] = _OAKMAILITEM
DESCRIPTOR.message_types_by_name['OakCustomizationSaveGameData'] = _OAKCUSTOMIZATIONSAVEGAMEDATA
DESCRIPTOR.message_types_by_name['OakInventoryCustomizationPartInfo'] = _OAKINVENTORYCUSTOMIZATIONPARTINFO
DESCRIPTOR.message_types_by_name['OakProfileCustomizationLinkData'] = _OAKPROFILECUSTOMIZATIONLINKDATA
DESCRIPTOR.message_types_by_name['InventoryBalanceStateInitializationData'] = _INVENTORYBALANCESTATEINITIALIZATIONDATA
DESCRIPTOR.message_types_by_name['OakInventoryItemSaveGameData'] = _OAKINVENTORYITEMSAVEGAMEDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Vec3 = _reflection.GeneratedProtocolMessageType('Vec3', (_message.Message,), dict(
  DESCRIPTOR = _VEC3,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.Vec3)
  ))
_sym_db.RegisterMessage(Vec3)

GameStatSaveGameData = _reflection.GeneratedProtocolMessageType('GameStatSaveGameData', (_message.Message,), dict(
  DESCRIPTOR = _GAMESTATSAVEGAMEDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.GameStatSaveGameData)
  ))
_sym_db.RegisterMessage(GameStatSaveGameData)

InventoryCategorySaveData = _reflection.GeneratedProtocolMessageType('InventoryCategorySaveData', (_message.Message,), dict(
  DESCRIPTOR = _INVENTORYCATEGORYSAVEDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.InventoryCategorySaveData)
  ))
_sym_db.RegisterMessage(InventoryCategorySaveData)

OakSDUSaveGameData = _reflection.GeneratedProtocolMessageType('OakSDUSaveGameData', (_message.Message,), dict(
  DESCRIPTOR = _OAKSDUSAVEGAMEDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.OakSDUSaveGameData)
  ))
_sym_db.RegisterMessage(OakSDUSaveGameData)

RegisteredDownloadableEntitlement = _reflection.GeneratedProtocolMessageType('RegisteredDownloadableEntitlement', (_message.Message,), dict(
  DESCRIPTOR = _REGISTEREDDOWNLOADABLEENTITLEMENT,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.RegisteredDownloadableEntitlement)
  ))
_sym_db.RegisterMessage(RegisteredDownloadableEntitlement)

RegisteredDownloadableEntitlements = _reflection.GeneratedProtocolMessageType('RegisteredDownloadableEntitlements', (_message.Message,), dict(
  DESCRIPTOR = _REGISTEREDDOWNLOADABLEENTITLEMENTS,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.RegisteredDownloadableEntitlements)
  ))
_sym_db.RegisterMessage(RegisteredDownloadableEntitlements)

ChallengeStatSaveGameData = _reflection.GeneratedProtocolMessageType('ChallengeStatSaveGameData', (_message.Message,), dict(
  DESCRIPTOR = _CHALLENGESTATSAVEGAMEDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.ChallengeStatSaveGameData)
  ))
_sym_db.RegisterMessage(ChallengeStatSaveGameData)

OakChallengeRewardSaveGameData = _reflection.GeneratedProtocolMessageType('OakChallengeRewardSaveGameData', (_message.Message,), dict(
  DESCRIPTOR = _OAKCHALLENGEREWARDSAVEGAMEDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.OakChallengeRewardSaveGameData)
  ))
_sym_db.RegisterMessage(OakChallengeRewardSaveGameData)

ChallengeSaveGameData = _reflection.GeneratedProtocolMessageType('ChallengeSaveGameData', (_message.Message,), dict(
  DESCRIPTOR = _CHALLENGESAVEGAMEDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.ChallengeSaveGameData)
  ))
_sym_db.RegisterMessage(ChallengeSaveGameData)

OakMailItem = _reflection.GeneratedProtocolMessageType('OakMailItem', (_message.Message,), dict(
  DESCRIPTOR = _OAKMAILITEM,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.OakMailItem)
  ))
_sym_db.RegisterMessage(OakMailItem)

OakCustomizationSaveGameData = _reflection.GeneratedProtocolMessageType('OakCustomizationSaveGameData', (_message.Message,), dict(
  DESCRIPTOR = _OAKCUSTOMIZATIONSAVEGAMEDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.OakCustomizationSaveGameData)
  ))
_sym_db.RegisterMessage(OakCustomizationSaveGameData)

OakInventoryCustomizationPartInfo = _reflection.GeneratedProtocolMessageType('OakInventoryCustomizationPartInfo', (_message.Message,), dict(
  DESCRIPTOR = _OAKINVENTORYCUSTOMIZATIONPARTINFO,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.OakInventoryCustomizationPartInfo)
  ))
_sym_db.RegisterMessage(OakInventoryCustomizationPartInfo)

OakProfileCustomizationLinkData = _reflection.GeneratedProtocolMessageType('OakProfileCustomizationLinkData', (_message.Message,), dict(
  DESCRIPTOR = _OAKPROFILECUSTOMIZATIONLINKDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.OakProfileCustomizationLinkData)
  ))
_sym_db.RegisterMessage(OakProfileCustomizationLinkData)

InventoryBalanceStateInitializationData = _reflection.GeneratedProtocolMessageType('InventoryBalanceStateInitializationData', (_message.Message,), dict(
  DESCRIPTOR = _INVENTORYBALANCESTATEINITIALIZATIONDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.InventoryBalanceStateInitializationData)
  ))
_sym_db.RegisterMessage(InventoryBalanceStateInitializationData)

OakInventoryItemSaveGameData = _reflection.GeneratedProtocolMessageType('OakInventoryItemSaveGameData', (_message.Message,), dict(
  DESCRIPTOR = _OAKINVENTORYITEMSAVEGAMEDATA,
  __module__ = 'OakShared_pb2'
  # @@protoc_insertion_point(class_scope:OakSave.OakInventoryItemSaveGameData)
  ))
_sym_db.RegisterMessage(OakInventoryItemSaveGameData)


# @@protoc_insertion_point(module_scope)
