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

from .PiccoloBaseClient import PiccoloClientComponent
import asyncio


class PiccoloSysinfo(PiccoloClientComponent):

    NAME = "sysinfo"

    def __init__(self, baseurl):
        super().__init__(baseurl)
        self._host = None
        self._server_version = None

    async def get_cpu(self):
        c = await self.a_get('cpu')
        return c

    async def get_mem(self):
        m = await self.a_get('mem')
        return m

    async def get_host(self):
        if self._host is None:
            self._host = await self.a_get('host')
        return self._host

    async def get_server_version(self):
        if self._server_version is None:
            self._server_version = await self.a_get('version')
        return self._server_version

    async def get_clock(self):
        c = await self.a_get('clock')
        return c

    async def get_info(self):
        info = {}
        info['cpu'] = await self.get_cpu()
        info['mem'] = await self.get_mem()
        return info

    async def set_clock(self, data):
        await self.a_put('clock', data)


async def main():
    base = 'coap://piccolo-thing2'

    p = PiccoloSysinfo(base)

    print(await p.get_host())
    for i in range(5):
        c = await p.get_clock()
        info = await p.get_info()

        print(c, info['cpu'], info['mem'])
        await asyncio.sleep(1)


if __name__ == '__main__':
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
