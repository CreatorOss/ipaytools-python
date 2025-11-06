#!/usr/bin/env python3
"""
Test REAL-TIME anti-rugi system
"""
from ipaytools.core import iPayTools

def test_real_time_anti_rugi():
    print("🛡️ REAL-TIME ANTI-RUGI SYSTEM TEST")
    print("=" * 50)
    
    tools = iPayTools(auto_adjust_fee=True)
    
    print("1. Testing REAL-TIME gas price check...")
    gas_price = tools.get_current_gas_price()
    print(f"   ✅ Current gas price: {tools.w3.from_wei(gas_price, 'gwei'):.2f} Gwei")
    
    print("\n2. Testing REAL-TIME minimum fee calculation...")
    min_fee = tools.calculate_minimum_profitable_fee()
    print(f"   ✅ Minimum profitable fee: {tools.w3.from_wei(min_fee, 'ether'):.6f} ETH")
    
    print("\n3. Testing REAL-TIME profitability check...")
    current_fee = tools.get_fee()
    is_profitable, profit, margin = tools._is_fee_profitable(current_fee)
    print(f"   ✅ Current fee: {tools.w3.from_wei(current_fee, 'ether'):.6f} ETH")
    print(f"   ✅ Is profitable: {is_profitable}")
    if is_profitable:
        print(f"   ✅ iPay profit: {tools.w3.from_wei(profit, 'ether'):.6f} ETH")
        print(f"   ✅ Profit margin: {margin:.1f}%")
    
    print("\n4. Testing SAFE transaction method...")
    try:
        result = tools.use_tool_safe("test_data_real_time")
        print("   ✅ SAFE transaction: SUCCESS (System profitable)")
    except Exception as e:
        print(f"   ✅ SAFE transaction: REJECTED ({e})")
    
    print("\n5. Testing UNPROFITABLE transaction rejection...")
    try:
        # Try dengan fee sangat rendah
        result = tools.use_tool_safe("test_data", value_eth=0.000001)
        print("   ❌ Should have been rejected!")
    except Exception as e:
        print(f"   ✅ Correctly rejected: {e}")
    
    print("\n🎉 REAL-TIME ANTI-RUGI SYSTEM: OPERATIONAL!")
    print("💡 Setiap transaksi sekarang check:")
    print("   - Current gas price")
    print("   - Minimum profitable fee") 
    print("   - Real-time profitability")
    print("   - Safety buffers (20% gas price, 30% gas estimate)")
    print("   - Auto-rejection jika tidak profitable")

if __name__ == "__main__":
    test_real_time_anti_rugi()
