#!/usr/bin/env python3
"""
Fix Fee Profitability - Update fee to profitable level
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ipaytools.core import iPayTools
from web3 import Web3
from decimal import Decimal

def calculate_minimum_profitable_fee(tools):
    """
    Calculate minimum fee that ensures profitability
    """
    # Get current gas price
    gas_price = tools.w3.eth.gas_price
    gas_price_gwei = tools.w3.from_wei(gas_price, 'gwei')
    
    # Estimate gas for useTool (from previous test: ~94,290 gas)
    estimated_gas = 100000  # Round up for safety
    
    # Calculate gas cost
    gas_cost_wei = estimated_gas * gas_price
    gas_cost_eth = tools.w3.from_wei(gas_cost_wei, 'ether')
    
    # iPay gets 70% of fee, so:
    # iPay_revenue = fee * 0.7
    # For profit: iPay_revenue > gas_cost
    # fee * 0.7 > gas_cost
    # fee > gas_cost / 0.7
    
    min_fee_eth = float(gas_cost_eth) / 0.7
    
    # Add 20% safety margin
    safe_fee_eth = min_fee_eth * 1.2
    
    # Round up to nice number
    if safe_fee_eth < 0.0002:
        safe_fee_eth = 0.0002
    elif safe_fee_eth < 0.0003:
        safe_fee_eth = 0.0003
    elif safe_fee_eth < 0.0005:
        safe_fee_eth = 0.0005
    else:
        # Round to nearest 0.0001
        safe_fee_eth = round(safe_fee_eth, 4)
    
    return {
        'gas_price_gwei': gas_price_gwei,
        'estimated_gas': estimated_gas,
        'gas_cost_eth': gas_cost_eth,
        'min_fee_eth': min_fee_eth,
        'recommended_fee_eth': safe_fee_eth,
        'safe_fee_wei': tools.w3.to_wei(safe_fee_eth, 'ether')
    }

def update_fee_to_profitable(tools, new_fee_wei):
    """
    Update contract fee to profitable level
    """
    try:
        # Check if we're the owner
        owner = tools.contract.functions.owner().call()
        if owner.lower() != tools.account.lower():
            print(f"❌ Not contract owner. Owner: {owner}, Account: {tools.account}")
            return False
        
        print(f"🔄 Updating fee to {tools.w3.from_wei(new_fee_wei, 'ether')} ETH...")
        
        # Build transaction
        transaction = {
            'from': tools.account,
            'gas': 100000,
            'gasPrice': tools.w3.eth.gas_price
        }
        
        # Send transaction
        tx_hash = tools.contract.functions.setFeePerUse(new_fee_wei).transact(transaction)
        
        print(f"⏳ Waiting for transaction: {tx_hash.hex()}")
        
        # Wait for receipt
        receipt = tools.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            print(f"✅ Fee updated successfully!")
            print(f"   Transaction: {tx_hash.hex()}")
            print(f"   Gas used: {receipt.gasUsed}")
            return True
        else:
            print(f"❌ Transaction failed")
            return False
            
    except Exception as e:
        print(f"❌ Failed to update fee: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_profitability(tools):
    """
    Verify that current fee is profitable
    """
    print("\n📊 PROFITABILITY VERIFICATION")
    print("=" * 50)
    
    # Get current fee
    current_fee_wei = tools.contract.functions.feePerUse().call()
    current_fee_eth = tools.w3.from_wei(current_fee_wei, 'ether')
    
    # Calculate costs
    gas_price = tools.w3.eth.gas_price
    gas_price_gwei = tools.w3.from_wei(gas_price, 'gwei')
    estimated_gas = 100000
    gas_cost_wei = estimated_gas * gas_price
    gas_cost_eth = tools.w3.from_wei(gas_cost_wei, 'ether')
    
    # Calculate revenue and profit
    iPay_revenue_eth = float(current_fee_eth) * 0.7
    developer_revenue_eth = float(current_fee_eth) * 0.3
    iPay_profit_eth = iPay_revenue_eth - float(gas_cost_eth)
    
    print(f"Current Fee: {current_fee_eth} ETH")
    print(f"Gas Price: {gas_price_gwei:.0f} Gwei")
    print(f"Gas Cost: {gas_cost_eth:.6f} ETH")
    print(f"\nRevenue Split:")
    print(f"  iPay (70%): {iPay_revenue_eth:.6f} ETH")
    print(f"  Developer (30%): {developer_revenue_eth:.6f} ETH")
    print(f"\nProfit Analysis:")
    print(f"  iPay Profit: {iPay_profit_eth:+.6f} ETH")
    print(f"  Developer Profit: {developer_revenue_eth:+.6f} ETH")
    
    if iPay_profit_eth > 0:
        print(f"\n✅ PROFITABLE! iPay earns {iPay_profit_eth:.6f} ETH per transaction")
        margin = (iPay_profit_eth / iPay_revenue_eth) * 100
        print(f"   Profit margin: {margin:.1f}%")
        return True
    else:
        print(f"\n❌ NOT PROFITABLE! iPay loses {abs(iPay_profit_eth):.6f} ETH per transaction")
        return False

def main():
    print("🔧 FEE PROFITABILITY FIX")
    print("=" * 50)
    
    try:
        # Initialize
        print("\n1. Initializing iPayTools...")
        tools = iPayTools()
        print(f"   ✅ Connected to: {tools.rpc_url}")
        print(f"   ✅ Account: {tools.account}")
        print(f"   ✅ Contract: {tools.contract_address}")
        
        # Check current fee
        print("\n2. Checking current fee...")
        current_fee_wei = tools.contract.functions.feePerUse().call()
        current_fee_eth = tools.w3.from_wei(current_fee_wei, 'ether')
        print(f"   Current fee: {current_fee_eth} ETH")
        
        # Calculate optimal fee
        print("\n3. Calculating optimal fee...")
        calc = calculate_minimum_profitable_fee(tools)
        print(f"   Gas price: {calc['gas_price_gwei']:.0f} Gwei")
        print(f"   Estimated gas: {calc['estimated_gas']}")
        print(f"   Gas cost: {calc['gas_cost_eth']:.6f} ETH")
        print(f"   Minimum profitable fee: {calc['min_fee_eth']:.6f} ETH")
        print(f"   Recommended fee (with 20% margin): {calc['recommended_fee_eth']:.6f} ETH")
        
        # Check if update needed
        if current_fee_wei < calc['safe_fee_wei']:
            print(f"\n4. ⚠️  Current fee is too low! Updating...")
            success = update_fee_to_profitable(tools, calc['safe_fee_wei'])
            
            if success:
                print("\n5. ✅ Fee updated successfully!")
            else:
                print("\n5. ❌ Failed to update fee")
                return False
        else:
            print(f"\n4. ✅ Current fee is already profitable")
        
        # Verify profitability
        print("\n6. Final verification...")
        is_profitable = verify_profitability(tools)
        
        if is_profitable:
            print("\n" + "=" * 50)
            print("🎉 SUCCESS! System is now profitable!")
            print("=" * 50)
            return True
        else:
            print("\n" + "=" * 50)
            print("❌ FAILED! System is still not profitable")
            print("=" * 50)
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
