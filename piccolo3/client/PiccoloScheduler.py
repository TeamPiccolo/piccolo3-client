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

__all__ = ['PiccoloScheduler']

from .PiccoloBaseClient import *
import datetime
import asyncio
import json

class PiccoloScheduler(PiccoloClientComponent):

    NAME = "scheduler"

    def __init__(self,baseurl):

        super().__init__(baseurl,path='/control/scheduler')

        self._quietTimeEnabled = None
        self._powerOffEnabled = None
        self._powerDelay = None
        self._quietStart = None
        self._quietEnd  = None

        self._jobs = []
        
        self._callbacks = []
        self.add_task(self._update_quietTimeEnabled())
        self.add_task(self._update_powerOffEnabled())
        self.add_task(self._update_powerDelay())
        self.add_task(self._update_quietStart())
        self.add_task(self._update_quietEnd())
        self.add_task(self._update_jobs())

        self._TIME_FORMAT = "%H:%M:%S%z"
        
    def register_callback(self,cb):
        self._callbacks.append(cb)

    def _create_time(self,t):
        if t is None or isinstance(t,datetime.time):
            return t
        else:
            return datetime.datetime.strptime(t,self._TIME_FORMAT).timetz()
        
    async def _update_quietTimeEnabled(self):
        u = 'quietTimeEnabled'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self._quietTimeEnabled = n
    async def get_quietTimeEnabled(self):
        self._quietTimeEnabled = await self.a_get('quietTimeEnabled')
        return self._quietTimeEnabled
    async def set_quietTimeEnabled(self,n):
        await self.a_put('quietTimeEnabled',n)

    async def _update_powerOffEnabled(self):
        u = 'powerOffEnabled'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self._powerOffEnabled = n
    async def get_powerOffEnabled(self):
        self._powerOffEnabled = await self.a_get('powerOffEnabled')
        return self._powerOffEnabled
    async def set_powerOffEnabled(self,n):
        await self.a_put('powerOffEnabled',n)

    async def _update_powerDelay(self):
        u = 'powerDelay'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self._powerDelay = n
    async def get_powerDelay(self):
        self._powerDelay = await self.a_get('powerDelay')
        return self._powerDelay
    async def set_powerDelay(self,n):
        await self.a_put('powerDelay',n)

    @property
    def quietStart(self):
        return self._quietStart
    @quietStart.setter
    def quietStart(self,t):
        self._quietStart = self._create_time(t)
        
    async def _update_quietStart(self):
        u = 'quietStart'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self.quietStart = n
    async def get_quietStart(self):
        self.quietStart = await self.a_get('quietStart')
        return self.quietStart
    async def set_quietStart(self,n):
        n = self._create_time(n)
        if n != self.quietStart:
            self.quietStart = n
            await self.a_put('quietStart',self.quietStart.strftime(self._TIME_FORMAT))

    @property
    def quietEnd(self):
        return self._quietEnd
    @quietEnd.setter
    def quietEnd(self,t):
        self._quietEnd = self._create_time(t)
        
    async def _update_quietEnd(self):
        u = 'quietEnd'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self.quietEnd = n
    async def get_quietEnd(self):
        self.quietEnd = await self.a_get('quietEnd')
        return self.quietEnd
    async def set_quietEnd(self,n):
        n = self._create_time(n)
        if n != self.quietEnd:
            self.quietEnd = n
            await self.a_put('quietEnd',self.quietEnd.strftime(self._TIME_FORMAT))

    @property
    def jobs(self):
        return self._jobs
    async def _update_jobs(self):
        u = 'jobs'
        async for n in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps({u:n}))
            self._jobs = n
    async def get_jobs(self):
        self._jobs = await self.a_get('jobs')
        return self._jobs
    
    async def suspend(self,jid):
        await self.a_put('suspend',jid)
    
    async def unsuspend(self,jid):
        await self.a_put('unsuspend',jid)
    
    async def delete(self,jid):
        await self.a_put('delete',jid)
    
async def main():
    base = 'coap://piccolo-thing2'

    p = PiccoloScheduler(base)

    print (await p.get_quietStart())
    print (await p.get_quietEnd())

if __name__ == '__main__':
    import time
    import datetime
    import pytz
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
