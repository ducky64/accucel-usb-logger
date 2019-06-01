import unittest

from decoder import decode_sys_info

class TestDecode(unittest.TestCase):
  def test_decode(self):
    reply = bytes.fromhex('0f255a000a010168011f40000127100000500cc801290125013c013601410142000000000000d3ffff0000000000000000000000000000000000000000000000')
    decoded = decode_sys_info(reply)
    self.assertEqual(decoded.resttime_min, 10)
    self.assertEqual(decoded.safety_timer_min, 360)
    self.assertEqual(decoded.capacity_cutout_mah, 8000)
    self.assertEqual(decoded.keybeep, False)
    self.assertEqual(decoded.buzzer, True)
    self.assertEqual(decoded.input_cutoff_mv, 10000)
    self.assertEqual(decoded.protection_temp_c, 80)
    self.assertEqual(decoded.battery_voltage_mv, 3272)
    self.assertEqual(decoded.cell_voltages_mv, [
      297, 293, 316, 310, 321, 322
    ])

    # Testvector from chargemaster-protocol analyzeReply_testbench
    reply = bytes.fromhex('0f255a00000100b4011f4001012af80000502e04100a100e100f017d0150014800000000000084ffff0000000000000000000000000000000000000000000000')
    decoded = decode_sys_info(reply)
    self.assertEqual(decoded.resttime_min, 0)
    self.assertEqual(decoded.safety_timer_min, 180)
    self.assertEqual(decoded.capacity_cutout_mah, 8000)
    self.assertEqual(decoded.keybeep, True)
    self.assertEqual(decoded.buzzer, True)
    self.assertEqual(decoded.input_cutoff_mv, 11000)
    self.assertEqual(decoded.protection_temp_c, 80)
    self.assertEqual(decoded.battery_voltage_mv, 11780)
    self.assertEqual(decoded.cell_voltages_mv, [
      4106, 4110, 4111, 381, 336, 328
    ])
