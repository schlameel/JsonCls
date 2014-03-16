'''
Created on Apr 1, 2013

@author: john
@copyright: John McCormick
@license: GPL v3.0
'''

class Member(object):
    '''The base class for a JsonCls member
    '''
    cls = str()
    cls_factory = None
    islist = False
    isprivate = False
    enforce_type = False
    json_name = str()
    member_name = str()
    allow_none = True
    all_keys = False
    path = None
    _explicit_json_name = None

    def __init__(self, cls=None, islist=False, isprivate=False, enforce_type=False, 
                 json_name=None, all_keys=False, keys=None, path=None, cls_factory=None):
        self.cls = cls
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        self.cls_factory = cls_factory
        
    def types_agree(self, value):
        if not value:
            return self.allow_none
        if self.islist and isinstance(value, list):
            if len(value) > 0:
                value = value[0]
            else:
                return self.allow_none
        
        if isinstance(self, IntMember):
            return isinstance(value, int)
        elif isinstance(self, LongMember):
            return isinstance(value, long)
        elif isinstance(self, FloatMember):
            return isinstance(value, float)
        elif isinstance(self, BasestringMember):
            return isinstance(value, basestring)
        elif isinstance(self, StrMember):
            return isinstance(value, str)
        elif isinstance(self, UnicodeMember):
            return isinstance(value, unicode)
        elif isinstance(self, BoolMember):
            return isinstance(value, bool)
        elif isinstance(self, CustomMember):
            return isinstance(value, dict)
        elif isinstance(self, Member):
            return True
        else:
            return False
        
    def read(self, value):
        '''Convert value (the value of the member) to a valid type JSON
        accepts.  For instance an array of bytes might be converted to 
        a hexidecimal string.
        '''
        return value
    
    def write(self, value):
        '''Convert value (the value of the member) from the JSON type
        to the expected type.  For instance a hexidecimal string might  
        be converted to an array of bytes.
        '''
        return value

class IntMember(Member):
    '''Integer Member
    '''     
    def __init__(self, islist=False, isprivate=False, enforce_type=True, json_name=None, 
                 all_keys=False, keys=None, path=None):
        self.cls = int
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        
class LongMember(Member):
    '''Long Member
    '''        
    def __init__(self, islist=False, isprivate=False, enforce_type=True, json_name=None, 
                 all_keys=False, keys=None, path=None):
        self.cls = long
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        
class FloatMember(Member):
    '''Float Member
    '''        
    def __init__(self, islist=False, isprivate=False, enforce_type=True, json_name=None, 
                 all_keys=False, keys=None, path=None):
        self.cls = float
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        
class BasestringMember(Member):
    '''basestring Member
    '''      
    def __init__(self, islist=False, isprivate=False, enforce_type=True, json_name=None, 
                 all_keys=False, keys=None, path=None):
        self.cls = basestring
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        
class StrMember(Member):
    '''string Member
    '''        
    def __init__(self, islist=False, isprivate=False, enforce_type=True, json_name=None, 
                 all_keys=False, keys=None, path=None):
        self.cls = str
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        
class UnicodeMember(Member):       
    '''Unicode Member
    ''' 
    def __init__(self, islist=False, isprivate=False, enforce_type=True, json_name=None, 
                 all_keys=False, keys=None, path=None):
        self.cls = unicode
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        
class BoolMember(Member):
    '''Bool Member
    '''
    def __init__(self, islist=False, isprivate=False, enforce_type=True, json_name=None, 
                 all_keys=False, keys=None, path=None):
        self.cls = bool
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        
class CustomMember(Member):
    '''Member of a custom class
    '''
    def __init__(self,cls=None, islist=False, isprivate=False, enforce_type=True, json_name=None, 
                 all_keys=False, keys=None, path=None, cls_factory=None):
        self.cls = cls
        self.cls_factory = cls_factory
        self.islist = islist
        self.isprivate = isprivate
        self.enforce_type = enforce_type
        self.json_name = json_name
        self.all_keys = all_keys
        self.keys = keys
        self.path = path
        