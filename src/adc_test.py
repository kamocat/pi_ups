from mcp3428 import ADC
import asyncio

async def main():
    adc = ADC()
    gain = [8,8,8,1]
    print("Initialized")
    while True:
        volts = await adc.get_all(gain)
        print(volts)
        await asyncio.sleep(1)

task = asyncio.run(main())
