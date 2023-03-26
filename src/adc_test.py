import time
import sqlite3
from mcp3428 import ADC
import asyncio

con = sqlite3.connect("battery.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS ups(time INTEGER, input1 REAL, input2 REAL, consumption REAL, volts REAL);")

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
    mA = 1e5
    volts = 11
    while True:
        vals = await adc.get_all(gain)
        data = (int(time.time()), 
            vals[0]*mA, 
            vals[1]*mA, 
            vals[2]*mA, 
            vals[3]*volts)
        cur.execute("INSERT INTO ups VALUES (?,?,?,?,?)", data)
        con.commit()
        print_with_units(vals)
        await asyncio.sleep(1)

task = asyncio.run(main())
