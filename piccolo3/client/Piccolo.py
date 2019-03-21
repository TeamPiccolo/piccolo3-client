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

__all__ = ['PiccoloControl']

from .PiccoloBaseClient import *

class PiccoloControl(PiccoloClientComponent):

    NAME = "control"

    def record_sequence(self,run,nsequence=1,auto=-1,delay=0.):
        """start recording a batch

        :param run: name of the current run
        :param nsequence: the number of squences to record
        :param auto: can be -1 for never; 0 once at the beginning; otherwise every nth measurement
        :param delay: delay in seconds between each sequence
        """

        self.put('record_sequence',run,nsequence=nsequence,auto=auto,delay=delay)

    def record_dark(self,run):
        """record a dark spectrum

        :param run: name of the current run
        """

        self.put('record_dark',run)

    @property
    def current_sequence(self):
        return self.get('current_sequence')

    @property
    def status(self):
        return self.get('status')


if __name__ == '__main__':
    import time
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    base = 'coap://piccolo-thing2'

    p = PiccoloControl(base)

    print (p.status)

    p.record_sequence('test_client',nsequence=10)

    for i in range(10):
        print (p.status,p.current_sequence)
        time.sleep(0.5)
    
