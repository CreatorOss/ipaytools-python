#!/usr/bin/env python3
"""
Contoh Konfigurasi iPayTools
"""

from ipaytools import iPayTools

def example_basic_config():
    """Contoh konfigurasi dasar"""
    print("🔧 Contoh Konfigurasi Dasar")
    
    # Konfigurasi default
    tools = iPayTools()
    print(f"✅ Default config - Contract: {tools.contract_address}")
    print(f"✅ Default config - RPC: {tools.rpc_url}")
    print(f"✅ Default config - Account: {tools.account}")

def example_custom_config():
    """Contoh konfigurasi custom"""
    print("\n🔧 Contoh Konfigurasi Custom")
    
    # Konfigurasi custom
    tools = iPayTools(
        contract_address="0x5FbDB2315678afecb367f032d93F642f64180aa3",
        rpc_url="http://localhost:8545",
        account_index=0
    )
    print(f"✅ Custom config - Contract: {tools.contract_address}")
    print(f"✅ Custom config - RPC: {tools.rpc_url}") 
    print(f"✅ Custom config - Account: {tools.account}")

def example_different_networks():
    """Contoh konfigurasi untuk network berbeda"""
    print("\n🔧 Contoh Network Berbeda")
    
    # Hardhat Local
    hardhat = iPayTools(
        contract_address="0x5FbDB2315678afecb367f032d93F642f64180aa3",
        rpc_url="http://localhost:8545"
    )
    print("✅ Hardhat Local: Ready")
    
    # Sepolia Testnet (contoh)
    print("🌐 Sepolia Testnet (example):")
    print("   tools = iPayTools(")
    print("       contract_address='0x1234...',")
    print("       rpc_url='https://sepolia.infura.io/v3/your-key'")
    print("   )")
    
    # Mainnet (contoh)  
    print("🔗 Ethereum Mainnet (example):")
    print("   tools = iPayTools(")
    print("       contract_address='0x5678...',") 
    print("       rpc_url='https://mainnet.infura.io/v3/your-key'")
    print("   )")

if __name__ == "__main__":
    example_basic_config()
    example_custom_config() 
    example_different_networks()
