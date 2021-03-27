import os
import logging
from typing import Union

def get_uid() -> Union[str, None]:
    try:
        # query = "echo ${UID}"
        query = "id -u $(whoami)"
        ret = os.popen(query).read().strip()
        return ret
    except Exception as e:
        logging.info(f"get_uid e: {e}")
        return None


def get_xauthority() -> Union[str, None]:
    try:
        # uid = get_uid()
        # assert uid is not None, "none uid"
        uid = "1000"
        query = "ps a | grep X"
        ret = os.popen(query).read().strip()
        xauthorities = []
        for line in ret.splitlines():
            index = line.find('-auth')
            if index >= 0:
                xauthorities.append(line[index:].split()[1])
        xauthorities = [xauthority for xauthority in xauthorities if xauthority.find(uid) >= 0]
        return xauthorities[0]
    except Exception as e:
        logging.info(f"get_xauthority e: {e}")
        return None


def get_displayid() -> Union[str, None]:
    try:
        query = """
        ps -u $(id -u) -o pid= \
        | xargs -I PID -r cat /proc/PID/environ 2> /dev/null 
        """
        ret = os.popen(query).read().strip().replace('\x00', ' ')
        index = ret.find("DISPLAY=:")
        assert index >= 0, "No DISPLAY"
        display_substr = ret[index:].split()[0]
        assert display_substr.find("DISPLAY=:") >= 0, "No DISPLAY"
        return display_substr
    except Exception as e:
        logging.info(f"get_displayid e: {e}")
        return None


def set_fanspeed(gpu_id: int, fan_speed: int = None) -> bool:
    display = get_displayid()
    if display is None:
        logging.info(f"set_fanspeed: display is None")
        return False

    xauthority = get_xauthority()
    if xauthority is None:
        logging.info(f"set_fanspeed: xauthority is None")
        return False

    if fan_speed is None:
        # set fan control off
        query = f"{display} XAUTHORITY={xauthority} nvidia-settings -a '[gpu:{gpu_id}]/GPUFanControlState=0'"
    else:
        assert 0 <= fan_speed <= 100, f"fan_speed not in limit: {fan_speed}"
        query = f"{display} XAUTHORITY={xauthority} nvidia-settings -a '[gpu:{gpu_id}]/GPUFanControlState=1' -a '[fan:{gpu_id}]/GPUTargetFanSpeed={fan_speed}'"
    try:
        ret = os.popen(query).read().strip()
        if ret.find('assigned') >= 0:
            return True
    except Exception as e:
        logging.error(f"set_fanspeed e: {e}")
        return False
