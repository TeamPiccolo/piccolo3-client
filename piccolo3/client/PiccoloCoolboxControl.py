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

__all__ = ['PiccoloCoolboxControl']

from .PiccoloBaseClient import *
import asyncio


class PiccoloTemperature(PiccoloNamedClientComponent):
    """manage temperature control on coolbox"""

    NAME = "coolboxctrl"

    def __init__(self, baseurl, name):

        super().__init__(baseurl, name)

        self._target_temp = None
        self._current_temp = None

        self._callbacks = []

        self.add_task(self._get_target_temp())
        self.add_task(self._get_current_temp())

    def register_callback(self, cb):
        self._callbacks.append(cb)

    async def _get_target_temp(self):
        u = 'target_temp'
        async for s in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps((self.name, u, s)))
            self._target_temp = s

    async def get_target_temp(self):
        self._targetTemp = await self.a_get('target_temp')
        return self._targetTemp

    async def set_target_temp(self, t):
        await self.a_put('target_temp', float(t))

    async def _get_current_temp(self):
        u = 'current_temp'
        async for s in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps((self.name, u, s)))
            self._current_temp = s

    async def get_current_temp(self):
        self.log.info(self.uri('current_temp'))
        self._current_temp = await self.a_get('current_temp')
        return self._current_temp

    @property
    def target_temp(self):
        return self._target_temp

    @property
    def current_temp(self):
        return self._current_temp


class PiccoloVoltage(PiccoloNamedClientComponent):
    """manage voltage control on coolbox"""

    NAME = "coolboxctrl"

    def __init__(self, baseurl, name):

        super().__init__(baseurl, name)

        self._current_voltage = None

        self._callbacks = []

        self.add_task(self._get_current_voltage())

    def register_callback(self, cb):
        self._callbacks.append(cb)

    async def _get_current_voltage(self):
        u = 'current_voltage'
        async for s in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps((self.name, u, s)))
            self._current_voltage = s

    async def get_current_voltage(self):
        self.log.info(self.uri('current_voltage'))
        self._current_voltage = await self.a_get('current_voltage')
        return self._current_voltage

    @property
    def current_voltage(self):
        return self._current_voltage


class PiccoloCurrent(PiccoloNamedClientComponent):
    """manage current control on coolbox"""

    NAME = "coolboxctrl"

    def __init__(self, baseurl, name):

        super().__init__(baseurl, name)

        self._current_current = None

        self._callbacks = []

        self.add_task(self._get_current_current())

    def register_callback(self, cb):
        self._callbacks.append(cb)

    async def _get_current_current(self):
        u = 'current_current'
        async for s in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps((self.name, u, s)))
            self._current_current = s

    async def get_current_current(self):
        self.log.info(self.uri('current_current'))
        self._current_current = await self.a_get('current_current')
        return self._current_current

    @property
    def current_current(self):
        return self._current_current


class PiccoloFan(PiccoloNamedClientComponent):
    """manage fan control on coolbox"""

    NAME = "coolboxctrl"

    def __init__(self, baseurl, name):

        super().__init__(baseurl, name)

        self._target_fan_state = None
        self._current_fan_state = None

        self._callbacks = []

        self.add_task(self._get_target_fan_state())
        self.add_task(self._get_current_fan_state())

    def register_callback(self, cb):
        self._callbacks.append(cb)

    async def _get_target_fan_state(self):
        u = 'target_fan_state'
        async for s in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps((self.name, u, s)))
            self._target_fan_state = s

    async def get_target_fan_state(self):
        self._fanState = await self.a_get('target_fan_state')
        return self._fanState

    async def set_target_fan_state(self, t):
        await self.a_put('target_fan_state', float(t))

    async def _get_current_fan_state(self):
        u = 'current_fan_state'
        async for s in self.a_observe(u):
            for cb in self._callbacks:
                await cb(json.dumps((self.name, u, s)))
            self._current_fan_state = s

    async def get_current_fan_state(self):
        self.log.info(self.uri('current_fan_state'))
        self._current_fan_state = await self.a_get('current_fan_state')
        return self._current_fan_state

    @property
    def target_fan_state(self):
        return self._target_fan_state

    @property
    def current_fan_state(self):
        return self._current_fan_state


class PiccoloCoolboxControl(PiccoloClientComponent):
    """manage temperature control on coolbox"""

    NAME = "coolboxctrl"

    def __init__(self, baseurl):
        super().__init__(baseurl)

        self._temperature_sensors = {}
        self._fan_sensors = {}
        self._current_sensors = {}
        self._voltage_sensors = {}

        self._temps = None
        self._fans = None
        self._currents = None
        self._voltages = None

        self._callbacks = []

        self.add_task(self._init_temperature_sensors())
        self.add_task(self._init_fan_sensors())
        self.add_task(self._init_current_sensors())
        self.add_task(self._init_voltage_sensors())

    async def _init_temperature_sensors(self):
        sensors = await self.get_temperature_sensors()
        for t in sensors:
            if t not in self.temperature_sensors:
                self.temperature_sensors[t] = PiccoloTemperature(
                    self.baseurl, t)
                for c in self._callbacks:
                    self.temperature_sensors[t].register_callback(c)

    async def _init_fan_sensors(self):
        sensors = await self.get_fan_sensors()
        for t in sensors:
            if t not in self.fan_sensors:
                self.fan_sensors[t] = PiccoloFan(
                    self.baseurl, t)
                for c in self._callbacks:
                    self.fan_sensors[t].register_callback(c)

    async def _init_current_sensors(self):
        sensors = await self.get_current_sensors()
        for t in sensors:
            if t not in self.current_sensors:
                self.current_sensors[t] = PiccoloCurrent(
                    self.baseurl, t)
                for c in self._callbacks:
                    self.current_sensors[t].register_callback(c)

    async def _init_voltage_sensors(self):
        sensors = await self.get_voltage_sensors()
        for t in sensors:
            if t not in self.voltage_sensors:
                self.voltage_sensors[t] = PiccoloVoltage(
                    self.baseurl, t)
                for c in self._callbacks:
                    self.voltage_sensors[t].register_callback(c)

    def register_callback(self, cb):
        self._callbacks.append(cb)
        for t in self.temperature_sensors:
            self.temperature_sensors[t].register_callback(cb)

    def shutdown_tasks(self):
        for t in self.temperature_sensors:
            self.temperature_sensors[t].shutdown_tasks()
        for t in self.fan_sensors:
            self.fan_sensors[t].shutdown_tasks()
        for t in self.current_sensors:
            self.current_sensors[t].shutdown_tasks()
        for t in self.voltage_sensors:
            self.voltage_sensors[t].shutdown_tasks()
        super().shutdown_tasks()

    async def get_temperature_sensors(self):
        if self._temps is None:
            self._temps = await self.a_get('temperature_sensors')
        return self._temps

    async def get_fan_sensors(self):
        if self._fans is None:
            self._fans = await self.a_get('fan_sensors')
        return self._fans

    async def get_current_sensors(self):
        if self._currents is None:
            self._currents = await self.a_get('current_sensors')
        return self._currents

    async def get_voltage_sensors(self):
        if self._voltages is None:
            self._voltages = await self.a_get('voltage_sensors')
        return self._voltages

    @property
    def temperature_sensors(self):
        return self._temperature_sensors

    @property
    def fan_sensors(self):
        return self._fan_sensors

    @property
    def voltage_sensors(self):
        return self._voltage_sensors

    @property
    def current_sensors(self):
        return self._current_sensors


async def main():
    base = 'coap://localhost'

    coolbox = PiccoloCoolboxControl(base)
    await asyncio.sleep(1)

    for i in range(10):
        for temp in coolbox.temperature_sensors:
            print(temp,
                  coolbox.temperature_sensors[temp].current_temp)
        await asyncio.sleep(1)
    coolbox.shutdown_tasks()
    await asyncio.sleep(5)

if __name__ == '__main__':
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
