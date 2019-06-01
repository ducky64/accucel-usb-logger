# accucel-usb-logger
CSV logger for Accucel-6 80W (with microUSB port) and compatible (Charge Master) chargers

## Usage

You will need Python3 and libusb1.

Under Ubuntu, you can:
```
sudo apt install python3 python3-libusb1
```

### Architecture Overview

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

- Overall implementation strategy, most protocol structure, and test case from [chargemaster-protocol](https://github.com/thomashenauer/chargemaster-protocol), which is a Pyhon2 library for interfacing with and decoding Charge Master devices. However, it does not provide CSV capability, nor is the decoder written to provide an API. 
- Additional protocol structure from [libb6](https://github.com/maciek134/libb6) and [ChargeGuru](https://github.com/maciek134/charge-guru), which interfaces with Charge Master devices in a C++ and QT-based GUI. Its README, at the time this software was written, indicates that it does not have CSV capability.
