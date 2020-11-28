import asyncio
from piccolo3 import client as piccolo

# the URL of the piccolo3 server
URL = 'coap://192.168.1.99'

# the piccolo3 client uses asyncio
# use a coroutine to communicate with piccolo server


async def main(pclient):

    await asyncio.sleep(1)
    print(pclient.coolbox.temperature_sensors.keys())

    for i in range(10):
        for temp in pclient.coolbox.temperature_sensors:
            print("main 1, temp:", i, temp,
                  pclient.coolbox.temperature_sensors[temp].current_temp)
            print("main 2, temp:", i, temp,
                  pclient.coolbox.temperature_sensors[temp].target_temp)
        for fan in pclient.coolbox.fan_sensors:
            print("main 3, fan:", i, fan,
                  pclient.coolbox.fan_sensors[fan].target_fan_state)
        for volt in pclient.coolbox.voltage_sensors:
            print("main 4:", i, volt,
                  pclient.coolbox.voltage_sensors[volt].current_voltage)
        for current in pclient.coolbox.current_sensors:
            print("main 5:", i, current,
                  pclient.coolbox.current_sensors[current].current_current)
            print("\n")
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
