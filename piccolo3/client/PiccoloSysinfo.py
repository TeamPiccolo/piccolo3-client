# Copyright 2014-2016 The Piccolo Team
#
# This file is part of piccolo3-client.
#
# piccolo3-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo3-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo3-client.  If not, see <http://www.gnu.org/licenses/>.

"""
.. moduleauthor:: Magnus Hagdorn <magnus.hagdorn@ed.ac.uk>

"""

__all__ = ['PiccoloSysinfo']

from .PiccoloBaseClient import *

class PiccoloSysinfo(PiccoloClientComponent):

    NAME = "sysinfo"

    @property
    def cpu(self):
        return self.get('cpu')
    @property
    def mem(self):
        return self.get('mem')
    @property
    def host(self):
        return self.get('host')
    @property
    def clock(self):
        return self.get('clock')
    @clock.setter
    def clock(self,data):
        self.put('clock',data)

if __name__ == '__main__':
    import time
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    base = 'coap://piccolo-thing2'

    p = PiccoloSysinfo(base)

    print (p.host)
    for i in range(5):
        print (p.clock,p.cpu,p.mem)
        time.sleep(1)

    #p.clock = 'blub'
