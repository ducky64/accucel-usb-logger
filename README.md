# accucel-usb-logger
CSV logger for Accucel-6 80W (with microUSB port) and compatible (Charge Master protocol) devices.

Written in Python 3 against Python 3.5.3 which is currently the latest supported by Raspbian.

## Usage

`python3 demo.py log.csv`

will connect to the charger and record charge data (time, battery voltage, current, capacity) once a second (the maximum rate supported by the charger) to both the specified .csv file and the console.

### Dependencies

You will need Python3 and libusb1.

Under Ubuntu, you can:
```
sudo apt install python3 python3-libusb1
```

### Architecture Overview
- `charger.py` contains a Charger class that opens the USB interface and provides high-level functions (eg, get sys info, get charge info) from the charger.
  This can be used as a library.
- `decoder.py` contains functions to decode received packets (as `bytes`) into structured NamedTuples. Also contains definitions for said NamedTuples.
- `charger_enum.py` contains protocol constants. 

### Static Checking & Testing

This project uses static type annotations. If you have it installed, invoke mypy with:
```
mypy --check-untyped-defs .
``` 

Run unit tests with:
```
python -m unittest discover
```

## Acknowledgments

- Overall interface strategy, some protocol structure, and a test case from [chargemaster-protocol](https://github.com/thomashenauer/chargemaster-protocol), which is a Pyhon2 library for interfacing with and decoding Charge Master devices. However, it does not provide CSV capability, nor is the decoder written to provide an API. 
- Additional protocol structure from [libb6](https://github.com/maciek134/libb6) and [ChargeGuru](https://github.com/maciek134/charge-guru), which interfaces with Charge Master devices in a C++ and QT-based GUI. Its README, at the time this software was written, indicates that it does not have CSV capability.
