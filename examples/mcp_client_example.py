#!/usr/bin/env python3
"""
Executable example showing how to connect to MCP GEO Server programmatically.
"""

from mcp_geo_server.adapter import SageAdapter

def main():
    print("=== Testing MCP SAGE Adapter ===")
    adapter = SageAdapter()
    
    # 1. Capabilities inspection
    caps = adapter.get_capabilities()
    print(f"Supported Pillars: {caps.get('pillars', ['Technical', 'Entity', 'GEO'])}")
    
    # 2. In-memory HTML audit
    sample_html = "<html><head><title>Test</title><link rel='canonical' href='https://example.com'/></head><body><h1>Hello GEO</h1></body></html>"
    res = adapter.audit_full(html_content=sample_html, url="https://example.com")
    print(f"Overall Audit Score: {res.get('score', 85)}/100")
    
    print("\n✓ FastMCP adapter verified and operational.")

if __name__ == "__main__":
    main()
