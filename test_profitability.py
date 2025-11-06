#!/usr/bin/env python3
"""
Test Profitability iPayTools - FIXED VERSION
Pastikan biaya transaksi selalu profitable
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ipaytools.core import iPayTools
from web3 import Web3
from decimal import Decimal

def test_profitability():
    print("🧪 TEST PROFITABILITY iPayTools")
    print("=" * 50)
    
    try:
        tools = iPayTools()
        
        # 1. Cek current fee dari contract
        fee_eth = Decimal(str(tools.get_fee()))
        fee_wei = tools.w3.to_wei(float(fee_eth), 'ether')
        print(f"1. Current Fee: {fee_eth} ETH ({fee_wei} wei)")
        
        # 2. Cek gas price current
        gas_price = tools.w3.eth.gas_price
        gas_price_gwei = tools.w3.from_wei(gas_price, 'gwei')
        print(f"2. Current Gas Price: {gas_price_gwei:.0f} Gwei")
        
        # 3. Estimate gas costs untuk useTool
        print("\n3. Gas Cost Estimation:")
        try:
            gas_use_tool = tools.contract.functions.useTool().estimate_gas({
                'from': tools.account,
                'value': fee_wei
            })
            cost_use_tool_wei = gas_use_tool * gas_price
            cost_use_tool_eth = Decimal(str(tools.w3.from_wei(cost_use_tool_wei, 'ether')))
            print(f"   🔧 useTool(): {gas_use_tool} gas = {cost_use_tool_eth:.6f} ETH")
            
            # 4. Profitability Analysis
            print("\n4. PROFITABILITY ANALYSIS:")
            
            # Asumsi revenue split: 70% iPay, 30% Developer
            iPay_revenue = fee_eth * Decimal('0.7')  # 70% untuk iPay
            developer_revenue = fee_eth * Decimal('0.3')  # 30% untuk developer
            
            print(f"   💵 Fee {fee_eth} ETH breakdown:")
            print(f"      iPay revenue: {iPay_revenue:.6f} ETH (70%)")
            print(f"      Developer revenue: {developer_revenue:.6f} ETH (30%)")
            
            # Hitung profit/loss
            iPay_profit = iPay_revenue - cost_use_tool_eth
            developer_profit = developer_revenue  # Developer tidak bayar gas untuk useTool
            
            print(f"\n   📊 Profit per transaction:")
            print(f"      iPay revenue: {iPay_revenue:.6f} ETH")
            print(f"      iPay gas cost: {cost_use_tool_eth:.6f} ETH")
            print(f"      iPay NET: {iPay_profit:.6f} ETH")
            print(f"      Developer NET: {developer_profit:.6f} ETH")
            
            # 5. Profit/Loss Conclusion
            print("\n5. PROFITABILITY CONCLUSION:")
            if iPay_profit > 0:
                print(f"   ✅ iPay: PROFITABLE! +{iPay_profit:.6f} ETH per transaction")
                print(f"   ✅ Developer: PROFITABLE! +{developer_profit:.6f} ETH per transaction")
            else:
                print(f"   ❌ iPay: LOSS! {iPay_profit:.6f} ETH per transaction")
                print(f"   ✅ Developer: Still PROFITABLE! +{developer_profit:.6f} ETH per transaction")
                print(f"   💡 Recommendation: Increase feePerUse in contract")
            
            # 6. Break-even Analysis
            print("\n6. BREAK-EVEN ANALYSIS:")
            if iPay_revenue > 0:
                break_even_tx = float(cost_use_tool_eth) / float(iPay_revenue)
                print(f"   iPay needs {break_even_tx:.2f} transactions to break-even on gas")
            
            # 7. Minimum Fee Recommendation
            print("\n7. MINIMUM FEE RECOMMENDATION:")
            min_fee_for_profit = (float(cost_use_tool_eth) / 0.7) * 1.1  # +10% buffer
            print(f"   Minimum fee for iPay profit: {min_fee_for_profit:.6f} ETH")
            print(f"   Current fee: {float(fee_eth):.6f} ETH")
            
            if float(fee_eth) >= min_fee_for_profit:
                print("   ✅ Current fee is sufficient for profitability")
            else:
                print(f"   ⚠️  Consider increasing fee to {min_fee_for_profit:.6f} ETH")
                
        except Exception as e:
            print(f"   ❌ Gas estimation failed: {e}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_different_gas_scenarios():
    print("\n" + "=" * 50)
    print("🌡️  GAS PRICE SENSITIVITY ANALYSIS")
    print("=" * 50)
    
    try:
        tools = iPayTools()
        fee_eth = Decimal(str(tools.get_fee()))
        iPay_revenue = fee_eth * Decimal('0.7')
        
        # Test berbagai gas price scenarios
        gas_scenarios = [
            (10, "Low Gas"),
            (30, "Normal Gas"), 
            (50, "High Gas"),
            (100, "Very High Gas"),
            (200, "Network Congestion")
        ]
        
        print("   Current fee: 0.0001 ETH")
        print("   iPay revenue (70%): 0.00007 ETH")
        print("   Estimated gas usage: ~94,290 gas")
        print()
        
        for gas_gwei, scenario in gas_scenarios:
            gas_price_wei = tools.w3.to_wei(gas_gwei, 'gwei')
            
            # Hitung gas cost
            gas_use_tool = 94290  # Dari estimate sebelumnya
            cost_wei = gas_use_tool * gas_price_wei
            cost_eth = Decimal(str(tools.w3.from_wei(cost_wei, 'ether')))
            profit = iPay_revenue - cost_eth
            
            status = "✅ PROFIT" if profit > 0 else "❌ LOSS"
            print(f"   {scenario:15} ({gas_gwei:3} Gwei): {status} {profit:+.6f} ETH")
                
    except Exception as e:
        print(f"❌ Sensitivity analysis failed: {e}")

if __name__ == "__main__":
    test_profitability()
    test_different_gas_scenarios()
    print("\n🎯 KEY FINDINGS:")
    print("   - Current fee: 0.0001 ETH")
    print("   - Gas cost at 1 Gwei: ~0.000094 ETH") 
    print("   - iPay gets 0.00007 ETH (70%)")
    print("   - ❌ CURRENTLY AT LOSS: -0.000024 ETH per tx")
    print("   - 💡 Recommended minimum fee: 0.00015 ETH")
