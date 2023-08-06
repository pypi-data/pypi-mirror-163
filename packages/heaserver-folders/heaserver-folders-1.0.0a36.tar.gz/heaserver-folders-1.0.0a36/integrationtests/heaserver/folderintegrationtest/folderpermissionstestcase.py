"""
Runs integration tests for the HEA folder service.

Note that each test opens an aiohttp server listening on port 8080.
"""

from heaserver.service.testcase import microservicetestcase, expectedvalues
from heaserver.service.testcase.dockermongo import DockerMongoManager
from heaserver.folder import service
from heaobject import user
from heaobject.root import Permission


db_values = {service.MONGODB_ITEMS_COLLECTION: [{
    'created': None,
    'derived_by': None,
    'derived_from': [],
    'description': None,
    'display_name': 'Reximus',
    'id': '666f6f2d6261722d71757578',
    'invites': [],
    'modified': None,
    'name': 'reximus',
    'owner': user.NONE_USER,
    'shares': [],
    'source': None,
    'type': 'heaobject.folder.Item',
    'version': None,
    'actual_object_type_name': 'heaobject.folder.Folder',
    'actual_object_id': '666f6f2d6261722d71757579',
    'actual_object_uri': 'http://localhost:8080/folders/666f6f2d6261722d71757579',
    'folder_id': 'root'
},
    {
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'id': '0123456789ab0123456789ab',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': user.NONE_USER,
        'shares': [{
            'type': 'heaobject.root.ShareImpl',
            'invite': None,
            'user': user.TEST_USER,
            'permissions': [Permission.VIEWER.name]
        }],
        'source': None,
        'type': 'heaobject.folder.Item',
        'version': None,
        'actual_object_type_name': 'heaobject.folder.Folder',
        'actual_object_id': '0123456789ab0123456789ac',
        'actual_object_uri': 'http://localhost:8080/folders/0123456789ab0123456789ac',
        'folder_id': 'root'
    }
], service.MONGODB_FOLDER_COLLECTION: [{
    'created': None,
    'derived_by': None,
    'derived_from': [],
    'description': None,
    'display_name': 'Reximus',
    'id': '666f6f2d6261722d71757578',
    'invites': [],
    'modified': None,
    'name': 'reximus',
    'owner': user.NONE_USER,
    'shares': [],
    'source': None,
    'type': 'heaobject.folder.Folder',
    'version': None,
    'mime_type': 'application/x.folder'
},
    {
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'id': '0123456789ab0123456789ab',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': user.NONE_USER,
        'shares': [{
            'type': 'heaobject.root.ShareImpl',
            'invite': None,
            'user': user.TEST_USER,
            'permissions': [Permission.VIEWER.name]
        }],
        'source': None,
        'type': 'heaobject.folder.Folder',
        'version': None,
        'mime_type': 'application/x.folder'
    }
], 'components': [
    {
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': user.NONE_USER,
        'shared_with': [],
        'source': None,
        'type': 'heaobject.registry.Component',
        'version': None,
        'base_url': 'http://localhost:8080',
        'resources': [{'type': 'heaobject.registry.Resource', 'resource_type_name': 'heaobject.folder.Folder',
                       'base_path': '/folders'},
                      {'type': 'heaobject.registry.Resource', 'resource_type_name': 'heaobject.folder.Item',
                       'base_path': '/items'}]
    }
]}

