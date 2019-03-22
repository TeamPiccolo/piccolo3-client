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
import asyncio

class PiccoloControl(PiccoloClientComponent):

    NAME = "control"

    async def record_sequence(self,run,nsequence=1,auto=-1,delay=0.):
        """start recording a batch

        :param run: name of the current run
        :param nsequence: the number of squences to record
        :param auto: can be -1 for never; 0 once at the beginning; otherwise every nth measurement
        :param delay: delay in seconds between each sequence
        """

        await self.a_put('record_sequence',run,nsequence=nsequence,auto=auto,delay=delay)

    async def record_dark(self,run):
        """record a dark spectrum

        :param run: name of the current run
        """

        await self.a_put('record_dark',run)

    async def get_current_sequence(self):
        return await self.a_get('current_sequence')

    async def get_status(self):
        return await self.a_get('status')


async def main():
    base = 'coap://piccolo-thing2'

    p = PiccoloControl(base)

    print (await p.get_status())

    await p.record_sequence('test_client',nsequence=10)

    for i in range(10):
        print (await p.get_status(),await p.get_current_sequence())
        await asyncio.sleep(0.5)
    
if __name__ == '__main__':
    import time
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
