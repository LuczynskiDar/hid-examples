import asyncio
from bleak import BleakScanner

async def scan():
    # devices = await BleakScanner.discover()
    # for d in devices:
    #     print(d.address, d.name)
  devices = await BleakScanner.discover(return_adv=True)
  for address, (device, adv) in devices.items():
      print(f"Name:     {device.name}")
      print(f"Address:  {address}")
      print(f"RSSI:     {adv.rssi}")
      print(f"Services: {adv.service_uuids}")
      print(f"Mfr data: {adv.manufacturer_data}")
      print("---")


if __name__ == '__main__':
    asyncio.run(scan())

