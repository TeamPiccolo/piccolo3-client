import asyncio
from piccolo3 import client as piccolo

# the URL of the piccolo3 server
URL = 'coap://piccolo-thing2'

# the name of the run
RUN = 'test'
# the number of sequences to record
NSEQ = 5
# use autointegration
AUTO = False
# delay between sequences in s
DELAY = 0
# start time, should be a datetime.datetime object
START = None
# interval in seconds between batches
INTERVAL = None
# end time, should be a datetime.datetime object
END = None


async def main():
    # the piccolo3 client uses asyncio
    # use a coroutine to communicate with piccolo server

    # connect to server
    pclient = piccolo.PiccoloSystem(URL)

    # get current status and sequence
    print(await pclient.control.get_status(),
          await pclient.control.get_current_sequence())

    # show list of connected spectormeters
    print(await pclient.spec.get_spectrometers())

    # for the example we use the first spectrometer
    s = (await pclient.spec.get_spectrometers())[0]
    print(s)
    await asyncio.sleep(1)
    print('status', await pclient.spec[s].get_status())
    # get min/max integration time
    print('min,max', await pclient.spec[s].get_min_time(),
          await pclient.spec[s].get_max_time())
    # set the min/max times
    await pclient.spec[s].set_min_time(10)
    await pclient.spec[s].set_max_time(20000)
    print('min,max',
          await pclient.spec[s].get_min_time(),
          await pclient.spec[s].get_max_time())

    # get the channels
    print('channels', pclient.spec[s].channels)

    # get the current time
    for c in pclient.spec[s].channels:
        print(c, await pclient.spec[s].get_current_time(c))
    # set the current times
    for c in pclient.spec[s].channels:
        await pclient.spec[s].set_current_time(c, 200)

    # record some data
    await pclient.control.record_sequence(RUN,
                                          nsequence=NSEQ,
                                          auto=AUTO,
                                          delay=DELAY,
                                          at_time=START,
                                          interval=INTERVAL,
                                          end_time=END)


if __name__ == '__main__':
    from piccolo3.common import piccoloLogging
    piccoloLogging()

    # start event loop and run piccolo program until complete
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    loop.run_until_complete(main())
