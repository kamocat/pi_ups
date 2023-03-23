from mcp3428 import ADC
import asyncio

async def main():
    adc = ADC()
    gain = [8,8,8,1]
    while true:
        volts = await adc.get_all(gain)
        print(volts)
        await asyncio.sleep(1000)

task = asyncio.run(main())
