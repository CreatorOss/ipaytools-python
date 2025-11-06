#!/usr/bin/env python3
"""
Quick fix untuk error di core.py
"""
import re

# Baca file core.py
with open('src/ipaytools/core.py', 'r') as f:
    content = f.read()

# Perbaiki: ganti estimate_gas_safe dengan _estimate_gas_safe
content = content.replace('estimate_gas_safe', '_estimate_gas_safe')

# Perbaiki parameter di use_tool_safe
old_method = '    def use_tool_safe(self, data="", value_eth=None):'
new_method = '    def use_tool_safe(self, data="", value_eth=None):'
# Method sudah benar, tidak perlu diubah

# Perbaiki error handling di _is_fee_profitable
old_profit_check = '''        if is_profitable:
            gas_price = self.get_current_gas_price()
            gas_estimate = self._estimate_gas_safe(fee_wei)
            gas_cost = gas_estimate * gas_price
            ipay_revenue = fee_wei * 70 // 100
            ipay_profit = ipay_revenue - gas_cost
            
            if ipay_revenue > 0:
                profit_margin = (ipay_profit / ipay_revenue) * 100
            else:
                profit_margin = 0
                
            self.logger.info(f"✅ Fee is profitable (margin: {profit_margin:.1f}%")'''

new_profit_check = '''        if is_profitable:
            try:
                gas_price = self.get_current_gas_price()
                gas_estimate = self._estimate_gas_safe(fee_wei)
                gas_cost = gas_estimate * gas_price
                ipay_revenue = fee_wei * 70 // 100
                ipay_profit = ipay_revenue - gas_cost
                
                if ipay_revenue > 0:
                    profit_margin = (ipay_profit / ipay_revenue) * 100
                else:
                    profit_margin = 0
                    
                self.logger.info(f"✅ Fee is profitable (margin: {profit_margin:.1f}%)")
            except Exception as e:
                self.logger.warning(f"Profit calculation failed: {e}")
                ipay_profit = 0
                profit_margin = 0'''

if old_profit_check in content:
    content = content.replace(old_profit_check, new_profit_check)
    print("✅ Profit calculation error handling fixed")

# Write back
with open('src/ipaytools/core.py', 'w') as f:
    f.write(content)

print("✅ Core.py errors fixed")
