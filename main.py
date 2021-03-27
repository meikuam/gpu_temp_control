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
    target_temp = 60
    stats = get_nvidia_smi()
    fan_speed = stats['fan.speed']
    print('fanspeed', fan_speed)

    while True:
        stats = get_nvidia_smi()
        for i, row in stats.iterrows():
            temp = row['temp.gpu']
            if temp > target_temp:
                fan_speed[i] = min(fan_speed[i] + 5, 100)
            elif temp < target_temp:
                fan_speed[i] = max(fan_speed[i] - 5, 0)
            if temp != target_temp:
                if set_fanspeed(gpu_id=i, fan_speed=fan_speed[i]):
                    print("gpu", i, "set fanspeed", fan_speed[i])
        time.sleep(sleep_time)

