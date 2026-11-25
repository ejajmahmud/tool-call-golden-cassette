"""CLI for Tool Call Golden Cassette."""
import argparse
import json
from .core import ToolCassette


def main():
    parser = argparse.ArgumentParser(description="Tool Call Golden Cassette CLI")
    parser.add_argument("--demo", action="store_true", help="Record and replay sample cassette")
    args = parser.parse_args()

    c = ToolCassette()
    c.record("fetch_issue", {"id": 42}, {"title": "Fix timeout"})
    replayed = c.replay("fetch_issue", {"id": 42})
    print(json.dumps({"replayed": replayed}, indent=2))


if __name__ == "__main__":
    main()
