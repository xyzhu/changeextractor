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
# Authors: Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>

import sys

def to_utf8(string):
    if isinstance(string, unicode):
        return str(string.encode('utf-8'))
    elif isinstance(string, bytes):
        for encoding in ['ascii', 'utf-8', 'iso-8859-15']:
            try:
                s = unicode(string, encoding)
            except:
                continue
            break

        return str(s.encode('utf-8'))
    else:
        return string




def printout(str='\n', args=None):
    if args is not None:
        str = str % tuple(to_utf8(arg) for arg in args)
    
    if str != '\n':
        str += '\n'
    sys.stdout.write(to_utf8(str))
    sys.stdout.flush()


def printerr(str='\n', args=None):
    if args is not None:
        str = str % tuple(to_utf8(arg) for arg in args)
    
    if str != '\n':
        str += '\n'
    sys.stderr.write(to_utf8(str))
    sys.stderr.flush()


def printdbg(str='\n', args=None):
    printout("DBG: " + str, args)

def save_result(content,save_file):
    f = open(save_file,'w+')
    f.write(content)
    f.close()