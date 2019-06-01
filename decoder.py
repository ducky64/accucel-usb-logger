from typing import *


class DecodeException(RuntimeError):
  pass

def decodeAssertEqual(got: Any, expected: Any, msg: str) -> None:
  if got != expected:
    raise DecodeException("%s, got %s != expected %s" % (msg, got, expected))


# We use NamedTuple because it provides immutability and a default useful to-string method
class SysInfo(NamedTuple):
  resttime_min: int  # minutes
  safety_timer_min: Optional[int]  # minutes
  capacity_cutout_mah: Optional[int]  # mAh
  keybeep: bool
  buzzer: bool
  input_cutoff_mv: int  # low-input-voltage cutoff, mV
  protection_temp_c: int  # degrees C
  battery_voltage_mv: int  # mV
  cell_voltages_mv: List[int]  # mV

def decode_sys_info(data: bytes) -> SysInfo:
  decodeAssertEqual(data[0], 0x0f, "Incorrect header")
  decodeAssertEqual(data[1], 37, "Incorrect packet length")
  decodeAssertEqual(data[2], 0x5a, "Incorrect transaction type")
  decodeAssertEqual(data[39:41], bytes([0xff, 0xff]), "Incorrect stop sequence")

  return SysInfo(
    resttime_min = data[4],
    safety_timer_min = int.from_bytes(data[6:8], 'big') if data[5] else None,
    capacity_cutout_mah = int.from_bytes(data[9:11], 'big') if data[8] else None,
    keybeep = bool(data[11]),
    buzzer = bool(data[12]),
    input_cutoff_mv = int.from_bytes(data[13:15], 'big'),
    protection_temp_c = data[17],  # suspect, check this
    battery_voltage_mv = int.from_bytes(data[18:20], 'big'),
    cell_voltages_mv = [
      int.from_bytes(data[20:22], 'big'),
      int.from_bytes(data[22:24], 'big'),
      int.from_bytes(data[24:26], 'big'),
      int.from_bytes(data[26:28], 'big'),
      int.from_bytes(data[28:30], 'big'),
      int.from_bytes(data[30:32], 'big'),
    ]
  )
