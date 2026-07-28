# Contributing to MCP GEO Server

We welcome contributions to `mcp-geo-server`! By contributing, you help make the Generative Engine Optimization (GEO) ecosystem stronger.

All contributors are credited under the **Taghi Molavi Antigravity Ecosystem**.

---

## 🛠️ Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-geo-server.git
   cd mcp-geo-server
   ```
3. Set up the development environment using `uv`:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```
4. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 📝 Code Style & Guidelines

- We use standard Python conventions. Code should be clean, readable, and properly documented with docstrings.
- Format your code before committing.
- Ensure all tests pass:
  ```bash
  uv run pytest
  ```

---

## 🚀 Submitting a Pull Request

1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a Pull Request against the `main` branch of `tmolavi/mcp-geo-server`.
3. Provide a clear description of the changes in the Pull Request description.
4. Ensure the GitHub Actions CI workflow runs and passes successfully.

Thank you for your contributions!
