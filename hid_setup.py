"""
Call setup_dll() before `import hid` to register the bundled hidapi.dll.

Usage in production code:
    from hid_setup import setup_dll
    setup_dll()
    import hid

The correct DLL (x64 or x86) is chosen automatically based on the
running Python interpreter's pointer size.
"""

import os
import struct
import pathlib


def setup_dll() -> None:
    """Add the bundled hidapi.dll directory to the Windows DLL search path."""
    arch = "x64" if struct.calcsize("P") == 8 else "x86"
    dll_dir = pathlib.Path(__file__).parent / "hidapi-win" / arch
    os.add_dll_directory(str(dll_dir))