content_ = [{'collection': {'version': '1.0', 'href': 'http://localhost:8080/folders/root/items/', 'items': [{'data': [
    {'name': 'created', 'value': None, 'prompt': 'created', 'display': True},
    {'name': 'derived_by', 'value': None, 'prompt': 'derived_by', 'display': True},
    {'name': 'derived_from', 'value': [], 'prompt': 'derived_from', 'display': True},
    {'name': 'description', 'value': None, 'prompt': 'description', 'display': True},
    {'name': 'display_name', 'value': 'Reximus', 'prompt': 'display_name', 'display': True},
    {'name': 'id', 'value': '666f6f2d6261722d71757578', 'prompt': 'id', 'display': False},
    {'name': 'invites', 'value': [], 'prompt': 'invites', 'display': True},
    {'name': 'modified', 'value': None, 'prompt': 'modified', 'display': True},
    {'name': 'name', 'value': 'reximus', 'prompt': 'name', 'display': True},
    {'name': 'owner', 'value': 'system|none', 'prompt': 'owner', 'display': True},
    {'name': 'shares', 'value': [], 'prompt': 'shares', 'display': True},
    {'name': 'source', 'value': None, 'prompt': 'source', 'display': True},
    {'name': 'version', 'value': None, 'prompt': 'version', 'display': True},
    {'name': 'actual_object_type_name', 'value': 'heaobject.folder.Folder', 'prompt': 'actual_object_type_name',
     'display': True},
    {'name': 'actual_object_id', 'value': '666f6f2d6261722d71757579', 'prompt': 'actual_object_id', 'display': True},
    {'name': 'folder_id', 'value': 'root', 'prompt': 'folder_id', 'display': True},
    {'section': 'actual_object', 'name': 'created', 'value': None, 'prompt': 'created', 'display': True},
    {'section': 'actual_object', 'name': 'derived_by', 'value': None, 'prompt': 'derived_by', 'display': True},
    {'section': 'actual_object', 'name': 'derived_from', 'value': [], 'prompt': 'derived_from', 'display': True},
    {'section': 'actual_object', 'name': 'description', 'value': None, 'prompt': 'description', 'display': True},
    {'section': 'actual_object', 'name': 'display_name', 'value': 'Reximus', 'prompt': 'display_name', 'display': True},
    {'section': 'actual_object', 'name': 'id', 'value': '666f6f2d6261722d71757579', 'prompt': 'id', 'display': False},
    {'section': 'actual_object', 'name': 'invites', 'value': [], 'prompt': 'invites', 'display': True},
    {'section': 'actual_object', 'name': 'modified', 'value': None, 'prompt': 'modified', 'display': True},
    {'section': 'actual_object', 'name': 'name', 'value': 'reximus', 'prompt': 'name', 'display': True},
    {'section': 'actual_object', 'name': 'owner', 'value': 'system|none', 'prompt': 'owner', 'display': True},
    {'section': 'actual_object', 'name': 'shares', 'value': [], 'prompt': 'shares', 'display': True},
    {'section': 'actual_object', 'name': 'source', 'value': None, 'prompt': 'source', 'display': True},
    {'section': 'actual_object', 'name': 'version', 'value': None, 'prompt': 'version', 'display': True},
    {'section': 'actual_object', 'name': 'mime_type', 'value': 'application/x.folder', 'prompt': 'mime_type',
     'display': True}], 'links': [{'prompt': 'Move', 'rel': 'mover',
                                   'href': 'http://localhost:8080/folders/root/items/666f6f2d6261722d71757578/mover'},
                                  {'prompt': 'Open', 'rel': 'hea-opener-choices',
                                   'href': 'http://localhost:8080/folders/root/items/666f6f2d6261722d71757578/opener'},
                                  {'prompt': 'Duplicate', 'rel': 'duplicator',
                                   'href': 'http://localhost:8080/folders/root/items/666f6f2d6261722d71757578/duplicator'}]}],
                            'template': {'prompt': 'Properties', 'rel': 'properties', 'data': [
                                {'name': 'id', 'value': '666f6f2d6261722d71757578', 'prompt': 'Id', 'required': True,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'source', 'value': None, 'prompt': 'Source', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'version', 'value': None, 'prompt': 'Version', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'display_name', 'value': 'Reximus', 'prompt': 'Name', 'required': True,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'description', 'value': None, 'prompt': 'Description', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'owner', 'value': 'system|none', 'prompt': 'Owner', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'created', 'value': None, 'prompt': 'Created', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'modified', 'value': None, 'prompt': 'Modified', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'invites', 'value': [], 'prompt': 'Share invites', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'shares', 'value': [], 'prompt': 'Shared with', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'derived_by', 'value': None, 'prompt': 'Derived by', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'derived_from', 'value': [], 'prompt': 'Derived from', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'items', 'value': None, 'prompt': 'Items', 'required': False, 'readOnly': True,
                                 'pattern': ''}]}}}, {
                'collection': {'version': '1.0', 'href': 'http://localhost:8080/folders/root/items/', 'items': [{
                    'data': [
                        {
                            'name': 'created',
                            'value': None,
                            'prompt': 'created',
                            'display': True},
                        {
                            'name': 'derived_by',
                            'value': None,
                            'prompt': 'derived_by',
                            'display': True},
                        {
                            'name': 'derived_from',
                            'value': [],
                            'prompt': 'derived_from',
                            'display': True},
                        {
                            'name': 'description',
                            'value': None,
                            'prompt': 'description',
                            'display': True},
                        {
                            'name': 'display_name',
                            'value': 'Reximus',
                            'prompt': 'display_name',
                            'display': True},
                        {
                            'name': 'id',
                            'value': '0123456789ab0123456789ab',
                            'prompt': 'id',
                            'display': False},
                        {
                            'name': 'invites',
                            'value': [],
                            'prompt': 'invites',
                            'display': True},
                        {
                            'name': 'modified',
                            'value': None,
                            'prompt': 'modified',
                            'display': True},
                        {
                            'name': 'name',
                            'value': 'reximus',
                            'prompt': 'name',
                            'display': True},
                        {
                            'name': 'owner',
                            'value': 'system|none',
                            'prompt': 'owner',
                            'display': True},
                        {
                            'name': 'shares',
                            'value': [],
                            'prompt': 'shares',
                            'display': True},
                        {
                            'name': 'source',
                            'value': None,
                            'prompt': 'source',
                            'display': True},
                        {
                            'name': 'version',
                            'value': None,
                            'prompt': 'version',
                            'display': True},
                        {
                            'name': 'actual_object_type_name',
                            'value': 'heaobject.folder.Folder',
                            'prompt': 'actual_object_type_name',
                            'display': True},
                        {
                            'name': 'actual_object_id',
                            'value': '0123456789ab0123456789ac',
                            'prompt': 'actual_object_id',
                            'display': True},
                        {
                            'name': 'folder_id',
                            'value': 'root',
                            'prompt': 'folder_id',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'created',
                            'value': None,
                            'prompt': 'created',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'derived_by',
                            'value': None,
                            'prompt': 'derived_by',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'derived_from',
                            'value': [],
                            'prompt': 'derived_from',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'description',
                            'value': None,
                            'prompt': 'description',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'display_name',
                            'value': 'Reximus',
                            'prompt': 'display_name',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'id',
                            'value': '0123456789ab0123456789ac',
                            'prompt': 'id',
                            'display': False},
                        {
                            'section': 'actual_object',
                            'name': 'invites',
                            'value': [],
                            'prompt': 'invites',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'modified',
                            'value': None,
                            'prompt': 'modified',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'name',
                            'value': 'reximus',
                            'prompt': 'name',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'owner',
                            'value': 'system|none',
                            'prompt': 'owner',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'shares',
                            'value': [],
                            'prompt': 'shares',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'source',
                            'value': None,
                            'prompt': 'source',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'version',
                            'value': None,
                            'prompt': 'version',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'mime_type',
                            'value': 'application/x.folder',
                            'prompt': 'mime_type',
                            'display': True}],
                    'links': [
                        {
                            'prompt': 'Move',
                            'rel': 'mover',
                            'href': 'http://localhost:8080/folders/root/items/0123456789ab0123456789ab/mover'},
                        {
                            'prompt': 'Open',
                            'rel': 'hea-opener-choices',
                            'href': 'http://localhost:8080/folders/root/items/0123456789ab0123456789ab/opener'},
                        {
                            'prompt': 'Duplicate',
                            'rel': 'duplicator',
                            'href': 'http://localhost:8080/folders/root/items/0123456789ab0123456789ab/duplicator'}]}],
                               'template': {'prompt': 'Properties', 'rel': 'properties', 'data': [
                                   {'name': 'id', 'value': '0123456789ab0123456789ab', 'prompt': 'Id', 'required': True,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'source', 'value': None, 'prompt': 'Source', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'version', 'value': None, 'prompt': 'Version', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'display_name', 'value': 'Reximus', 'prompt': 'Name', 'required': True,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'description', 'value': None, 'prompt': 'Description', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'owner', 'value': 'system|none', 'prompt': 'Owner', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'created', 'value': None, 'prompt': 'Created', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'modified', 'value': None, 'prompt': 'Modified', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'invites', 'value': [], 'prompt': 'Share invites', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'shares', 'value': [], 'prompt': 'Shared with', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'derived_by', 'value': None, 'prompt': 'Derived by', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'derived_from', 'value': [], 'prompt': 'Derived from', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'items', 'value': None, 'prompt': 'Items', 'required': False,
                                    'readOnly': True, 'pattern': ''}]}}}]

