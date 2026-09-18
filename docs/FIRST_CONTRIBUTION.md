# First Contribution Guide: MCP GEO Server

Welcome to MCP GEO Server! We welcome contributions to our FastMCP tool definitions and agent protocol integrations.

---

## ⚡ 5-Step Contributor Journey

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/tmolavi/mcp-geo-server.git
   cd mcp-geo-server
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

2. **Run Tests & Demo**:
   ```bash
   PYTHONPATH=src pytest tests/ -v
   PYTHONPATH=src python examples/public_demo/run_demo.py
   ```

3. **Open Issue / Discussion**: Check [GitHub Discussions](https://github.com/tmolavi/mcp-geo-server/discussions).
4. **Implement Changes**: Adhere to FastMCP tool schema specifications.
5. **Submit Pull Request**: Open a PR ensuring backward compatibility for agent clients.
