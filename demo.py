import argparse
import csv
import time

from charger import Charger

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Charger logger')

  parser.add_argument('outfile', type=argparse.FileType('w'))
  parser.add_argument('--verbose', action='store_true',
                      help='dump hex transactions')
  args = parser.parse_args()

  charger = Charger(verbose=args.verbose)
  print(charger.get_sys_info())

  writer = csv.writer(args.outfile)
  # TODO: log individual cells
  writer.writerow(['time [%s]' % time.strftime('%z', time.gmtime()),
                   'time (s)', 'state', 'voltage (mV)', 'current (mA)', 'capacity (mAh)',
                   'temp, external (C)', 'temp, internal (C)', 'impedance'])

  try:
    last_state_time = (None, 0)
    while True:
      now = time.gmtime()
      charge_info = charger.get_charge_info()

      # We oversample so the wall clock time is more accurate, but it appears the charger doesn't update info more often
      # than 1 second, so we can discard duplicates.
      if charge_info.state == last_state_time[0] and charge_info.time_s == last_state_time[1]:
        continue
      last_state_time = (charge_info.state, charge_info.time_s)

      writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S', now),
          charge_info.time_s, charge_info.state.to_abbrev(),
          charge_info.voltage_mv, charge_info.current_ma, charge_info.capacity_mah,
          charge_info.temp_external_c, charge_info.temp_internal_c, charge_info.impedance])
      print("%s  %s T+%3dm %2ds    %2d.%03d V, %2d.%03d A, %2d.%03d Ah    %2d Ce, %2d Ci  %d" % (
        time.strftime('%H:%M:%S', now), charge_info.state.to_abbrev(),
        charge_info.time_s // 60, charge_info.time_s % 60,
        charge_info.voltage_mv // 1000, charge_info.voltage_mv % 1000,
        charge_info.current_ma // 1000, charge_info.current_ma % 1000,
        charge_info.capacity_mah // 1000, charge_info.capacity_mah % 1000,
        charge_info.temp_external_c, charge_info.temp_internal_c,
        charge_info.impedance,
      ))
      time.sleep(0.2)

  except KeyboardInterrupt:
    print("Interrupted")

  charger.close()
