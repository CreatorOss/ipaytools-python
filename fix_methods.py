#!/usr/bin/env python3
"""
Fix method names di core.py
"""
import re

# Baca file core.py
with open('src/ipaytools/core.py', 'r') as f:
    content = f.read()

# Cari method gas estimation yang sebenarnya
if "def estimate_gas_safe(" in content:
    print("✅ Method estimate_gas_safe ditemukan")
    # Ganti semua pemanggilan _estimate_gas_safe menjadi estimate_gas_safe
    content = content.replace('_estimate_gas_safe', 'estimate_gas_safe')
    print("✅ Method names diperbaiki")
else:
    print("❌ Method estimate_gas_safe tidak ditemukan")
    # Cari method gas estimation lainnya
    gas_methods = re.findall(r'def.*gas.*\(', content)
    print(f"Method gas yang ditemukan: {gas_methods}")

# Write back
with open('src/ipaytools/core.py', 'w') as f:
    f.write(content)

print("✅ Core.py updated")
