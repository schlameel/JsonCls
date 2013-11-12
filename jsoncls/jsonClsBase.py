'''
Created on Apr 1, 2013

@author: schlameel
@copyright: Schlameel
@license: GPL v3.0
'''
from jsoncls.memberSet import MemberSet
from jsoncls.mapper import DirectMapper
from jsoncls.member import Member, CustomMember
from jsoncls.core import  json_dumps
import json

class JsonClsBase(type):
    '''The metaclass that builds JsonCls classes
    '''

    def __new__(cls, name, bases, attrs):
        '''
        new
        '''
        super_new = super(JsonClsBase, cls).__new__
        parents = [b for b in bases if isinstance(b, JsonClsBase)]
        if not parents:
            # If this isn't a subclass of JsonCls, don't do anything special.
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        
        # Get Members and non-Members
        members = {}
        _member_sets = {}
        if '_mapper' in attrs:
            _mapper = attrs.pop('_mapper')
        elif hasattr(new_class, '_mapper'):
            _mapper = getattr(new_class, '_mapper')
        else:
            _mapper = DirectMapper()
            
        for obj_name, obj in attrs.items():
            if isinstance(obj, Member):
                members.update({obj_name : obj})
            elif isinstance(obj, MemberSet):
                _member_sets.update({obj_name : obj})
            else:
                # Add the non members
                setattr(new_class, obj_name, obj)
            
        #Process Members
        _members = {}
        for member_name, member in members.items():
            # Add the member names as attributes applying the specified class
            if member.cls:
                setattr(new_class, member_name, member.cls())
            else:
                setattr(new_class, member_name, member.cls)
            member.member_name = member_name
            if member.isprivate:
                map_member_name = _public_name(member_name)
            else:
                map_member_name = member_name
            if not member.json_name:
                member.json_name = _mapper.toJson(map_member_name)
            _members.update({member_name : member})
        # Add the list of completed members
        setattr(new_class, '_members', _members)
        setattr(new_class, '_mapper', _mapper)

        #Process Filters
        for member_set_name, member_set in _member_sets.items():
            setattr(member_set,'name', member_set_name)
            setattr(new_class, member_set_name, member_set)
        setattr(new_class, '_member_sets', _member_sets)
            
        return new_class
    
def _public_name(s):
    while s.startswith('_'):
        s = s[1:]
    return s
    
