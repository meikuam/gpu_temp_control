import os
import sys
import time
import logging

sys.path.append('.')

from src.nvidia_smi import set_power_limit, get_nvidia_smi
from src.nvidia_settings import set_fanspeed


if __name__ == "__main__":

    logging.basicConfig(
        # filename='messages.log',
        format="%(asctime)-15s %(message)s'",
        level=logging.INFO
    )

    sleep_time = 2
    speed_delta = 0.25
    target_temp = 60
    stats = get_nvidia_smi()
    fan_speed = stats['fan.speed'].astype(float)
    print('fanspeed', fan_speed)

    while True:
        stats = get_nvidia_smi()
        message = ""
        for i, row in stats.iterrows():
            temp = row['temp.gpu']
            temp_delta = temp - target_temp
            fan_speed[i] = max(min(fan_speed[i] + temp_delta * speed_delta, 100.0), 0.0)
            if set_fanspeed(gpu_id=i, fan_speed=int(fan_speed[i])):
            	pass
            message += f" gpu {i} temp {row['temp.gpu']} speed {fan_speed[i]}"
        print(message)
        time.sleep(sleep_time)

