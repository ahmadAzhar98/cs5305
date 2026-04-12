import sys
from pathlib import Path

# Add project root to path
module_path = str(Path("../").resolve())
if module_path not in sys.path:
    sys.path.insert(0, module_path)

print(f"Added to Python path: {module_path}")

from llm_utils import setup, create_azure_llm, create_azure_embedding

setup()