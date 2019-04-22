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
import datetime
from dateutil.tz import tzlocal
import argparse
import logging
import time
import sys
import asyncio

TODAY=str(datetime.datetime.now().date())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--piccolo-url',metavar='URL',default='coap://localhost',help='set the URL of the piccolo server, default coap://localhost')
    parser.add_argument('--debug', action='store_true',default=False,help="enable debugging output")
    parser.add_argument('-r','--run',metavar='RUN',default=TODAY,help='name of the run, default = %s'%TODAY)
    parser.add_argument('-a','--auto',metavar='A',type=int,default=-1,help="autointegrate, when A=0 only before the first sequence, if A>0 autointegrate every Ath sequence")
    parser.add_argument('-n','--number-sequences',metavar='N',type=int,default=1,help="set the number of sequences, default=1")
    parser.add_argument('-d','--delay',type=float,metavar='D',default=0.,help="delay between measurements in m, default=0")
    parser.add_argument('--start',metavar='HH:MM',help="start recording at HH:MM in local time zone")
    parser.add_argument('--interval',type=float,help="recrod a new batch every INTERVAL seconds")
    parser.add_argument('--stop',metavar='HH:MM',help="stop recording after HH:MM in local time zone")
    parser.add_argument('-v','--version',action='store_true',default=False,help="print version and exit")

    args = parser.parse_args()

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
    loop.run_until_complete(pclient.control.record_sequence(args.run,
                                                            nsequence=args.number_sequences,
                                                            auto=args.auto,
                                                            delay=args.delay,
                                                            at_time=start,
                                                            interval=args.interval,
                                                            end_time=stop ))


if __name__ == '__main__':
    main()
