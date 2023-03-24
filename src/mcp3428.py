from smbus2 import SMBus, i2c_msg
import asyncio

lock = asyncio.Lock()

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

class ADC:
    def __init__(self,address=0x68):
        self.addr = address
        self.bus = SMBus(1)
    
    async def get(self,channel: int,gain: int=1):
        channel &= 3
        #Log-2 of gain
        if gain < 2:
            gain = 0
        elif gain < 4:
            gain = 1
        elif gain < 8:
            gain = 2
        else:
            gain = 3
        
        cfg = (channel << 5) | gain | 0x88
        async with lock:
            self.bus.write_byte(self.addr, cfg)
            await asyncio.sleep(0.1) 
            #SMBus requires that we write to a register
            #so we re-write the config byte without restarting the conversion
            data = self.bus.read_i2c_block_data(self.addr,cfg&0x7f,3)
        if(data[2] & 0x80):
            print("Conversion not completed.")
        
        #Convert to volts
        scale = (0.5 ** gain) * 0.001/16
        volts = data[0]<<8 | data[1] 
        #volts = hex(volts)
        volts = sign_extend(volts, 16)
        volts *= scale
        return volts

    async def get_all(self,gain):
        return [await self.get(i,gain[i]) for i in range(len(gain))]

