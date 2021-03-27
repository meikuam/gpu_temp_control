import os
import pandas as pd
import logging
from io import StringIO
from typing import Union


def get_nvidia_smi() -> Union[pd.DataFrame, None]:
    query = "nvidia-smi --query-gpu=gpu_name,temperature.gpu,temperature.memory,utilization.gpu,memory.free,memory.used,memory.total,power.draw,power.limit,fan.speed --format=csv,nounits,noheader"
    try:
        ret = os.popen(query).read()
        return pd.read_csv(
            StringIO(ret),
            header=None,
            names=[
                'name', 'temp.gpu', 'temp.mem',
                'mem.utilization', 'mem.free', 'mem.used', 'mem.total',
                'power.draw', 'power.limit',
                'fan.speed'
            ]
        )
    except Exception as e:
        logging.info(f"get_current e: {e}")
        return None


def set_power_limit(gpu_id: int, power_limit: int) -> bool:
    query = f"nvidia-smi -i {gpu_id} -pl {power_limit}"
    status = os.popen(query).read().strip()
    if "Power limit for GPU" in status and "was set" in status:
        return True
    else:
        return False
