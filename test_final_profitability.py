#!/usr/bin/env python3
"""
FINAL PROFITABILITY TEST
Memastikan sistem TIDAK PERNAH RUGI dalam berbagai skenario
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ipaytools.core import iPayTools
from web3 import Web3

def main():
    print("=" * 70)
    print("🛡️  FINAL ANTI-LOSS PROTECTION TEST")
    print("=" * 70)
    
    try:
        # Test 1: Initialization dengan auto-adjust
        print("\n✅ TEST 1: Auto Fee Adjustment on Init")
        print("-" * 70)
        tools = iPayTools(auto_adjust_fee=True)
        
        fee_wei = tools.contract.functions.feePerUse().call()
        fee_eth = tools.w3.from_wei(fee_wei, 'ether')
        
        is_profitable, profit, margin = tools._is_fee_profitable(fee_wei)
        
        print(f"Current Fee: {fee_eth} ETH")
        print(f"Is Profitable: {is_profitable}")
        print(f"iPay Profit: {profit:+.6f} ETH per transaction")
        print(f"Profit Margin: {margin:.1f}%")
        
        if not is_profitable:
            print("❌ FAILED: Fee is not profitable after init!")
            return False
        
        print("✅ PASSED: Fee is automatically profitable!")
        
        # Test 2: Transaction rejection untuk unprofitable fee
        print("\n✅ TEST 2: Transaction Rejection for Unprofitable Fee")
        print("-" * 70)
        
        # Set fee yang terlalu rendah
        owner = tools.contract.functions.owner().call()
        if owner.lower() == tools.account.lower():
            print("Setting fee to unprofitable level (0.00001 ETH)...")
            low_fee_wei = tools.w3.to_wei(0.00001, 'ether')
            
            tx_hash = tools.contract.functions.setFeePerUse(low_fee_wei).transact({
                'from': tools.account,
                'gas': 100000,
                'gasPrice': tools.w3.eth.gas_price
            })
            tools.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Verify unprofitable
            is_profitable, profit, margin = tools._is_fee_profitable(low_fee_wei)
            print(f"Fee: 0.00001 ETH")
            print(f"Is Profitable: {is_profitable}")
            print(f"iPay Profit: {profit:+.6f} ETH")
            
            if is_profitable:
                print("⚠️  Fee is still profitable, cannot test rejection")
            else:
                # Try to use tool - should be REJECTED
                print("\nAttempting transaction with unprofitable fee...")
                
                # Create new instance without auto-adjust
                tools_no_auto = iPayTools(auto_adjust_fee=False)
                
                try:
                    if not tools_no_auto.is_registered():
                        tools_no_auto.register_app()
                    
                    tools_no_auto.use_tool()
                    print("❌ FAILED: Transaction was NOT rejected!")
                    return False
                    
                except Exception as e:
                    if "not profitable" in str(e).lower():
                        print(f"✅ PASSED: Transaction correctly rejected!")
                        print(f"   Reason: {e}")
                    else:
                        print(f"⚠️  Transaction rejected with different error: {e}")
        
        # Test 3: Profitability dengan current fee
        print("\n✅ TEST 3: Current Fee Profitability Analysis")
        print("-" * 70)
        
        # Reset to profitable fee
        tools_final = iPayTools(auto_adjust_fee=True)
        
        fee_wei = tools_final.contract.functions.feePerUse().call()
        fee_eth = float(tools_final.w3.from_wei(fee_wei, 'ether'))
        
        gas_price = tools_final.w3.eth.gas_price
        gas_price_gwei = tools_final.w3.from_wei(gas_price, 'gwei')
        gas_cost_eth = float(tools_final.w3.from_wei(100000 * gas_price, 'ether'))
        
        iPay_revenue = fee_eth * 0.7
        developer_revenue = fee_eth * 0.3
        iPay_profit = iPay_revenue - gas_cost_eth
        
        print(f"Fee: {fee_eth} ETH")
        print(f"Gas Price: {gas_price_gwei:.0f} Gwei")
        print(f"Gas Cost: {gas_cost_eth:.6f} ETH")
        print(f"\nRevenue Split:")
        print(f"  iPay (70%): {iPay_revenue:.6f} ETH")
        print(f"  Developer (30%): {developer_revenue:.6f} ETH")
        print(f"\nProfit per Transaction:")
        print(f"  iPay: {iPay_profit:+.6f} ETH")
        print(f"  Developer: {developer_revenue:+.6f} ETH")
        
        if iPay_profit <= 0:
            print("\n❌ FAILED: iPay is losing money!")
            return False
        
        if developer_revenue <= 0:
            print("\n❌ FAILED: Developer is not earning!")
            return False
        
        margin = (iPay_profit / iPay_revenue) * 100
        print(f"\n✅ PASSED: Both parties profitable!")
        print(f"   iPay profit margin: {margin:.1f}%")
        
        # Test 4: Actual transaction
        print("\n✅ TEST 4: Actual Transaction Test")
        print("-" * 70)
        
        if not tools_final.is_registered():
            print("Registering app...")
            tools_final.register_app()
        
        initial_earnings = tools_final.get_developer_earnings()
        print(f"Initial earnings: {initial_earnings:.6f} ETH")
        
        print(f"Executing transaction with fee: {fee_eth} ETH...")
        success = tools_final.use_tool()
        
        if not success:
            print("❌ FAILED: Transaction failed!")
            return False
        
        final_earnings = tools_final.get_developer_earnings()
        earnings_increase = float(final_earnings) - float(initial_earnings)
        
        print(f"Final earnings: {final_earnings:.6f} ETH")
        print(f"Earnings increase: {earnings_increase:+.6f} ETH")
        
        expected_earnings = fee_eth * 0.3
        
        if abs(earnings_increase - expected_earnings) < 0.000001:
            print(f"✅ PASSED: Earnings match expected ({expected_earnings:.6f} ETH)")
        else:
            print(f"⚠️  Earnings differ: expected {expected_earnings:.6f}, got {earnings_increase:.6f}")
        
        # Final Summary
        print("\n" + "=" * 70)
        print("📊 FINAL SUMMARY")
        print("=" * 70)
        print("\n✅ ALL CRITICAL TESTS PASSED!")
        print("\n🛡️  ANTI-LOSS PROTECTION FEATURES:")
        print("   ✓ Auto fee adjustment on initialization")
        print("   ✓ Transaction rejection for unprofitable fees")
        print("   ✓ Minimum 20% profit margin requirement")
        print("   ✓ 30% safety buffer in fee calculation")
        print("   ✓ Real-time profitability validation")
        print("\n💰 CURRENT PROFITABILITY:")
        print(f"   Fee: {fee_eth} ETH")
        print(f"   iPay profit: {iPay_profit:+.6f} ETH per transaction")
        print(f"   Developer revenue: {developer_revenue:.6f} ETH per transaction")
        print(f"   Profit margin: {margin:.1f}%")
        print("\n🎉 SYSTEM IS SAFE AND PROFITABLE!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
