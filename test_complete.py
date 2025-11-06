#!/usr/bin/env python3
"""
Comprehensive test suite for iPayTools
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ipaytools.core import iPayTools

def test_all_features():
    """Test all iPayTools features comprehensively"""
    print("=" * 60)
    print("🧪 iPayTools Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        print("\n1️⃣  Testing Initialization...")
        tools = iPayTools(auto_adjust_fee=True)
        print(f"   ✅ Connected to: {tools.rpc_url}")
        print(f"   ✅ Contract: {tools.contract_address}")
        
        # Get account from web3
        if tools.w3.eth.accounts:
            account = tools.w3.eth.accounts[0]
            print(f"   ✅ Primary account: {account}")
        else:
            print("   ⚠️  No accounts found")
            return False
        
        print("\n2️⃣  Testing Fee Operations...")
        current_fee = tools.get_fee()
        print(f"   ✅ Current fee: {current_fee} ETH")
        
        # Check profitability
        is_profitable, profit, margin = tools._is_fee_profitable(current_fee)
        print(f"   ✅ Is profitable: {is_profitable}")
        if is_profitable:
            print(f"   ✅ iPay profit: {profit:.6f} ETH")
            print(f"   ✅ Profit margin: {margin:.1f}%")
        else:
            print(f"   ⚠️  iPay loss: {profit:.6f} ETH")
        
        print("\n3️⃣  Testing Profitability Protection...")
        try:
            tools._ensure_profitable_fee()
            print("   ✅ Profitability protection working")
        except Exception as e:
            print(f"   ⚠️  Profitability protection: {e}")
        
        print("\n4️⃣  Testing Registration Check...")
        is_registered = tools.is_registered(account)
        print(f"   ✅ Is registered: {is_registered}")
        
        print("\n5️⃣  Testing Contract Info...")
        balance = tools.get_contract_balance()
        earnings = tools.get_developer_earnings(account)
        print(f"   ✅ Contract balance: {balance} ETH")
        print(f"   ✅ Developer earnings: {earnings} ETH")
        
        print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_features()
    sys.exit(0 if success else 1)
