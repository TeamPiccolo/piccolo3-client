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
from .ptimes import setIntegrationTimes
import datetime
from dateutil.tz import tzlocal
import logging
import time
import sys
import asyncio

TODAY=str(datetime.datetime.now().date())
    
def main():
    parser = piccolo.PiccoloArgumentParser()
    parser.addRunOptions()
    parser.addIntegrationTimeOptions()
    parser.addSchedulerOptions()
    
    args = parser.parse_args()
    piccoloLogging(debug=args.debug)
    
    if args.start:
        start = datetime.datetime.combine(
            datetime.datetime.now(),
            datetime.datetime.strptime(args.start,"%H:%M").time())
        start = start.replace(tzinfo=tzlocal())
        start = str(start)
    else:
        start = None

    if args.stop:
        stop = datetime.datetime.combine(
            datetime.datetime.now(),
            datetime.datetime.strptime(args.stop,"%H:%M").time())
        stop = stop.replace(tzinfo=tzlocal())
        stop = str(stop)
    else:
        stop = None
        
    pclient = piccolo.PiccoloSystem(args.piccolo_url)
    loop = asyncio.get_event_loop()
    if args.list_spectrometers:
        loop.run_until_complete(pclient.spec.pprint())
    else:
        times = {}
        for d in ['upwelling','downwelling','minimal','maximal']:
            times[d] = getattr(args,d)
        loop.run_until_complete(setIntegrationTimes(pclient,times))
        loop.run_until_complete(pclient.control.record_sequence(args.run,
                                                                nsequence=args.number_sequences,
                                                                auto=args.auto,
                                                                delay=args.delay,
                                                                at_time=start,
                                                                interval=args.interval,
                                                                end_time=stop ))
    pclient.shutdown()


if __name__ == '__main__':
    main()
