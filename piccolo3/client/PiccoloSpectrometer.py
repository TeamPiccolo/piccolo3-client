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

__all__ = ['PiccoloSpectrometers']

from .PiccoloBaseClient import *
import asyncio

import os.path
import json
import time

class PiccoloSpectrometer(PiccoloNamedClientComponent):
    NAME = "spectrometer"
    
    def __init__(self,baseurl,name,channels):

        super().__init__(baseurl,name)

        self._channels = channels
        self._min_time = None
        self._max_time = None
        self._current_time = {}
        self._auto_status = {}

        self._callbacks = []
        
        loop = asyncio.get_event_loop()
        loop.create_task(self._update_min_time())
        loop.create_task(self._update_max_time())
        for c in self.channels:
            loop.create_task(self._update_current_time(c))
            loop.create_task(self._update_auto_status(c))
            
    @property
    def channels(self):
        return self._channels

    def register_callback(self,cb):
        self._callbacks.append(cb)
    
    async def _update_min_time(self):
        u = 'min_time'
        async for t in self.a_observe(u):
           for cb in self._callbacks:
               await cb(json.dumps((self.name,u,t)))
           self._min_time = t
    async def get_min_time(self):
        self._min_time = await self.a_get('min_time')
        return self._min_time
    async def set_min_time(self,t):
        await self.a_put('min_time',t)

    async def _update_max_time(self):
        u = 'max_time'
        async for t in self.a_observe('max_time'):
           for cb in self._callbacks:
               await cb(json.dumps((self.name,u,t)))
           self._max_time = t
    async def get_max_time(self):
        self._max_time = await self.a_get('max_time')
        return self._max_time
    async def set_max_time(self,t):
        await self.a_put('max_time',t)

    async def _update_current_time(self,c):
        u = 'current_time/'+c
        async for t in self.a_observe(u):
           for cb in self._callbacks:
               await cb(json.dumps((self.name,u,t)))
           self._current_time[c] = t
    async def get_current_time(self,c):
        self._current_time[c] = await self.a_get('current_time/'+c)
        return self._current_time[c]
    async def set_current_time(self,c,t):
        await self.a_put('current_time/'+c,t)

    async def _update_auto_status(self,c):
        u = 'autointegration/'+c
        async for t in self.a_observe(u):
           for cb in self._callbacks:
               await cb(json.dumps((self.name,u,t)))
           self._auto_status[c] = t
    async def get_auto_status(self,c):
        self._auto_status[c] = await self.a_get('autointegration/'+c)
        return self._auto_status[c]
        
    async def get_status(self):
        s = await self.a_get('status')
        return s
        
    @property
    def min_time(self):
        return self._min_time
    @property
    def max_time(self):
        return self._max_time
        
    def get_current_time(self,channel):
        return self._current_time[channel]
    
class PiccoloSpectrometers(PiccoloClientComponent):

    NAME = "spectrometers"
    
    def __init__(self,baseurl):
        super().__init__(baseurl,path='/spectrometer')

        self._spectrometers = {}
        self._specs = None
        self._channels = None
        self._callbacks = []

        loop = asyncio.get_event_loop()
        loop.create_task(self._init_spectrometers())

    async def _init_spectrometers(self):
        channels = await self.get_channels()
        specs = await self.get_spectrometers()
        for s in specs:
            if s not in self._spectrometers:
                self._spectrometers[s] = PiccoloSpectrometer(self.baseurl,s,channels)
                for c in self._callbacks:
                    self._spectrometers[s].register_callback(c)

    def register_callback(self,cb):
        self._callbacks.append(cb)
        for s in self.keys():
            self[s].register_callback(cb)

    async def get_spectrometers(self):
        if self._specs is None:
            self._specs = await self.a_get('spectrometers')
        return self._specs
            
    async def get_channels(self):
        if self._channels is None:
            self._channels = await self.a_get('channels')
        return self._channels
            
    # implement methods so object can act as a read-only dictionary
    def keys(self):
        return self._spectrometers.keys()
    def __getitem__(self,s):
        return self._spectrometers[s]
    def __len__(self):
        return len(self._spectrometers)
    def __iter__(self):
        for s in self.keys():
            yield s
    def __contains__(self,s):
        return s in self._spectrometers
    

async def main():
    base = 'coap://piccolo-thing2'

    spectrometers = PiccoloSpectrometers(base)

    for i in range(10):

        for s in spectrometers:
            print (spectrometers[s].name,spectrometers[s].min_time,spectrometers[s].max_time,spectrometers[s].channels)
            for channel in spectrometers[s].channels:
                print (spectrometers[s].name,channel,spectrometers[s].get_current_time(channel))
            print (await spectrometers[s].get_status())

        print('\n')
            
        await asyncio.sleep(1)

if __name__ == '__main__':
    import time
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
