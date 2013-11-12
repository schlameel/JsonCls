'''
Created on Apr 1, 2013

@author: schlameel
@copyright: Schlameel
@license: GPL v3.0
'''

class Mapper(object):
    '''An object that allows a custom mapping of member name to json name.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def toJson(self, s):
        return s
    
    def toMember(self, s):
        return s
    
class DirectMapper(Mapper):
    pass
    
class CamelMapper(Mapper):
    '''Map camelCase between json item names and pythonic member names
    camelCase <-> camel_case
    '''
    
    def toJson(self, s):
        ret = ''
        upper_now = False
        for index in range(len(s)):
            if s[index] == '_':
                if not index is 0:
                    upper_now = True
            else:
                if upper_now:
                    ret += s[index].upper()
                    upper_now = False
                else:
                    ret += s[index]
        return ret
        
    def toMember(self, s):
        ret = ''
        start = 0
        for index in range(len(s)):
            if s[index].isupper():
                if ret:
                    ret += '_'
                ret += s[start:index].lower()
                start = index
        if ret:
            return ret + '_' + s[start:].lower()
        else:
            return s

class InitialCapsMapper(Mapper):
    '''Map initial caps between json item names and pythonic member names
    InitialCaps <-> initial_caps
    '''
    
    def toJson(self, s):
        ret = s[0].upper()
        upper_now = False
        for index in range(1, len(s)):
            if s[index] == '_':
                upper_now = True
            else:
                if upper_now:
                    ret += s[index].upper()
                    upper_now = False
                else:
                    ret += s[index]
        return ret
        
    def toMember(self, s):
        ret = s[0].lower()
        start = 1
        for index in range(1, len(s)):
            if s[index].isupper():
                if len(ret) > 1:
                    ret += '_'
                ret += s[start:index].lower()
                start = index
        if len(ret) > 1:
            return ret + '_' + s[start:].lower()
        else:
            return ret + s[start:].lower()
    
class NamedMapper(Mapper):
    '''Supply a list of dicts that maps member names to json names
    [{'member' : member_name_1, 'json' : json_name_1},
     ...
     {'member' : member_name_n, 'json' : json_name_n}]  
    '''
    _member2json = {}
    _json2member = {}
    
    def __init__(self, names):
        for name in names:
            self._member2json.update({name['member'] : name['json']})
            self._json2member.update({name['json'] : name['member']})
    
    def toJson(self, s):
        if s in self._member2json:
            return self._member2json[s]
        return None
    
    def toMember(self, s):
        if s in self._json2member:
            return self._json2member[s]
        return None        
    
    
    
