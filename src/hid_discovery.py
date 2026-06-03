import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from hid_setup import setup_dll
setup_dll()
import hid
import json

if __name__ == '__main__':
    for device in hid.enumerate():
        # print(device)
        ...
        
    devices_enumerated = hid.enumerate()
    print(type(devices_enumerated))

    current_folder = Path(__file__).parent
    dump_file = current_folder / '.data' /'devices.json'
    dump_file.parent.mkdir(parents=True, exist_ok=True)
    with open(dump_file, 'w', encoding='utf-8') as f:
        json.dump(devices_enumerated, f, ensure_ascii=False, indent=4,
              default=lambda x: x.decode('utf-8', errors='replace') if isinstance(x, bytes) else str(x))
    
    