class JsonCls(object):
    '''The base inheritable class
    '''
    __metaclass__ = JsonClsBase
    
    def __reprJSON__(self):
        dct = {}
        for member_name, member in self._members.items():
            attr = getattr(self, member_name)
            if isinstance(attr, JsonCls):
                if not self._is_empty(attr):
                    if member.path:
                        dct.update(self._path_infuse(obj=dct, path=member.path, value=attr))
                    else:
                        dct.update({member.json_name : attr})
            elif attr is not None:
                if member.path:
                    dct.update(self._path_infuse(obj=dct, path=member.path, value=attr))
                else:
                    dct.update({member.json_name : attr})
        return dct
    
    def _is_empty(self, obj):
        for member_name, member in obj._members.items():
            attr = getattr(obj, member_name)
            if attr is not None:
                if isinstance(member, CustomMember) and member.cls:
                    if not self._is_empty(getattr(obj, member_name)):
                        return False
                else:
                        return False
        return True
    
    def _from_json_dct(self, json_dct):
        for member_name, member in self._members.items():
            if member.path:
                json_value = self._path_extract(json_dct, member.path)
            elif not member.json_name in json_dct.keys():
                continue
            else:
                json_value = json_dct[member.json_name]
            if member.enforce_type and member.cls:
                if not member.types_agree(json_value):
                    raise TypeError('JSON value type {0} of item "{1}" does not agree with member.cls{2}'.format(type(json_value), member.json_name, type(member.cls)))
            
            member_value = json_value
            if isinstance(json_value, list):
                member_value = []
                for item in json_value:
                    if member.cls and isinstance(member, CustomMember):
                        if issubclass(member.cls, JsonCls):
                            member_value.append(member.cls().json(item))
                        else:
                            member_value.append(member.cls(item))
                    elif member.cls_factory:
                        cls_factory = member.cls_factory(item)
                        if issubclass(cls_factory, JsonCls):
                            member_value.append(cls_factory().json(item))
                        else:
                            member_value.append(cls_factory(item))
                    else:
                        member_value.append(item)
            else:
                if member.all_keys:
                    if member.cls and isinstance(member, CustomMember) and isinstance(json_value, dict):
                        # For CustomMembers, create an object for each dict item
                        member_value = {}
                        for key, value in json_value.items():
                            if issubclass(member.cls, JsonCls):
                                member_value.update({key : member.cls().json(value)})
                            else:
                                member_value.update({key : member.cls(value)})
                    elif member.cls_factory:
                        cls_factory = member.cls_factory(value)
                        member_value = {}
                        for key, value in json_value.items():
                            if issubclass(cls_factory, JsonCls):
                                member_value.update({key : cls_factory().json(value)})
                            else:
                                member_value.update({key : cls_factory(value)})
                else:
                    if member.cls and isinstance(member, CustomMember) and isinstance(json_value, dict):
                        if issubclass(member.cls, JsonCls):
                            member_value = member.cls().json(json_value)
                        else:
                            member_value = member.cls(json_value)
                    elif member.cls_factory:
                        cls_factory = member.cls_factory(json_value)
                        if issubclass(cls_factory, JsonCls):
                            member_value = cls_factory().json(json_value)
                        else:
                            member_value = cls_factory(json_value) 
            setattr(self, member_name, member_value)
                        
    def _from_json_string(self, json_string):
        self._from_json_dct(json.loads(json_string))
    
    def _path_infuse(self, obj, path, value, indicies=None):
        key = path.split('.')[0]
        next_path = '.'.join(path.split('.')[1:])
        if not key:
            return value
        
        if key == '[]':
            if not (obj and isinstance(obj, list)):
                obj = []
            if indicies:
                self._prefill(obj, indicies[0])
                next_obj = obj[indicies[0]]
                obj[indicies[0]] = self._path_infuse(next_obj, next_path, value, indicies[1:])
            else:
                obj.append(self._path_infuse(None, next_path, value))
        elif key == '*':
            if not (obj and isinstance(obj, dict)):
                obj = {}
            obj.update(value)
        else:
            if not obj:
                obj = {}
            next_obj = None
            if key in obj:
                next_obj = obj.get(key)
            obj.update({key : self._path_infuse(next_obj, next_path, value, indicies)})
        return obj
    
    def _path_extract(self, obj, path):
        current = obj
        extract_list = False
        for key in path.split('.'):
            if extract_list:
                lst = []
                for d in current:
                    lst.append(self._path_extract(d, key))
                current = lst
                break
            elif key == '[]':
                extract_list = True
            elif key == '*':
                return current
                pass
            elif isinstance(current, dict) and current.has_key(key):
                current = current[key]
            else:
                return None
                break
        return current
    
    def _prefill(self, obj, count=0):
        if len(obj) <= count:
            for i in range(len(obj), count + 1):
                obj.append(None)
    
    def json(self, json_in=None, as_dict=False, member_set=None, indent=0, *args):
        ''':param json_in: the source JSON
        :type json_in: string or dict
        :param as_dict: return JSON as dict
        :type as_dict: bool
        :param member_set: set of fields to return in JSON
        :type member_set: jsoncls.MemberSet
        :param indent: spaces to use for each level of indentation
        :type indent: int
        :returns: self if JSON supplied, JSON string or dict if no source supplied
        :rtype: JsonCls, string, dict
        '''
        dct = {}
        if json_in or len(args) > 0:
            if not json_in:
                json_in = args[0]
            if isinstance(json_in, basestring):
                self._from_json_string(json_in)
            else:
                self._from_json_dct(json_in)
            return self
        elif member_set:
            for member in member_set.members:
                if getattr(self, member.member_name):
                    dct.update({member.json_name:getattr(self, member.member_name)})
                
        else:
            dct = self.__reprJSON__()
        
        if as_dict:
            return dct
        else:
            return json_dumps(dct, indent)
    
    
    

    
