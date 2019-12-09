# Copyright 2018- The Piccolo Team
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

__all__ = ['PiccoloClientComponent','PiccoloNamedClientComponent']

import asyncio
import aiocoap
import json
import logging
import os.path
import time

class PiccoloClientComponent:
    NAME = 'component'
    NRETRIES = 3600

    __protocol = None
    __lock = asyncio.Lock()
    
    def __init__(self,baseurl,path=None):
        self._log = logging.getLogger(self.logName)
        self._protocol = None
        self._baseurl = baseurl
        self._path = path
        self._tasks = []
        self.log.debug("initialised")

    @property
    def baseurl(self):
        return self._baseurl
    @property
    def path(self):
        if self._path is None:
            return '/'+self.NAME
        else:
            return self._path
    def uri(self,resource=None):
        if resource is None:
            return self.baseurl+self.path
        else:
            if resource.startswith('/'):
                return self.baseurl+resource
            else:
                return self.baseurl+os.path.join(self.path,resource)
    @property
    def logName(self):
        return 'piccolo.client.{0}'.format(self.NAME)
    @property
    def log(self):
        """get the logger"""
        return self._log

    def add_task(self,task):
        loop = asyncio.get_event_loop()
        t = loop.create_task(task)
        self._tasks.append(t)
    
    def handle_response(self,response):
        p = response.payload.decode()
        if response.code.is_successful():
            if len(p) > 0:
                return json.loads(response.payload.decode())
        else:
            raise RuntimeError('{}: {}'.format(
                response.code,p))

    async def isConnected(self):
        p = await self.get_protocol()
        return p is not None
        
    async def get_protocol(self):
        if self.__protocol is None:
            async with self.__lock:
                if self.__protocol is None:
                    self.log.info('create client context')
                    # try talking to server
                    for i in range(self.NRETRIES):
                        if i==1:
                            self.log.warning('waiting for connection')
                        try:
                            self.__protocol = await aiocoap.Context.create_client_context()
                            request = aiocoap.Message(code=aiocoap.GET,uri=self.uri(resource='/control/status'))
                            p_request = self.__protocol.request(request)
                            response = await p_request.response
                            break
                        except ConnectionRefusedError as e:
                            if i%10 == 0:
                                self.log.error(e)
                            self.__protocol.shutdown()
                            await asyncio.sleep(1)
                            continue
                    else:
                        raise RuntimeError('5.00: failed after {} retries'.format(self.NRETRIES))
                else:
                    self.log.debug('client context appeared')
        return self.__protocol

    async def shutdown(self):
        async with self.__lock:
            if self.__protocol is not None:
                self.log.info('shutting down client context')
                await self.__protocol.shutdown()
                self.__protocol = None
            else:
                self.log.debug('client context already disappeared')
                
    async def a_get(self,resource):
        protocol = await self.get_protocol()
        request = aiocoap.Message(code=aiocoap.GET,uri=self.uri(resource))
        p_request = protocol.request(request)

        response = await p_request.response
        return self.handle_response(response)
        
    async def a_put(self,resource,*args,**kwargs):
        payload = json.dumps([args,kwargs]).encode()
        
        protocol = await self.get_protocol()
        request = aiocoap.Message(code=aiocoap.PUT,
                                  payload = payload,
                                  uri=self.uri(resource))
        response = await protocol.request(request).response
        return self.handle_response(response)

    async def a_observe(self,resource):
        protocol = await self.get_protocol()

        request = aiocoap.Message(code=aiocoap.GET,uri=self.uri(resource),observe=0)

        pr = protocol.request(request)
        r = await pr.response
        yield self.handle_response(r)

        async for r in pr.observation:
            yield self.handle_response(r)
        
    def get(self,resource):
        return asyncio.get_event_loop().run_until_complete(self.a_get(resource))

    def put(self,resource,*args,**kwargs):
        return asyncio.get_event_loop().run_until_complete(self.a_put(resource,*args,**kwargs))

class PiccoloNamedClientComponent(PiccoloClientComponent):
    """
    a client component with a name
    """

    NAME = 'named_component'

    def __init__(self,baseurl,name,path=None):
        """
        :param name: name of the component
        """

        self._name = name
        super().__init__(baseurl,path=path)
        
    @property
    def name(self):
        """the name of the component"""
        return self._name

    @property
    def logName(self):
        return 'piccolo.client.{0}.{1}'.format(self.NAME,self.name)
 
    @property
    def path(self):
        if self._path is None:
            return os.path.join('/',self.NAME,self.name)
        else:
            return self._path

    
if __name__ == '__main__':
    from piccolo3.common import piccoloLogging
    piccoloLogging(debug=True)
    
    client = PiccoloClientComponent('coap://piccolo-thing2')
        
    if True:
        print (client.get('/sysinfo/clock'))



    if False:
        async def observe():
           protocol = await aiocoap.Context.create_client_context()
           #request = aiocoap.Message(code=aiocoap.GET,uri='coap://piccolo-thing2/data_dir/current_run',observe=0)
           request = aiocoap.Message(code=aiocoap.GET,uri='coap://piccolo-thing2/spectrometer/S_instrument_simulator_2/min_time',observe=0)

           pr = protocol.request(request)
           r = await pr.response
           print("First response: %s\n%r"%(r, r.payload))

           async for r in pr.observation:
              print("Next result: %s\n%r"%(r, r.payload))

        #asyncio.get_event_loop().run_until_complete(observe())
        loop = asyncio.get_event_loop()
        loop.create_task(observe())
        print('here')
        loop.run_forever()

