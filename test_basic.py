#!/usr/bin/env python3
print("🧪 TEST 1: Basic Import & Instantiation")
try:
    from ipaytools import iPayTools
    tools = iPayTools()
    print("✅ Import & Instantiation: SUCCESS")
    print(f"✅ Address: {tools.default_address}")
    print(f"✅ Contract: {tools.contract_address}")
    print(f"✅ Connected: {tools.w3.is_connected()}")
except Exception as e:
    print(f"❌ Failed: {e}")
