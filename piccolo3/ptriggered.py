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
from .ptimes import setIntegrationTimes, print_spectrometers
import logging
import signal
import asyncio
import sys
import gpiozero

# Which port is the Pixhawk trigger signal connected to? It should be on GPIO
# port 12, but can be moved if necessary, Avoid ports 5, 17, 18, 22, 23, 24, 25
# and 27 as these are used by the Piccolo's shutters and LEDs.
trigger_port = 12 # Should be on GPIO 12.
reset_port = 20 # used to reset signal


trigger = gpiozero.DigitalInputDevice(trigger_port)
reset   = gpiozero.DigitalOutputDevice(reset_port)

log = logging.getLogger("piccolo.trigger")

async def trigger_loop(pclient,run,nsequence,auto,delay,simulate_trigger):
    while True:
        log.info('waiting for trigger')
        if simulate_trigger:
            await asyncio.sleep(1)
        else:
            while True:
                if trigger.value:
                    break
                await asyncio.sleep(0.1)
        log.debug('got trigger')

        if await pclient.control.get_status() == 'idle':
            log.info('start recording')
            await pclient.control.record_sequence(run,nsequence=nsequence,auto=auto,delay=delay)

        await asyncio.sleep(0.1)
        # reset trigger board
        reset.on()
        await asyncio.sleep(0.01)
        reset.off()

def main():
    parser = piccolo.PiccoloArgumentParser()
    parser.add_argument('-s','--simulate-trigger',action='store_true',default=False,help='trigger every 1 second, useful for debugging')
    parser.addRunOptions()
    parser.addIntegrationTimeOptions()

    args = parser.parse_args()

    piccoloLogging(debug=args.debug)

    if trigger.value:
        # If the trigger signal is high initially this probably indicates an electronics problem. Check the connections. The LED
        log.error('Cannot start Piccolo Client because the Pixhawk trigger signal is active (high). Check that the trigger signal from the Pixhawk is connected and that it is low. The Pixhawk trigger LED should be off.')
        log.info('waiting to reset trigger')
    while trigger.value:
        pass
    log.debug('Finished setting up port ')
    
    
    pclient = piccolo.PiccoloSystem(args.piccolo_url)

    def stop_piccolo(signum, frame):
        pclient.shutdown()
        sys.exit(1)
    for s in [signal.SIGINT,signal.SIGTERM]:
        signal.signal(s,stop_piccolo)
        
    
    loop = asyncio.get_event_loop()
    if args.list_spectrometers:
        loop.run_until_complete(print_spectrometers(pclient))
    else:
        times = {}
        for d in ['upwelling','downwelling','minimal','maximal']:
            times[d] = getattr(args,d)
        loop.run_until_complete(setIntegrationTimes(pclient,times))        
        loop.run_until_complete(trigger_loop(pclient,args.run,args.number_sequences,args.auto,args.delay,args.simulate_trigger))

    pclient.shutdown()

if __name__ == '__main__':
    main()
