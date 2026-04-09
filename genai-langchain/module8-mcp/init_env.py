import sys
from pathlib import Path

# Add project root to path
module_path = str(Path("../").resolve())
if module_path not in sys.path:
    sys.path.insert(0, module_path)

print(f"Added to Python path: {module_path}")

from llm_utils import setup, create_azure_llm, create_azure_embedding
from pprint import pprint
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader

from mcp.shared.exceptions import McpError
from mcp.types import CallToolResult, TextContent

setup()