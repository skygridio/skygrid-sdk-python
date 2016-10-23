from datetime import datetime

ISO8601_format = '%Y-%m-%dT%H:%M:%S.%fZ'

def object_empty(obj):
  for key in obj:
    return False
  
  return True


#def deep_clone(obj):
#  return JSON.parse(JSON.stringify(obj))


def merge_fields(target, source, fields):
  for field in fields:
    if field in source:
      source_field = source[field]

      if not type(source_field) == dict:
        target[field] = source_field
      else:
        target_field = target[field]

        for key in source_field:
          target_field[key] = source_field[key]


def merge_acl(data, changes=None):
  if 'acl' in changes:
    if not changes['acl'] == None and len(changes['acl']) > 0:
      data['acl'] = changes['acl']
    else:
      data.pop('acl', None)


def prepare_changes(changes, ret):
  for key in changes:
    if not key == 'acl':
      ret[key] = changes[key]
    elif not changes['acl'] == None:
      ret['acl'] = changes['acl']
    else:
      ret['acl'] = None
    
  return ret


def fix_data_dates(data):
  if 'createdAt' in data:
    data['createdAt'] = datetime.strptime(data['createdAt'], ISO8601_format)

  if 'updatedAt' in data:
    data['updatedAt'] = datetime.strptime(data['updatedAt'], ISO8601_format)


def date_to_string(date):
  return date.strftime(ISO8601_format)