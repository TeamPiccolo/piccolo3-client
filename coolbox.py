import asyncio
from piccolo3 import client as piccolo

# the URL of the piccolo3 server
URL = 'coap://localhost'

# the piccolo3 client uses asyncio
# use a coroutine to communicate with piccolo server
async def main(pclient):

    await asyncio.sleep(1)
    print (pclient.coolbox.temperature_sensors.keys())

    for i in range(10):
        for temp in pclient.coolbox.temperature_sensors:
            print (temp,pclient.coolbox.temperature_sensors[temp].current_temp)
        await asyncio.sleep(1)


    
if __name__ == '__main__':
    from piccolo3.common import piccoloLogging
    piccoloLogging()

    # connect to server
    pclient = piccolo.PiccoloSystem(URL)
        
    # start event loop and run piccolo program until complete
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    loop.run_until_complete(main(pclient))

    pclient.shutdown()
