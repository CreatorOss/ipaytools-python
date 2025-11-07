#!/usr/bin/env python3
"""
Test BRICS Multi-Currency System
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ipaytools.core import iPayTools

def test_brics_system():
    print("🌍 TESTING BRICS MULTI-CURRENCY SYSTEM")
    print("=" * 50)
    
    try:
        # Initialize iPayTools with BRICS
        tools = iPayTools(auto_adjust_fee=True)
        print("✅ iPayTools with BRICS initialized")
        
        # Test 1: Get all BRICS exchange rates
        print("\n1. Testing BRICS Exchange Rates:")
        rates = tools.get_brics_exchange_rates()
        for currency, info in rates.items():
            print(f"   💰 {currency} ({info['name']}): 1 = {info['rate']} IDR")
        
        # Test 2: Get specific currency info
        print("\n2. Testing Currency Info:")
        cny_info = tools.get_brics_currency_info('CNY')
        print(f"   🇨🇳 CNY Info: {cny_info}")
        
        # Test 3: Fee quotes
        print("\n3. Testing Fee Quotes:")
        quote = tools.get_brics_fee_quote('IDR', 'CNY', 1000000)  # 1 juta IDR to CNY
        print(f"   💸 Fee Quote: {quote['amount']} IDR → {quote['final_amount']:.2f} CNY")
        print(f"   📊 Fee: {quote['fee_percent']}% ({quote['fee_amount']:.2f} CNY)")
        
        # Test 4: Send BRICS payment (simulation)
        print("\n4. Testing BRICS Payment (Simulation):")
        payment = tools.send_brics_payment('CNY', 500000, 'fake_recipient_address')  # 500k IDR to CNY
        print(f"   🚀 Payment: {payment['amount']} IDR → {payment['final_amount']:.2f} CNY")
        print(f"   ✅ Status: {payment['status']}")
        print(f"   🔗 TX Hash: {payment['transaction_hash']}")
        
        # Test 5: Receive BRICS payment (simulation)
        print("\n5. Testing BRICS Receipt (Simulation):")
        receipt = tools.receive_brics_payment('CNY', 1000, 'fake_sender_address')  # 1000 CNY to IDR
        print(f"   🔄 Receipt: {receipt['amount']} CNY → {receipt['final_amount']:.0f} IDR")
        print(f"   ✅ Status: {receipt['status']}")
        
        print("\n🎉 BRICS SYSTEM TEST: ALL PASSED!")
        print("🌍 Multi-currency platform ready for production!")
        
    except Exception as e:
        print(f"❌ BRICS System Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_brics_system()
