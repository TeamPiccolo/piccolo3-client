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

import os.path
import json
import time

class PiccoloSpectrometer(PiccoloNamedClientComponent):
    NAME = "spectrometer"
    
    def __init__(self,baseurl,name):

        super().__init__(baseurl,name)

    @property
    def min_time(self):
        return self.get('min_time')
    @min_time.setter
    def min_time(self,t):
        self.put('min_time',t)
    @property
    def max_time(self):
        return self.get('max_time')
    @max_time.setter
    def max_time(self,t):
        self.put('max_time',t)

    @property
    def status(self):
        return self.get('status')
        
    def get_current_time(self,channel):
        return self.get(os.path.join('current_time',channel))
    def set_current_time(self,channel,t):
        return self.put(os.path.join('current_time',channel))
    
class PiccoloSpectrometers(PiccoloClientComponent):

    NAME = "spectrometers"
    
    def __init__(self,baseurl):
        super().__init__(baseurl,path='/spectrometer')

        self._spectrometers = {}
        
        for s in self.get('spectrometers'):
            self._spectrometers[s] = PiccoloSpectrometer(baseurl,s)

    @property
    def spectrometers(self):
        return self._spectrometers
            
    # implement methods so object can act as a read-only dictionary
    def keys(self):
        return self.spectrometers.keys()
    def __getitem__(self,s):
        return self.spectrometers[s]
    def __len__(self):
        return len(self.spectrometers)
    def __iter__(self):
        for s in self.keys():
            yield s
    def __contains__(self,s):
        return s in self.spectrometers
    
if __name__ == '__main__':
    import time
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)

    base = 'coap://piccolo-thing2'

    if True:
        spectrometers = PiccoloSpectrometers(base)

        for s in spectrometers:
            print (spectrometers[s].name,spectrometers[s].min_time,spectrometers[s].max_time)
            for channel in ['upwelling','downwelling']:
                print (spectrometers[s].name,channel,spectrometers[s].get_current_time(channel))
            print (spectrometers[s].status)
            print('\n')

    else:
        spectrometer = PiccoloSpectrometer(client,'S_instrument_simulator_2')
        print(spectrometer.min_time)

        spectrometer.min_time = 6
        
        for i in range(20):
            print(spectrometer.min_time)
            time.sleep(1)
        


