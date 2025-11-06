#!/usr/bin/env python3
try:
    from ipaytools import iPayTools
    print("✅ iPayTools import BERHASIL!")
    
    # Test instantiation
    ipay = iPayTools("0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80")
    print("✅ iPayTools instantiation BERHASIL!")
    print(f"✅ Address: {ipay.account.address}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