content = {
    service.MONGODB_ITEMS_COLLECTION: {
        '666f6f2d6261722d71757578': content_,
        '0123456789ab0123456789ab': {}
    },
    service.MONGODB_FOLDER_COLLECTION: {
        '666f6f2d6261722d71757578': content_,
        '0123456789ab0123456789ab': {}
    }
}

ItemPermissionsTestCase = \
    microservicetestcase.get_test_case_cls_default(href='http://localhost:8080/folders/root/items/',
                                                   wstl_package=service.__package__,
                                                   coll=service.MONGODB_ITEMS_COLLECTION,
                                                   fixtures=db_values,
                                                   db_manager_cls=DockerMongoManager,
                                                   get_all_actions=[
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-item-move',
                                                           url='http://localhost:8080/folders/{folder_id}/items/{id}/mover',
                                                           rel=['hea-mover']),
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-item-duplicate',
                                                           url='http://localhost:8080/folders/{folder_id}/items/{id}/duplicator',
                                                           rel=['hea-duplicator']),
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-item-get-actual',
                                                           url='{+actual_object_uri}',
                                                           rel=['hea-actual']
                                                       )
                                                   ],
                                                   get_actions=[
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-item-move',
                                                           url='http://localhost:8080/folders/{folder_id}/items/{id}/mover',
                                                           rel=['hea-mover']),
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-item-duplicate',
                                                           url='http://localhost:8080/folders/{folder_id}/items/{id}/duplicator',
                                                           rel=['hea-duplicator']),
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-item-get-actual',
                                                           url='{+actual_object_uri}',
                                                           rel=['hea-actual']
                                                       )
                                                   ],
                                                   duplicate_action_name='heaserver-folders-item-duplicate-form',
                                                   put_content_status=404,
                                                   sub=user.TEST_USER)

