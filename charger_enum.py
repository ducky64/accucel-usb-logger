from enum import IntEnum


# Constants from https://github.com/maciek134/libb6/blob/4e330d50963a8eb95dc88e156dcc85d40cfee91c/Enum.hh

class Command(IntEnum):
  GET_DEV_INFO = 0x57
  GET_SYS_INFO = 0x5a
  GET_CHARGE_INFO = 0x55
  STOP_CHARGING = 0xfe

  @classmethod
  def _calculate_checksum(cls, packet: bytes):
    return bytes([sum(packet[2:]) % 256])

  @classmethod
  def to_packet(cls, command: 'Command'):
    # Ideally we'd use from __future__ import annotations, but Raspbian is still on Python 3.5.3 =(
    packet = bytes([0x0f, 0x03, command, 0x00])
    packet = packet + cls._calculate_checksum(packet) + bytes([0xff, 0xff])
    return packet

class ChargingModeLi(IntEnum):
  STANDARD = 0x00
  DISCHARGE = 0x01
  STORAGE = 0x02
  FAST = 0x03
  BALANCE = 0x04

class ChargingModeNi(IntEnum):
  STANDARD = 0x00
  AUTO = 0x01
  DISCHARGE = 0x02
  REPEAK = 0x03
  CYCLE = 0x04

class ChargingModePb(IntEnum):
  CHARGE = 0x00
  DISCHARGE = 0x01

class BatteryType(IntEnum):
  LIPO = 0x00
  LIIO = 0x01
  LIFE = 0x02
  LIHV = 0x03
  NIMH = 0x04
  NICD = 0x05
  PB = 0x06

class State(IntEnum):
  CHARGING = 0x01
  ERROR_1 = 0x02
  COMPLETE = 0x03
  ERROR_2 = 0x04

  def to_abbrev(self):
    return {
        self.CHARGING: 'CHG',
        self.ERROR_1: 'ER1',
        self.COMPLETE: 'FIN',
        self.ERROR_2: 'ER2',
      }[self]

class Error(IntEnum):
  CONNECTION_BROKEN_1 = 0x000b
  CELL_VOLTAGE_INVALID = 0x000c
  BALANCE_CONNECTION = 0x000d
  NO_BATTERY = 0x000e
  CELL_NUMBER_INCORRECT = 0x000f
  CONNECTION_MAIN_PORT = 0x0010
  BATTERY_FULL = 0x0011
  CHARGE_NOT_NEEDED = 0x0012
  CELL_HIGH_VOLTAGE = 0x0013
  CONNECTION_BROKEN_2 = 0x0014
  CONNECTION_BROKEN_3 = 0x0015
  CONNECTION_BROKEN_4 = 0x0016
  INT_TEMP_TOO_HIGH = 0x0100
  EXT_TEMP_TOO_HIGH = 0x0200
  DC_IN_TOO_LOW = 0x0300
  DC_IN_TOO_HIGH = 0x0400
  OVER_TIME_LIMIT = 0x0500
  OVER_CAPACITY_LIMIT = 0x0600
  REVERSE_POLARITY = 0x0700

  CONTROL_FAIL = 0x0800
  BREAK_DOWN = 0x0900
  INPUT_FAIL = 0x1000

  UNKNOWN = 0xffff
