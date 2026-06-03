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
TARGET_INTERFACE = int(os.getenv('TARGET_INTERFACE'))

if __name__ == '__main__':
        
    devices_enumerated = hid.enumerate()

    current_folder = Path(__file__).parent
    dump_file = current_folder / '.data' /'devices.json'
    dump_file.parent.mkdir(parents=True, exist_ok=True)
    if not dump_file.exists():
        with open(dump_file, 'w', encoding='utf-8') as f:
            json.dump(devices_enumerated, f, ensure_ascii=False, indent=4,
                default=lambda x: x.decode('utf-8', errors='replace') if isinstance(x, bytes) else str(x))

    devices = hid.enumerate(DEC_DELL_ID, DEC_PROD_ID)
    device = next(d for d in devices if d['interface_number'] == TARGET_INTERFACE)
    print(f"product_id={device['product_id']} interface={device['interface_number']}  usage_page={device['usage_page']}  path={device['path']}")

    with hid.Device(path=device['path']) as h:
        while True:
            h.nonblocking = True
            report = h.read(64)
            if report:
                print(f"interface={device['interface_number']}  dane: {report}")
  
