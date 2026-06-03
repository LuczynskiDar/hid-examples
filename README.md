# hid-examples

Python HID examples and tests — device enumeration, report reading, input validation.

---

## Choosing a library

Two main Python packages are available for HID communication:

| Library | pip | GitHub | Windows |
|---|---|---|---|
| `hid` | `pip install hid` | https://github.com/apmorton/pyhidapi | **recommended** — pure Python wrapper, straightforward setup |
| `hidapi` | `pip install hidapi` | https://github.com/trezor/cython-hidapi | use with caution — Cython wrapper, may require a compiler |
| `pywinusb` | `pip install pywinusb` | — | yes — Windows-native, no DLL required |

**On Windows use `hid`.** The `hidapi` package is a Cython wrapper — if pip cannot find a prebuilt wheel for your Python version, it will attempt to compile from source, which can be problematic on Windows.

---

## Installing `hid` on Windows

`pip install hid` **is not enough** — it is only the Python wrapper. You also need the native DLL.

### Step 1 — install the Python package

```bash
pip install hid
```

### Step 2 — download hidapi.dll

From the libusb/hidapi releases page on GitHub:

```
https://github.com/libusb/hidapi/releases
```

Download `hidapi-win.zip`. Inside you will find two folders: `x64` and `x86`.

### Step 3 — check your Python architecture

```bash
python -c "import struct; print(struct.calcsize('P') * 8)"
```

- Output `64` → use `x64/hidapi.dll`
- Output `32` → use `x86/hidapi.dll`

### Step 4 — place the DLL where Windows can find it

**With venv (recommended):** put `hidapi.dll` in the `Scripts` folder of your venv:

```
venv/Scripts/hidapi.dll
```

Windows looks for DLLs in the directory of the running executable — `python.exe` in a venv lives in `Scripts/`.

**Alternative — via code (Python 3.8+):**

```python
import os
os.add_dll_directory(r"C:\path\to\folder\with\dll")
import hid
```

`os.add_dll_directory` is the official Python 3.8+ way on Windows — no need to touch system environment variables.

**Other options (without venv):**

- next to your `.py` script
- `C:\Windows\System32` (for 64-bit)
- Python installation folder (`C:\Python3x\`)

---

## Verification

```python
import hid

print(hid.enumerate())  # lists all connected HID devices

# read details of a specific device (change vid/pid to match yours)
with hid.Device(0x046d, 0xc534) as h:
    print(f'Manufacturer: {h.manufacturer}')
    print(f'Product:      {h.product}')
    print(f'Serial:       {h.serial}')
```

If you get `OSError: hidapi not found` — the DLL is in the wrong place or is the wrong architecture.

---

## Installing `hidapi` (trezor/cython-hidapi)

Cython wrapper — more feature-rich, validated on hardware wallets (TREZOR), PIC microcontrollers, weather stations.

```bash
pip install hidapi
```

On Linux the default backend is `hidraw`. To switch to `libusb`:

```bash
HIDAPI_WITH_LIBUSB=1 pip install hidapi
```

On Linux a udev rule file may be needed after installation — without it the device may be inaccessible without sudo.

---

## References

- https://stackoverflow.com/questions/70894915/cant-load-hidapi-with-python-library-hid-on-windows
- https://github.com/libusb/hidapi/releases
- https://github.com/apmorton/pyhidapi
- https://github.com/trezor/cython-hidapi
