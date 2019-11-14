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
import json

class PiccoloControl(PiccoloClientComponent):

    NAME = "control"

    def __init__(self,baseurl):

        super().__init__(baseurl)

        self._numSequences = None
        self._autointegration = None
        self._delay = None
        self._target = None
        
        self._callbacks = []
        self.add_task(self._update_status())
        self.add_task(self._update_numSequences())
        self.add_task(self._update_autointegration())
        self.add_task(self._update_delay())
        self.add_task(self._update_target())

    def register_callback(self,cb):
        self._callbacks.append(cb)
        
    async def _update_numSequences(self):
        u = 'numSequences'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self._numSequences = n
    async def get_numSequences(self):
        self._numSequences = await self.a_get('numSequences')
        return self._numSequences
    async def set_numSequences(self,n):
        await self.a_put('numSequences',n)

    async def _update_autointegration(self):
        u = 'autointegration'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self._autointegration = n
    async def get_autointegration(self):
        self._autointegration = await self.a_get('autointegration')
        return self._autointegration
    async def set_autointegration(self,n):
        await self.a_put('autointegration',n)

    async def _update_delay(self):
        u = 'delay'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self._delay = n
    async def get_delay(self):
        self._delay = await self.a_get('delay')
        return self._delay
    async def set_delay(self,n):
        await self.a_put('delay',n)

    async def _update_target(self):
        u = 'target'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self._target = n
    async def get_target(self):
        self._target = await self.a_get('target')
        return self._target
    async def set_target(self,n):
        await self.a_put('target',n)

        
    async def record_sequence(self,run=None,nsequence=None,auto=None,delay=None, target=None,at_time=None,interval=None,end_time=None):
        """start recording a batch

        :param run: name of the current run
        :param nsequence: the number of squences to record
        :param auto: can be -1 for never; 0 once at the beginning; otherwise every nth measurement
        :param delay: delay in seconds between each sequence
        :param target: target saturation percentage for autointegration
        :param at_time: the time at which the job should run or None
        :param interval: repeated scheduled run if interval is not set to None
        :param end_time: the time after which the job is no longer scheduled
        """

        if at_time is not None:
            at_time = str(at_time)
        if end_time is not None:
            end_time = str(end_time)
        
        await self.a_put('record_sequence',run=run,nsequence=nsequence,auto=auto,delay=delay,target=target,at_time=at_time,interval=interval,end_time=end_time)

    async def record_dark(self,run=None):
        """record a dark spectrum

        :param run: name of the current run
        """

        await self.a_put('record_dark',run=run)

    async def auto(self,target=None):
        """autointegrate

        :param target: target saturation percentage for autointegration
        """

        await self.a_put('auto',target=target)
        
    async def pause(self):
        """pause data acquisition"""

        await self.a_get('pause')
        
    async def abort(self):
        """abort data acquisition"""

        await self.a_get('abort')

    async def get_current_sequence(self):
        return await self.a_get('current_sequence')

    async def _update_status(self):
        async for s in self.a_observe('status'):
           for cb in self._callbacks:
               await cb(json.dumps({'status':s}))
    async def get_status(self):
        return await self.a_get('status')


async def main():
    base = 'coap://localhost'

    p = PiccoloControl(base)

    print (await p.get_status())

    #await p.record_sequence('test_client',nsequence=10)
    if False:


        for i in range(10):
            print (await p.get_status(),await p.get_current_sequence())
            await asyncio.sleep(0.5)

    now = datetime.datetime.now(tz=pytz.utc)
    await p.record_sequence('test_client',nsequence=10,at_time=now+datetime.timedelta(seconds=15))
    
    await asyncio.sleep(10)
    
    #for i in range(30):
    #    print (await p.get_status(),await p.get_current_sequence())
    #    await asyncio.sleep(1)                 
    
if __name__ == '__main__':
    import time
    import datetime
    import pytz
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
