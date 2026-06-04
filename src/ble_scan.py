import asyncio
import json, os
from pathlib import Path
from bleak import BleakClient, BleakScanner

from dotenv import load_dotenv

load_dotenv()

QCY7_ADDRESS = os.getenv('QCY7_ADDRESS')

current_folder = Path(__file__).parent
dump_file = current_folder / '.data' /'ble_devices.json'
dump_file.parent.mkdir(parents=True, exist_ok=True)

async def scan():

    # devices = await BleakScanner.discover()
    # for d in devices:
    #     print(d.address, d.name)   
    
    export = []
    
    devices = await BleakScanner.discover(return_adv=True)
    for address, (device, adv) in devices.items():
        print(f"Name:     {device.name}")
        print(f"Address:  {address}")
        print(f"RSSI:     {adv.rssi}")
        print(f"Services: {adv.service_uuids}")
        print(f"Mfr data: {adv.manufacturer_data}")
        print("---")

        export.append({
            'name': device.name,
            'address': address,
            'rssi': adv.rssi,
            'services': adv.service_uuids,
            'mfr_data': adv.manufacturer_data
        })

    
    with open(dump_file, 'w', encoding='utf-8') as f:
        json.dump(export, f, ensure_ascii=False, indent=4,
            default=lambda x: x.decode('utf-8', errors='replace') if isinstance(x, bytes) else str(x))

async def connect():
    async with BleakClient(QCY7_ADDRESS) as client:
        services = client.services
        for service in services:
            print(f"Service: {service.description} | {service.uuid}")
            for char in service.characteristics:
                print(f"  Char: {char.description} | {char.uuid} | {char.properties}")

async def device_name():
    async with BleakClient(QCY7_ADDRESS) as client:
        
        services = client.services
        device_name_char = 'Device Name'
        device_name_uuid = ''
        for service in services:
            for char in service.characteristics:
                if char.description == device_name_char:
                    device_name_uuid = char.uuid
                    break
            
        name = await client.read_gatt_char(device_name_uuid)
        print(name.decode("utf-8"))

async def selected_characteristics():
    
    async with BleakClient(QCY7_ADDRESS) as client:
        
        defined_services = ['ATT', 'OBEX']
        seen = []
        check_srvcs = {}
        
        services = client.services
        for service in services:
            for char in service.characteristics:
                if char.description in defined_services and char.description not in seen:
                    seen.append(char.description)
                    check_srvcs[char.description] = {
                        'uuid': char.uuid,
                        'properties': char.properties
                    }
        for k, v in check_srvcs.items():
            data = await client.read_gatt_char(v['uuid'])
            print(f"{k} | {'uuid'}: 0x{data.hex()}")
    
async def notify_with_data_change():
       
  def handler(sender, data):
      print(f"Raw: {data.hex()}")
      print(f"Bytes: {list(data)}")

  async with BleakClient(QCY7_ADDRESS) as client:
        seen = []
        check_srvcs = {}
        
        services = client.services
        for service in services:
            for char in service.characteristics:
                if 'notify' in char.properties and char.uuid not in seen:
                    seen.append(char.uuid)
                    check_srvcs = {
                        'description': char.description,
                        'uuid': char.uuid,
                        'properties': char.properties
                    }
                    break
                    
        await client.start_notify(check_srvcs['uuid'], handler)
        
        await asyncio.sleep(60)
  
async def main():
    if not dump_file.exists():
        await scan()

    await connect()
    await device_name()
    await selected_characteristics()
    await notify_with_data_change()
      
if __name__ == '__main__':

    asyncio.run(main())