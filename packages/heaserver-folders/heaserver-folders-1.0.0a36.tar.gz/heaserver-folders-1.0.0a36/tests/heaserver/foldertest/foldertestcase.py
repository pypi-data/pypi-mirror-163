from heaserver.service.testcase import microservicetestcase, expectedvalues
from heaserver.folder import service
from heaobject import user

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
    'shares': [{'type': 'heaobject.root.ShareImpl', 'user': 'system|all', 'permissions': ['CREATOR']}],
    'source': None,
    'type': 'heaobject.folder.Item',
    'version': None,
    'actual_object_type_name': 'heaobject.folder.Folder',
    'actual_object_id': '666f6f2d6261722d71757578',
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
        'shares': [{'type': 'heaobject.root.ShareImpl', 'user': 'system|all', 'permissions': ['CREATOR']}],
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
        'shares': [],
        'source': None,
        'type': 'heaobject.folder.Folder',
        'version': None,
        'mime_type': 'application/x.folder'
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
    {'name': 'folder_id', 'value': 'root', 'prompt': 'folder_id', 'display': True}],
    'links': [{'prompt': 'Move', 'rel': 'mover',
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
                            'display': True}
                    ],
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
        '666f6f2d6261722d71757578': content_
    },
    service.MONGODB_FOLDER_COLLECTION: {
        '666f6f2d6261722d71757579': content_
    }
}

ItemTestCase = \
    microservicetestcase.get_test_case_cls_default(href='http://localhost:8080/folders/root/items/',
                                                   wstl_package=service.__package__,
                                                   coll=service.MONGODB_ITEMS_COLLECTION,
                                                   fixtures=db_values,
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
                                                   put_content_status=404)

FolderTestCase = \
    microservicetestcase.get_test_case_cls_default(href='http://localhost:8080/folders/',
                                                   wstl_package=service.__package__,
                                                   coll=service.MONGODB_FOLDER_COLLECTION,
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
                                                   put_content_status=404)
