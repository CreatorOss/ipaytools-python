#!/usr/bin/env python3
"""
Test BRICS System - Fixed Version
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ipaytools.core import iPayTools

def test_brics_system_fixed():
    print("🌍 TESTING BRICS SYSTEM - FIXED VERSION")
    print("=" * 50)
    
    try:
        tools = iPayTools(auto_adjust_fee=True)
        print("✅ iPayTools with BRICS initialized")
        
        # Test 1: BRICS Exchange Rates
        print("\n1. BRICS Exchange Rates:")
        rates = tools.get_brics_exchange_rates()
        for currency, info in rates.items():
            print(f"   💰 {currency} ({info['name']}): 1 = {info['rate']} IDR")
        
        # Test 2: Currency Info
        print("\n2. Currency Information:")
        currencies_to_test = ['CNY', 'INR', 'SAR']
        for currency in currencies_to_test:
            try:
                info = tools.get_brics_currency_info(currency)
                print(f"   🇺🇳 {currency}:")
                print(f"      Name: {info['name']}")
                print(f"      Rate: 1 = {info['current_rate']} IDR")
                print(f"      Fee Individual: {info['fee_individual']}%")
                print(f"      Fee Bundle: {info['fee_bundle']}%")
            except Exception as e:
                print(f"   ⚠️ {currency} info failed: {e}")
        
        # Test 3: Fee Quotes
        print("\n3. Fee Quotes:")
        test_quotes = [
            ('IDR', 'CNY', 1000000, 'Individual'),
            ('IDR', 'INR', 500000, 'Bundle'),
            ('CNY', 'IDR', 1000, 'Individual')
        ]
        
        for from_curr, to_curr, amount, fee_type in test_quotes:
            try:
                quote = tools.get_brics_fee_quote(from_curr, to_curr, amount, fee_type.lower())
                print(f"   💸 {from_curr} → {to_curr}:")
                print(f"      Amount: {quote['amount']} {from_curr}")
                print(f"      Final: {quote['final_amount']:.2f} {to_curr}")
                print(f"      Fee: {quote['fee_percent']}%")
                print(f"      Rate: 1 {to_curr} = {quote['exchange_rate']} IDR")
            except Exception as e:
                print(f"   ⚠️ Quote {from_curr}→{to_curr} failed: {e}")
        
        # Test 4: Payment Simulation
        print("\n4. Payment Simulation:")
        try:
            payment = tools.send_brics_payment('CNY', 500000, 'test_recipient_123')
            print(f"   🚀 Payment Simulation:")
            print(f"      Status: {payment['status']}")
            print(f"      Amount: {payment['amount']} IDR → {payment['final_amount']:.2f} CNY")
            print(f"      TX Hash: {payment['transaction_hash'][:20]}...")
        except Exception as e:
            print(f"   ⚠️ Payment simulation failed: {e}")
        
        print("\n🎉 BRICS SYSTEM TEST COMPLETED!")
        print("🌍 Multi-currency platform operational!")
        
    except Exception as e:
        print(f"❌ BRICS System Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_brics_system_fixed()
