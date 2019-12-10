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

__all__ = ['PiccoloArgumentParser']

import argparse
import datetime

TODAY=str(datetime.datetime.now().date())

class PiccoloArgumentParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()

        self.add_argument('-u','--piccolo-url',metavar='URL',default='coap://localhost',help='set the URL of the piccolo server, default coap://localhost')
        self.add_argument('-l','--list-spectrometers',action='store_true',default=False,help="list connected spectormeters and exist")
        self.add_argument('--debug', action='store_true',default=False,help="enable debugging output")
        self.add_argument('-v','--version',action='store_true',default=False,help="print version and exit")


    def add_argument(self,*args,**keyargs):
        self._parser.add_argument(*args,**keyargs)

    def add_argument_group(self,*args,**keyargs):
        return self._parser.add_argument_group(*args,**keyargs)

    def parse_args(self,*args,**keyargs):
        return self._parser.parse_args(*args,**keyargs)
        
    def addRunOptions(self):
        group = self.add_argument_group('run options')
        group.add_argument('-r','--run',metavar='RUN',default=TODAY,help='name of the run, default = %s'%TODAY)
        group.add_argument('-a','--auto',metavar='A',type=int,default=-1,help="autointegrate, when A=0 only before the first sequence, if A>0 autointegrate every Ath sequence")
        group.add_argument('-n','--number-sequences',metavar='N',type=int,default=1,help="set the number of sequences, default=1")
        group.add_argument('-d','--delay',type=float,metavar='D',default=0.,help="delay between measurements in ms, default=0")

    def addIntegrationTimeOptions(self):
        group = self.add_argument_group('integration time options')
        for tc,ts in [('D','downwelling'),
                      ('U','upwelling'),
                      ('N','minimal'),
                      ('X','maximal')]:
            sname = '-'+tc
            lname = '--'+ts+'-integration-time'
            hlp = "set the {} integration time of spectrometer NAME to TIME (in ms)".format(ts)
            group.add_argument(sname,lname,dest=ts,default=[],nargs='*',metavar="NAME:TIME",help=hlp)

    def addSchedulerOptions(self):
        group = self.add_argument_group('scheduler options')
        group.add_argument('--start',metavar='HH:MM',help="start recording at HH:MM in local time zone")
        group.add_argument('--interval',type=float,help="recrod a new batch every INTERVAL seconds")
        group.add_argument('--stop',metavar='HH:MM',help="stop recording after HH:MM in local time zone")
    
if __name__ == '__main__':

    parser = PiccoloArgumentParser()
    parser.addRunOptions()
    parser.addSchedulerOptions()
    parser.addIntegrationTimeOptions()
    args = parser.parse_args()

