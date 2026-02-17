import time
from smbus2 import SMBus, i2c_msg

I2C_BUS = 2
HDC302x_ADDRESS = 0x47


def HDC302xReset():
    try:
        with SMBus(I2C_BUS) as bus:
            write = i2c_msg.write(HDC302x_ADDRESS, [0x30, 0xA2])
            bus.i2c_rdwr(write)
            time.sleep(0.04)
    except Exception as e:
        print("Reset Error:", e)


def HDC302xRead():
    try:
        with SMBus(I2C_BUS) as bus:

            # Trigger measurement
            write = i2c_msg.write(HDC302x_ADDRESS, [0x24, 0x00])
            bus.i2c_rdwr(write)

            time.sleep(0.04)

            # Read 6 bytes (raw read, no register)
            read = i2c_msg.read(HDC302x_ADDRESS, 6)
            bus.i2c_rdwr(read)

            data = list(read)

            temp_raw = (data[0] << 8) | data[1]
            hum_raw  = (data[3] << 8) | data[4]

            temperature_c = ((temp_raw / 65535.0) * 175.0) - 45.0
            humidity = (hum_raw / 65535.0) * 100.0

            return temperature_c, humidity

    except Exception as e:
        print("Read Error:", e)
        return None, None
