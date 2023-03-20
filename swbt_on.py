import ui
import cb
import sound
import struct
import time
import binascii


class SwitchBot(object):
    def __init__(self):
        self.peripheral = None

    def did_discover_peripheral(self, p):
        print(p.name, p.uuid, p.state, p.services)
        print("===================")

        if p.name and "WoHand" in p.name and not self.peripheral:
            self.peripheral = p
            print("Connecting to switchbot...")
            cb.connect_peripheral(p)
            cb.stop_scan()

    def did_connect_peripheral(self, p):
        print("Connected:", p.name)
        print("Discovering services...")
        p.discover_services()

    def did_fail_to_connect_peripheral(self, p, error):
        print("Failed to connect: %s" % (error,))

    def did_disconnect_peripheral(self, p, error):
        print("Disconnected, error: %s" % (error,))
        self.peripheral = None

    def did_discover_services(self, p, error):
        for s in p.services:
            print(s)
            print(s.uuid)
            if s.uuid == "CBA20D00-224D-11E6-9FB8-0002A5D5C51B":
                print("switch on or off service, discovering characteristitcs...")
                p.discover_characteristics(s)

    def did_discover_characteristics(self, s, error):
        print("Did discover characteristics...")
        for c in s.characteristics:
            print(c.uuid)
            if c.uuid == "CBA20002-224D-11E6-9FB8-0002A5D5C51B":
                self.peripheral.write_characteristic_value(c, "\x57\x01\x01", True)
                print("On")
                time.sleep(3)
                break

    cb.stop_scan()
    cb.reset()


if __name__ == "__main__":
    try:
        swbt = SwitchBot()
        cb.set_central_delegate(swbt)
        print("Scanning for peripherals...")
        cb.scan_for_peripherals()  # scan開始
    except KeyboardInterrupt:
        cb.reset()
        cb.stop_scan()
