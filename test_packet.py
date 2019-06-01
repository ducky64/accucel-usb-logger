import unittest

from charger_enum import Command

class TestPacket(unittest.TestCase):
  def test_command_packet(self):
    self.assertEqual(Command.to_packet(Command.GET_SYS_INFO), bytes([0x0f, 0x03, 0x5a, 0x00, 0x5a, 0xff, 0xff]))
