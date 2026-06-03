import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from hid_setup import setup_dll
setup_dll()
import hid
import json
from dotenv import load_dotenv

load_dotenv()

DEC_PROD_ID = int(os.getenv('DEVICE_DEC_ID'))
DEC_DELL_ID = 16700

if __name__ == '__main__':
    for device in hid.enumerate():
        # print(device)
        ...
        
    devices_enumerated = hid.enumerate()

    current_folder = Path(__file__).parent
    dump_file = current_folder / '.data' /'devices.json'
    dump_file.parent.mkdir(parents=True, exist_ok=True)
    if not dump_file.exists():
        with open(dump_file, 'w', encoding='utf-8') as f:
            json.dump(devices_enumerated, f, ensure_ascii=False, indent=4,
                default=lambda x: x.decode('utf-8', errors='replace') if isinstance(x, bytes) else str(x))
    
    with hid.Device(DEC_DELL_ID, DEC_PROD_ID) as h:
        print(f'Manufacturer: {h.manufacturer}')
        print(f'Product:      {h.product}')
        print(f'Serial:       {h.serial}')
        
        # report = h.get_feature_report(0x00, 64)
        # print(report)

        for _ in range(20):          # odczytaj 20 raportów
            report = h.read(64)      # blokuje do momentu gdy mysz wyśle dane
            print(report)