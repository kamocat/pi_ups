from mcp3428 import ADC
import asyncio

def print_with_units(volts):
    scale = [1e5,1e5,1e5,11]
    mA = '{:.1f}mA'
    V = '{:.3f}V'
    units = [mA,mA,mA,V]
    vals = [units[i].format(scale[i]*volts[i]) for i in range(4)]
    print(vals)


async def main():
    adc = ADC()
    gain = [8,8,8,1]
    print("Initialized")
    while True:
        volts = await adc.get_all(gain)
        print_with_units(volts)
        await asyncio.sleep(1)

task = asyncio.run(main())
