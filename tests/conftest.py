import sys, os
import pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from hid_setup import setup_dll
setup_dll()
import hid
import json
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def hid_fixture():
    return hid