FolderPermissionsTestCase = \
    microservicetestcase.get_test_case_cls_default(href='http://localhost:8080/folders/',
                                                   wstl_package=service.__package__,
                                                   coll=service.MONGODB_FOLDER_COLLECTION,
                                                   db_manager_cls=DockerMongoManager,
                                                   fixtures=db_values,
                                                   get_all_actions=[
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-folder-get-properties',
                                                           rel=['hea-properties']),
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-folder-get-open-choices',
                                                           url='http://localhost:8080/folders/{id}/opener',
                                                           rel=['hea-opener-choices']),
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-folder-duplicate',
                                                           url='http://localhost:8080/folders/{id}/duplicator',
                                                           rel=['hea-duplicator'])],
                                                   get_actions=[
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-folder-get-properties',
                                                           rel=['hea-properties']),
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-folder-get-open-choices',
                                                           url='http://localhost:8080/folders/{id}/opener',
                                                           rel=['hea-opener-choices']),
                                                       expectedvalues.Action(
                                                           name='heaserver-folders-folder-duplicate',
                                                           url='http://localhost:8080/folders/{id}/duplicator',
                                                           rel=['hea-duplicator'])],
                                                   duplicate_action_name='heaserver-folders-folder-duplicate-form',
                                                   put_content_status=404,
                                                   sub=user.TEST_USER)
