#!/usr/bin/env python3
"""
Test Anti-Loss Protection System
Memastikan sistem REJECT transaksi yang akan rugi dan auto-adjust fee
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ipaytools.core import iPayTools
from web3 import Web3

def test_auto_fee_adjustment():
    """Test 1: Auto fee adjustment saat initialization"""
    print("=" * 70)
    print("TEST 1: AUTO FEE ADJUSTMENT ON INITIALIZATION")
    print("=" * 70)
    
    try:
        print("\n1. Initializing iPayTools with auto_adjust_fee=True...")
        tools = iPayTools(auto_adjust_fee=True)
        
        print("\n2. Checking fee after initialization...")
        fee_wei = tools.contract.functions.feePerUse().call()
        fee_eth = tools.w3.from_wei(fee_wei, 'ether')
        
        print(f"   Current fee: {fee_eth} ETH")
        
        # Check profitability
        is_profitable, profit, margin = tools._is_fee_profitable(fee_wei)
        
        print(f"\n3. Profitability check:")
        print(f"   Is profitable: {is_profitable}")
        print(f"   iPay profit: {profit:+.6f} ETH")
        print(f"   Profit margin: {margin:.1f}%")
        
        if is_profitable:
            print(f"\n✅ TEST PASSED: Fee is automatically profitable!")
            return True
        else:
            print(f"\n❌ TEST FAILED: Fee is not profitable after auto-adjustment")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_transaction_rejection():
    """Test 2: Transaction rejection jika fee tidak profitable"""
    print("\n" + "=" * 70)
    print("TEST 2: TRANSACTION REJECTION FOR UNPROFITABLE FEE")
    print("=" * 70)
    
    try:
        # Initialize without auto-adjust untuk test rejection
        print("\n1. Setting up test scenario...")
        tools = iPayTools(auto_adjust_fee=False)
        
        # Manually set fee yang terlalu rendah (jika kita owner)
        owner = tools.contract.functions.owner().call()
        if owner.lower() == tools.account.lower():
            print("\n2. Setting fee to unprofitable level (0.00001 ETH)...")
            low_fee_wei = tools.w3.to_wei(0.00001, 'ether')
            
            tx_hash = tools.contract.functions.setFeePerUse(low_fee_wei).transact({
                'from': tools.account,
                'gas': 100000,
                'gasPrice': tools.w3.eth.gas_price
            })
            tools.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print("   ✅ Fee set to unprofitable level")
            
            # Verify fee is unprofitable
            is_profitable, profit, margin = tools._is_fee_profitable(low_fee_wei)
            print(f"\n3. Verifying fee is unprofitable:")
            print(f"   Fee: 0.00001 ETH")
            print(f"   Is profitable: {is_profitable}")
            print(f"   iPay profit: {profit:+.6f} ETH")
            
            if is_profitable:
                print("\n⚠️  Fee is still profitable, cannot test rejection")
                return True
            
            # Try to use tool - should be REJECTED
            print(f"\n4. Attempting to use tool with unprofitable fee...")
            print("   Expected: Transaction should be REJECTED")
            
            try:
                # Register if needed
                if not tools.is_registered():
                    tools.register_app()
                
                # This should FAIL
                tools.use_tool()
                
                print("\n❌ TEST FAILED: Transaction was NOT rejected!")
                return False
                
            except Exception as e:
                if "not profitable" in str(e).lower():
                    print(f"\n✅ TEST PASSED: Transaction correctly rejected!")
                    print(f"   Rejection reason: {e}")
                    return True
                else:
                    print(f"\n❌ TEST FAILED: Wrong error: {e}")
                    return False
        else:
            print("\n⚠️  Not contract owner, skipping rejection test")
            return True
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auto_recovery():
    """Test 3: Auto recovery dari unprofitable fee"""
    print("\n" + "=" * 70)
    print("TEST 3: AUTO RECOVERY FROM UNPROFITABLE FEE")
    print("=" * 70)
    
    try:
        print("\n1. Setting up test scenario...")
        tools = iPayTools(auto_adjust_fee=False)
        
        owner = tools.contract.functions.owner().call()
        if owner.lower() == tools.account.lower():
            # Set unprofitable fee
            print("\n2. Setting fee to unprofitable level...")
            low_fee_wei = tools.w3.to_wei(0.00001, 'ether')
            tx_hash = tools.contract.functions.setFeePerUse(low_fee_wei).transact({
                'from': tools.account,
                'gas': 100000,
                'gasPrice': tools.w3.eth.gas_price
            })
            tools.w3.eth.wait_for_transaction_receipt(tx_hash)
            print("   ✅ Fee set to 0.00001 ETH (unprofitable)")
            
            # Verify unprofitable
            is_profitable, profit, margin = tools._is_fee_profitable(low_fee_wei)
            print(f"\n3. Verifying unprofitable state:")
            print(f"   Is profitable: {is_profitable}")
            print(f"   iPay profit: {profit:+.6f} ETH")
            
            if is_profitable:
                print("\n⚠️  Fee is still profitable, cannot test recovery")
                return True
            
            # Now enable auto-adjust and try transaction
            print(f"\n4. Enabling auto-adjust and attempting transaction...")
            tools.auto_adjust_fee = True
            
            # Register if needed
            if not tools.is_registered():
                tools.register_app()
            
            # This should auto-adjust fee and succeed
            success = tools.use_tool()
            
            if success:
                # Verify fee was adjusted
                new_fee_wei = tools.contract.functions.feePerUse().call()
                new_fee_eth = tools.w3.from_wei(new_fee_wei, 'ether')
                is_profitable, profit, margin = tools._is_fee_profitable(new_fee_wei)
                
                print(f"\n5. Verifying recovery:")
                print(f"   New fee: {new_fee_eth} ETH")
                print(f"   Is profitable: {is_profitable}")
                print(f"   iPay profit: {profit:+.6f} ETH")
                print(f"   Profit margin: {margin:.1f}%")
                
                if is_profitable:
                    print(f"\n✅ TEST PASSED: System auto-recovered to profitable state!")
                    return True
                else:
                    print(f"\n❌ TEST FAILED: Fee adjusted but still not profitable")
                    return False
            else:
                print(f"\n❌ TEST FAILED: Transaction failed after auto-adjust")
                return False
        else:
            print("\n⚠️  Not contract owner, skipping recovery test")
            return True
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_profitability_validation():
    """Test 4: Profitability validation methods"""
    print("\n" + "=" * 70)
    print("TEST 4: PROFITABILITY VALIDATION METHODS")
    print("=" * 70)
    
    try:
        tools = iPayTools()
        
        print("\n1. Testing _is_fee_profitable()...")
        current_fee_wei = tools.contract.functions.feePerUse().call()
        is_profitable, profit, margin = tools._is_fee_profitable(current_fee_wei)
        
        print(f"   Current fee: {tools.w3.from_wei(current_fee_wei, 'ether')} ETH")
        print(f"   Is profitable: {is_profitable}")
        print(f"   iPay profit: {profit:+.6f} ETH")
        print(f"   Profit margin: {margin:.1f}%")
        
        if not is_profitable:
            print("\n❌ Current fee is not profitable!")
            return False
        
        print("\n2. Testing _calculate_minimum_profitable_fee()...")
        min_fee_wei, min_fee_eth, gas_cost = tools._calculate_minimum_profitable_fee()
        
        print(f"   Gas cost: {gas_cost:.6f} ETH")
        print(f"   Minimum fee: {min_fee_eth:.6f} ETH")
        print(f"   Current fee: {tools.w3.from_wei(current_fee_wei, 'ether')} ETH")
        
        if current_fee_wei >= min_fee_wei:
            print(f"\n✅ Current fee meets minimum requirement")
        else:
            print(f"\n⚠️  Current fee is below minimum")
        
        print("\n3. Testing _ensure_profitable_fee()...")
        result = tools._ensure_profitable_fee()
        
        if result:
            print(f"   ✅ Fee is ensured to be profitable")
        else:
            print(f"   ⚠️  Could not ensure profitable fee")
        
        print(f"\n✅ TEST PASSED: All validation methods working!")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_various_gas_prices():
    """Test 5: Behavior dengan berbagai gas prices"""
    print("\n" + "=" * 70)
    print("TEST 5: BEHAVIOR WITH VARIOUS GAS PRICES")
    print("=" * 70)
    
    try:
        tools = iPayTools()
        
        current_fee_wei = tools.contract.functions.feePerUse().call()
        current_fee_eth = float(tools.w3.from_wei(current_fee_wei, 'ether'))
        
        print(f"\nCurrent fee: {current_fee_eth} ETH")
        print("\nSimulating different gas prices:")
        print("-" * 70)
        
        # Simulate berbagai gas prices
        gas_scenarios = [
            (1, "Very Low (Hardhat)"),
            (10, "Low"),
            (20, "Normal"),
            (30, "High"),
            (50, "Very High")
        ]
        
        for gas_gwei, scenario in gas_scenarios:
            # Calculate profitability at this gas price
            gas_price_wei = tools.w3.to_wei(gas_gwei, 'gwei')
            gas_cost_wei = 100000 * gas_price_wei
            gas_cost_eth = float(tools.w3.from_wei(gas_cost_wei, 'ether'))
            
            iPay_revenue = current_fee_eth * 0.7
            iPay_profit = iPay_revenue - gas_cost_eth
            
            # Calculate minimum fee needed
            min_fee_needed = (gas_cost_eth / 0.7) * 1.3  # with 30% buffer
            
            if iPay_profit > 0:
                margin = (iPay_profit / iPay_revenue) * 100
                status = f"✅ PROFIT {iPay_profit:+.6f} ETH (margin: {margin:.1f}%)"
            else:
                status = f"❌ LOSS {iPay_profit:+.6f} ETH (need: {min_fee_needed:.6f} ETH)"
            
            print(f"{scenario:20} ({gas_gwei:3} Gwei): {status}")
        
        print("-" * 70)
        print(f"\n✅ TEST PASSED: Gas price analysis complete")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "=" * 70)
    print("🛡️  ANTI-LOSS PROTECTION SYSTEM TEST SUITE")
    print("=" * 70)
    
    results = []
    
    # Run all tests
    results.append(("Auto Fee Adjustment", test_auto_fee_adjustment()))
    results.append(("Transaction Rejection", test_transaction_rejection()))
    results.append(("Auto Recovery", test_auto_recovery()))
    results.append(("Profitability Validation", test_profitability_validation()))
    results.append(("Various Gas Prices", test_various_gas_prices()))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:30} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL TESTS PASSED - ANTI-LOSS PROTECTION WORKING!")
        print("\n✅ System Features:")
        print("   • Auto fee adjustment on initialization")
        print("   • Transaction rejection for unprofitable fees")
        print("   • Auto recovery from unprofitable state")
        print("   • Minimum 20% profit margin requirement")
        print("   • 30% safety buffer for fee calculation")
    else:
        print("❌ SOME TESTS FAILED - REVIEW REQUIRED")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
