from charger import Charger

import charger_enum

if __name__ == '__main__':
  charger = Charger()
  print(charger.get_sys_info())
  print(charger.get_charge_info())
  print(charger._send_command(charger_enum.Command.GET_CHARGE_INFO).hex())

  charger.close()
