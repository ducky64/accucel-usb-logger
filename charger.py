from typing import *
import usb1  # type: ignore
import charger_enum
import decoder

# interface code largely from
# https://github.com/thomashenauer/chargemaster-protocol/blob/master/Python%20and%20libusb%20helpers/usb_transaction_testbench.py

class Charger():
  USB_VID = 0x0000
  USB_PID = 0x0001
  INTERFACE = 0
  ENDPOINT = 1

  TIMEOUT_MS = 250

  def __init__(self, deviceNum: Optional[int]=None, verbose=False):
    # Opens the device USB interface
    self.verbose = verbose

    context = usb1.USBContext()
    devices = context.getDeviceList(skip_on_access_error=False, skip_on_error=False)
    devices = list(filter(lambda device:
        device.getVendorID() == self.USB_VID and device.getProductID() == self.USB_PID,
        devices))
    if deviceNum is not None:
      devices = devices[deviceNum:deviceNum+1]
    if len(devices) != 1:
      raise RuntimeError("Found != 1 devices matching VID/PID: %s" % (devices))

    self.handle = devices[0].open()

    if self.handle.kernelDriverActive(self.INTERFACE):
      self.handle.detachKernelDriver(self.INTERFACE)

    if self.handle.kernelDriverActive(self.INTERFACE):
      raise RuntimeError("Error detaching kernel")

    self.handle.claimInterface(self.INTERFACE)

  def close(self):
    # Closes the device USB interface. No more actions may be performed.
    # TODO: can this be part of a destructor?
    self.handle.releaseInterface(self.INTERFACE)

  def get_sys_info(self):
    return decoder.decode_sys_info(self._send_command(charger_enum.Command.GET_SYS_INFO))

  def get_charge_info(self):
    return decoder.decode_charge_info(self._send_command(charger_enum.Command.GET_CHARGE_INFO))

  def _send_command(self, command: charger_enum.Command) -> bytes:
    packet = charger_enum.Command.to_packet(command)
    if self.verbose:
      print("Charger command %s: %s" % (command, packet.hex()))

    done = False
    while not done:
      try:
        self.handle.interruptWrite(self.ENDPOINT, packet, self.TIMEOUT_MS)
        done = True
      except usb1.USBErrorTimeout:
        pass

    result = bytes(self.handle.interruptRead(self.ENDPOINT, 64))
    if self.verbose:
      print("  Result: %s" % result.hex())

    return result
