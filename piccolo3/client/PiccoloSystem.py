# Copyright 2014-2016 The Piccolo Team
#
# This file is part of piccolo3-server.
#
# piccolo3-server is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo3-server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo3-server.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ['PiccoloSystem']

from .Piccolo import *
from .PiccoloDataDir import *
from .PiccoloSysinfo import *
from .PiccoloSpectrometer import *
from .PiccoloScheduler import *
from .PiccoloCoolboxControl import *
from .PiccoloBaseClient import PiccoloClientBase

import asyncio

class PiccoloSystem(PiccoloClientBase):
    NAME = None
    def __init__(self,baseurl):
        super().__init__()
        self.control = PiccoloControl(baseurl)
        self.scheduler = PiccoloScheduler(baseurl)
        self.sys = PiccoloSysinfo(baseurl)
        self.coolbox = PiccoloCoolboxControl(baseurl)
        self.spec = PiccoloSpectrometers(baseurl)
        self.data = PiccoloDataDir(baseurl)

    async def _wait(self):
        self.log.debug('waiting for tasks')
        for task in asyncio.Task.all_tasks():
            try:
                await task
            except asyncio.CancelledError:
                continue
        self.log.debug('all tasks done')
        
    def shutdown(self):
        self.log.debug('shutting down')
        self.control.shutdown_tasks()
        self.scheduler.shutdown_tasks()
        self.sys.shutdown_tasks()
        self.coolbox.shutdown_tasks()
        self.spec.shutdown_tasks()
        self.data.shutdown_tasks()

        loop = asyncio.get_event_loop()
        loop.create_task(self._wait())
