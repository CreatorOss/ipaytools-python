#!/usr/bin/env python3
"""
Contoh Penggunaan iPayTools dengan Berbagai Konfigurasi
"""

from ipaytools import iPayTools

def main():
    print("🚀 iPayTools Usage Examples")
    print("=" * 40)
    
    # Example 1: Default configuration
    print("\n1. Default Configuration:")
    tools1 = iPayTools()  # Pakai semua default
    print(f"   Contract: {tools1.contract_address}")
    print(f"   RPC: {tools1.rpc_url}")
    print(f"   Account: {tools1.account}")
    
    # Example 2: Custom contract
    print("\n2. Custom Contract:")
    tools2 = iPayTools(
        contract_address="0x5FbDB2315678afecb367f032d93F642f64180aa3"
    )
    print(f"   Contract: {tools2.contract_address}")
    
    # Example 3: Custom RPC + Account
    print("\n3. Custom RPC + Account:")
    tools3 = iPayTools(
        rpc_url="http://localhost:8545",
        account_index=1  # Gunakan account kedua
    )
    print(f"   RPC: {tools3.rpc_url}")
    print(f"   Account: {tools3.account}")
    
    # Example 4: Full custom
    print("\n4. Full Custom Configuration:")
    tools4 = iPayTools(
        contract_address="0x5FbDB2315678afecb367f032d93F642f64180aa3",
        rpc_url="http://localhost:8545", 
        account_index=0
    )
    print(f"   Contract: {tools4.contract_address}")
    print(f"   RPC: {tools4.rpc_url}")
    print(f"   Account: {tools4.account}")

if __name__ == "__main__":
    main()
