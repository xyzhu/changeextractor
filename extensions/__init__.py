# Copyright (C) 2008 LibreSoft
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors :
#       Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>

import os
from glob import glob
from pycvsanaly2.utils import printdbg

__all__ = ['Extension', 'get_extension', 'register_extension']


class ExtensionUnknownError(Exception):
    '''Unknown extension'''


class ExtensionRunError(Exception):
    '''Error running extension'''
    
    
class ExtensionBackoutError(Exception):
    '''Error backing out data created by extension'''


class Extension(object):

    deps = []
    
    def run(self, repo, uri, db):
        raise NotImplementedError
    
from pycvsanaly2.utils import printerr


_extensions = {}


def register_extension(extension_name, extension_class):
    _extensions[extension_name] = extension_class


def get_extension(extension_name):
    if extension_name not in _extensions:
        try:
            __import__("extensions.%s" % extension_name)
        except ImportError as e:
            printerr("Error in importing extension %s: %s", 
                     (extension_name, str(e)))

    if extension_name not in _extensions:
        raise ExtensionUnknownError('Extension %s not registered' % \
                                    extension_name)

    return _extensions[extension_name]


def get_all_extensions():
    # Do something to get a list of extensions, probably like a file
    # glob, then do a get_extension on each one. Return the entire
    # _extensions list
    
    # Get a list of the paths that are sitting in the directory with this
    # script, ie. all possible extensions
    possible_file_paths = glob(os.path.realpath(os.path.dirname(__file__)) \
                               + "/*.py")
    
    # This splitting will extract the file name from the expression.
    # The list has special Python files, like __init.py__ filtered.
    for extension in [os.path.splitext(os.path.split(fp)[1])[0] for 
                      fp in possible_file_paths if (not fp.startswith('__')
                      and not fp.endswith('__.py'))]:
        try:
            printdbg("Getting extension " + extension)
            get_extension(extension)
        except ExtensionUnknownError:
            pass
        
    return _extensions
