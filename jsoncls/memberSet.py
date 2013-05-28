'''
Created on Apr 4, 2013
@copyright: John McCormick
@license: GPL v3.0
@author: john
'''

class MemberSet(object):
    '''MemberSet defines a set of members that can be included in a .json() call.
    
    Example:
    >>> import jsoncls
    >>> class SampleClass(jsoncls.JsonCls):
    ...     foo = jsoncls.Member()
    ...     bar = jsoncls.Member()
    ...     baz = jsoncls.Member()
    ...     qux = jsoncls.Member()
    ...     early_set = jsoncls.MemberSet(foo, bar)
    ... 
    >>> sc = SampleClass()
    >>> sc.foo = 1
    >>> sc.bar = 2
    >>> print sc.json(member_set=sc.early_set)
    {"foo": 1, "bar": 2}
    '''
    name = None
    members = []

    def __init__(self, *args, **kwargs):
        '''Class constructor
        '''
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'members' in kwargs:
            self.members = kwargs['members']
        else:
            self.members = []
            for member in args:
                self.members.append(member)
            
