'''jsoncls - A library for mapping between JSON and Python objects

Created on Apr 2, 2013

@author: schlameel
@copyright: Schlameel
@license: GPL v3.0
'''

from jsoncls.jsonClsBase import JsonCls
from jsoncls.member import Member, IntMember, LongMember, FloatMember, StringMember, BoolMember, CustomMember
from jsoncls.mapper import CamelMapper, DirectMapper, Mapper, InitialCapsMapper, NamedMapper
from jsoncls.core import json_dumps
from jsoncls.memberSet import MemberSet

__author__ = "John McCormick"
__copyright__ = "Copyright 2013, John McCormick"
__credits__ = ["John McCormick"]
__license__ = "GPL 3.0"
__version__ = "0.1.0"
__maintainer__ = "John McCormick"
__status__ = "Alpha"

VERSION = (0, 1, 0, 'alpha', 0)

def get_version(version=None):
    """Derives a PEP386-compliant version number from VERSION."""
    if version is None:
        version = VERSION
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        # At the toplevel, this would cause an import loop.
        from django.utils.version import get_svn_revision
        svn_revision = get_svn_revision()[4:]
        if svn_revision != 'unknown':
            sub = '.dev%s' % svn_revision

    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub
