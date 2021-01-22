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

from piccolo3 import client as piccolo
from piccolo3.common import piccoloLogging
import asyncio


async def setIntegrationTimes(pclient, times):
    specs = await pclient.spec.get_spectrometers()
    for d in times:
        for i in times[d]:
            try:
                s, t = i.split(':')
            except ValueError:
                print(f'cannot parse {i}')
                continue
            if s in specs:
                if d in ['upwelling', 'downwelling']:
                    await pclient.spec[s].set_current_time(d, t)
                elif d == 'minimal':
                    await pclient.spec[s].set_min_time(t)
                elif d == 'maximal':
                    await pclient.spec[s].set_max_time(t)
                else:
                    print(f'unkown channel {d}')
            else:
                print(f'unknown spectrometers {s}')
    await asyncio.sleep(1)


def main():
    parser = piccolo.PiccoloArgumentParser()
    parser.addIntegrationTimeOptions()

    args = parser.parse_args()

    piccoloLogging(debug=args.debug)

    pclient = piccolo.PiccoloSystem(args.piccolo_url)
    loop = asyncio.get_event_loop()
    if args.list_spectrometers:
        loop.run_until_complete(pclient.spec.pprint())
    else:
        times = {}
        for d in ['upwelling', 'downwelling', 'minimal', 'maximal']:
            times[d] = getattr(args, d)
        loop.run_until_complete(setIntegrationTimes(pclient, times))

    pclient.shutdown()


if __name__ == '__main__':
    main()
