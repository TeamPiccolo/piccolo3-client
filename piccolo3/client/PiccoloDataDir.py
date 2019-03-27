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

__all__ = ['PiccoloDataDir']

from .PiccoloBaseClient import *
import asyncio, aiocoap

class PiccoloRunDir(PiccoloNamedClientComponent):
    NAME = 'run'

    def __init__(self,baseurl,name):
        super().__init__(baseurl,name,path='/data_dir/runs/'+name)

        self._current_batch = None

    def __str__(self):
        return self.name
        
    async def get_current_batch(self):
        self._current_batch = await self.a_get('current_batch')
        return self._current_batch

    @property
    def current_batch(self):
        return self._current_batch

class PiccoloDataDir(PiccoloClientComponent):
    """manage piccolo output data directory"""

    NAME = 'data_dir'

    def __init__(self,baseurl):
        super().__init__(baseurl)

        self._datadir = None
        self._current_run = None
        self._runs = {}
        loop = asyncio.get_event_loop()
        loop.create_task(self._init_runs())
        loop.create_task(self._update_current_run())

    async def _init_runs(self):
        runs = await self.a_put('all_runs')
        for r in runs:
            if r not in self._runs:
                self._runs[r] = PiccoloRunDir(self.baseurl,r)

    async def _update_current_run(self):
        async for r in self.a_observe('current_run'):
            if r not in self._runs:
                self._runs[r] = PiccoloRunDir(self.baseurl,r)
            self._current_run = self._runs[r]
                
    async def get_mount(self):
        r = await self.a_get('mount')
        return r
    async def set_mount(self,m):
        await self.a_put('mount',m)

    async def get_datadir(self):
        if self._datadir is None:
            self._datadir = await self.a_get('datadir')
        return self._datadir
        
    async def get_current_run(self):
        run = await self.a_get('current_run')
        if run not in self._runs:
            self._runs[run] = PiccoloRunDir(self.baseurl,run)
        self._current_run = self._runs[run]
        return self._current_run
    async def set_current_run(self,run):
        if isinstance(run,PiccoloRunDir):
            run = run.name
        await self.a_put('current_run',run)
        
    @property
    def current_run(self):
        return self._current_run

        
    # implement methods so object can act as a read-only dictionary
    def keys(self):
        return self._runs.keys()
    def __getitem__(self,r):
        return self._runs[r]
    def __len__(self):
        return len(self._runs)
    def __iter__(self):
        for r in self._runs.keys():
            yield r
    def __contains__(self,r):
        return r in self._runs

    

async def main():
    base = 'coap://piccolo-thing2'

    dataDir = PiccoloDataDir(base)
    m = await dataDir.get_mount()
    print (m)

    run = await dataDir.get_current_run()
    b = await run.get_current_batch()    
    print (run.name,b)

    await dataDir.set_current_run('magi_19')
    run = await dataDir.get_current_run()
    print (run.name)
    for i in range(10):
        print (dataDir.current_run)
        await asyncio.sleep(1)
    
    run = await dataDir.get_current_run()
    print (run.name)
    
    await asyncio.sleep(30)
    
    print (dataDir.keys())

        
if __name__ == '__main__':
    import time
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
