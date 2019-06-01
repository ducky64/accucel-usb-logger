from charger import Charger

if __name__ == '__main__':
  charger = Charger()
  print(charger.get_sys_info())

  charger.close()
