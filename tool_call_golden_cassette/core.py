"""Core deterministic record/replay cassette for agent tool calls."""
import hashlib
import json
from typing import Any, Dict, List


class CassetteMissError(Exception):
    """Raised when replay encounters an unrecorded tool call or exhausted responses."""


class ToolCassette:
    """Records and replays ordered tool responses keyed by tool name and canonical arguments."""

    def __init__(self):
        self._entries: Dict[str, List[Any]] = {}

    @staticmethod
    def _key(tool_name: str, args: Dict[str, Any]) -> str:
        payload = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]

    def record(self, tool_name: str, args: Dict[str, Any], response: Any):
        k = self._key(tool_name, args)
        self._entries.setdefault(k, []).append(response)

    def replay(self, tool_name: str, args: Dict[str, Any]) -> Any:
        k = self._key(tool_name, args)
        queue = self._entries.get(k)
        if not queue:
            raise CassetteMissError(f"No recorded interaction for {tool_name}({args})")
        return queue.pop(0)

    def dump_json(self) -> str:
        return json.dumps(self._entries, indent=2, sort_keys=True)

    @classmethod
    def load_json(cls, raw: str) -> "ToolCassette":
        inst = cls()
        inst._entries = json.loads(raw)
        return inst
