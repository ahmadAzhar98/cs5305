from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv
import sys
import asyncio
import subprocess
import io
from pathlib import Path
from pprint import pprint

import mcp.client.stdio as _mcp_stdio

if sys.platform == "win32":
    # Patch MCP's Windows stdio transport to avoid fileno() errors.
    # Jupyter replaces sys.stderr (and sys.__stderr__) with a fake OutStream
    # that raises UnsupportedOperation on fileno(). MCP's Windows subprocess
    # fallback passes this stream as stderr to subprocess.Popen, which fails.
    # We patch _create_platform_compatible_process to substitute subprocess.DEVNULL
    # when the errlog stream doesn't support fileno().
    try:
        _orig_create = _mcp_stdio._create_platform_compatible_process

        async def _patched_create(command, args, env, errlog, cwd):
            try:
                if errlog is not None and not isinstance(errlog, int):
                    errlog.fileno()
            except io.UnsupportedOperation:
                errlog = subprocess.DEVNULL
            return await _orig_create(command, args, env, errlog, cwd)

        _mcp_stdio._create_platform_compatible_process = _patched_create
        print("MCP Windows stderr patch applied.")
    except ImportError:
        print("mcp not yet installed; skipping patch.")

sys.path.append(str(Path("../module7-genai-langchain").resolve()))
from azure_openai_llm import create_azure_llm

load_dotenv()
print("Environment initializing completed successfully.")
