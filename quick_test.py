#!/usr/bin/env python3
from src.ipaytools.core import iPayTools

def main():
    print("🚀 Quick Test iPayTools")
    try:
        # Initialize with auto-adjust fee
        t = iPayTools(auto_adjust_fee=True)
        print("✅ Initialization successful")
        print("RPC URL:", t.rpc_url)
        print("Contract:", t.contract_address)
        
        # Get first account
        if t.w3.eth.accounts:
            account = t.w3.eth.accounts[0]
            print("Account:", account)
        else:
            print("❌ No accounts available")
            return
        
        # Check current fee
        fee = t.get_fee()
        print("Current fee:", fee, "ETH")
        
        # Check profitability
        is_profitable, profit, margin = t._is_fee_profitable(fee)
        print("Is profitable:", is_profitable)
        if is_profitable:
            print("iPay profit:", f"{profit:.6f} ETH")
            print("Profit margin:", f"{margin:.1f}%")
        else:
            print("iPay loss:", f"{profit:.6f} ETH")
        
        # Check registration
        is_registered = t.is_registered(account)
        print("Is registered:", is_registered)
        
        print("✅ Quick test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
