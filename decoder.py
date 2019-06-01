from typing import *
import charger_enum


class DecodeException(RuntimeError):
  pass

def decodeAssertEqual(got: Any, expected: Any, msg: str) -> None:
  if got != expected:
    raise DecodeException("%s, got %s != expected %s" % (msg, got, expected))


# We use NamedTuple because it provides immutability and a default useful to-string method
# Ideally we'd use the class-based syntax instead of this dumpster fire, but Raspbian is still on Python 3.5.3 =(
SysInfo = NamedTuple('SysInfo', [
  ('resttime_min', int),  # minutes
  ('safety_timer_min', Optional[int]),  # minutes
  ('capacity_cutout_mah', Optional[int]),  # mAh
  ('keybeep', bool),
  ('buzzer', bool),
  ('input_cutoff_mv', int),  # low-input-voltage cutoff, mV
  ('protection_temp_c', int),  # degrees C
  ('battery_voltage_mv', int),  # mV
  ('cell_voltages_mv', List[int]),  # mV
])

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

ChargeInfo = NamedTuple('ChargeInfo', [
  ('state', 'charger_enum.State'),
  ('capacity_mah', int),
  ('time_s', int),
  ('voltage_mv', int),
  ('current_ma', int),
  ('temp_external_c', int),
  ('temp_internal_c', int),
  ('impedance', int),
  ('cell_voltages_mv', List[int]),  # mV
])

def decode_charge_info(data: bytes) -> ChargeInfo:
  decodeAssertEqual(data[0], 0x0f, "Incorrect header")
  decodeAssertEqual(data[1], 34, "Incorrect packet length")
  decodeAssertEqual(data[2], 0x55, "Incorrect transaction type")

  return ChargeInfo(
    state = charger_enum.State(data[4]),
    capacity_mah = int.from_bytes(data[5:7], 'big'),
    time_s = int.from_bytes(data[7:9], 'big'),
    voltage_mv = int.from_bytes(data[9:11], 'big'),
    current_ma = int.from_bytes(data[11:13], 'big'),
    temp_external_c = data[13],
    temp_internal_c = data[14],
    impedance = int.from_bytes(data[15:17], 'big'),
    cell_voltages_mv = [
      int.from_bytes(data[17:19], 'big'),
      int.from_bytes(data[19:21], 'big'),
      int.from_bytes(data[21:23], 'big'),
      int.from_bytes(data[23:25], 'big'),
      int.from_bytes(data[25:27], 'big'),
      int.from_bytes(data[27:29], 'big'),
    ]
  )
