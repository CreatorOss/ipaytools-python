# 🛡️ Anti-Loss Protection System

## Overview

iPayTools dilengkapi dengan sistem proteksi otomatis yang **MENJAMIN TIDAK ADA KERUGIAN** dalam setiap transaksi. Sistem ini secara otomatis memvalidasi profitabilitas sebelum setiap transaksi dan menolak transaksi yang akan menyebabkan kerugian.

## ✅ Fitur Keamanan

### 1. **Auto Fee Adjustment on Initialization**
- Saat iPayTools diinisialisasi, sistem otomatis mengecek apakah fee saat ini profitable
- Jika tidak profitable, fee akan otomatis dinaikkan ke level yang aman
- Minimum profit margin: **20%**
- Safety buffer: **30%**

```python
from ipaytools import iPayTools

# Auto-adjust fee saat init (default: True)
tools = iPayTools(auto_adjust_fee=True)
# Fee otomatis disesuaikan jika tidak profitable
```

### 2. **Transaction Rejection for Unprofitable Fees**
- Setiap transaksi divalidasi SEBELUM dieksekusi
- Jika fee tidak profitable, transaksi akan **DITOLAK**
- Error message yang jelas menjelaskan alasan penolakan

```python
try:
    tools.use_tool()
except Exception as e:
    # Error: "Transaction rejected: Fee is not profitable"
    print(e)
```

### 3. **Real-time Profitability Validation**
- Sistem menghitung profit margin secara real-time
- Memperhitungkan gas price saat ini
- Memastikan iPay dan Developer sama-sama profit

### 4. **Dynamic Fee Calculation**
- Fee dihitung berdasarkan formula:
  ```
  Minimum Fee = (Gas Cost / 0.7) * 1.3
  ```
- Gas Cost = Estimated Gas (100,000) × Current Gas Price
- 0.7 = iPay revenue share (70%)
- 1.3 = Safety buffer (30%)

## 📊 Revenue Split

Setiap transaksi dibagi:
- **70%** untuk iPay Team
- **30%** untuk App Developer

## 🔒 Safety Parameters

```python
class iPayTools:
    MIN_PROFIT_MARGIN = 0.20  # Minimum 20% profit margin
    SAFETY_BUFFER = 1.30      # 30% safety buffer
    AUTO_ADJUST_FEE = True    # Auto-adjust fee if not profitable
```

## 💡 Usage Examples

### Basic Usage (Recommended)
```python
from ipaytools import iPayTools

# Initialize dengan auto-adjust (default)
tools = iPayTools()

# Register app (gratis)
tools.register_app()

# Use tool - fee otomatis divalidasi
tools.use_tool()  # ✅ Hanya berhasil jika profitable
```

### Manual Control
```python
# Disable auto-adjust untuk kontrol manual
tools = iPayTools(auto_adjust_fee=False)

# Check profitability manually
is_profitable, profit, margin = tools._is_fee_profitable()
print(f"Profitable: {is_profitable}")
print(f"Profit: {profit:.6f} ETH")
print(f"Margin: {margin:.1f}%")

# Calculate minimum profitable fee
min_fee_wei, min_fee_eth, gas_cost = tools._calculate_minimum_profitable_fee()
print(f"Minimum fee: {min_fee_eth:.6f} ETH")
```

### Check Current Profitability
```python
# Get current fee
fee_eth = tools.get_fee()
print(f"Current fee: {fee_eth} ETH")

# Check if profitable
is_profitable, profit, margin = tools._is_fee_profitable()
if is_profitable:
    print(f"✅ Profitable! Margin: {margin:.1f}%")
else:
    print(f"❌ Not profitable! Loss: {profit:.6f} ETH")
```

## 🧪 Test Results

```
✅ TEST 1: Auto Fee Adjustment on Init
   Current Fee: 0.000196 ETH
   iPay Profit: +0.000032 ETH per transaction
   Profit Margin: 23.6%

✅ TEST 2: Transaction Rejection for Unprofitable Fee
   Fee: 0.00001 ETH (unprofitable)
   Result: Transaction correctly rejected!

✅ TEST 3: Current Fee Profitability Analysis
   Fee: 0.000196 ETH
   iPay Profit: +0.000032 ETH
   Developer Revenue: +0.000059 ETH
   Both parties profitable!

✅ TEST 4: Actual Transaction Test
   Expected earnings: 0.000059 ETH
   Actual earnings: 0.000059 ETH
   ✅ Earnings match expected!
```

## 📈 Profitability at Different Gas Prices

| Gas Price | Status | iPay Profit | Notes |
|-----------|--------|-------------|-------|
| 1 Gwei (Hardhat) | ✅ PROFIT | +0.000110 ETH | Safe |
| 10 Gwei (Low) | ⚠️ LOSS | -0.000790 ETH | Fee auto-adjusted |
| 30 Gwei (Normal) | ⚠️ LOSS | -0.002790 ETH | Fee auto-adjusted |
| 50 Gwei (High) | ⚠️ LOSS | -0.004790 ETH | Fee auto-adjusted |

**Note:** Sistem otomatis menaikkan fee jika gas price naik untuk memastikan tetap profitable.

## 🚨 Error Handling

### Transaction Rejected
```python
ERROR: ❌ TRANSACTION REJECTED: Fee is not profitable!
   Current fee: 0.000010 ETH
   iPay profit: -0.000098 ETH
   System would LOSE money on this transaction!
```

### Auto-Recovery
```python
INFO: 🔄 Attempting to auto-adjust fee...
INFO: 💡 Recommended fee: 0.000196 ETH (gas cost: 0.000105 ETH)
INFO: 🔄 Auto-adjusting fee to 0.000196 ETH...
INFO: ✅ Fee auto-adjusted successfully!
INFO: ✅ Fee adjusted to 0.000196 ETH, retrying transaction...
INFO: ✅ Profitability check passed (margin: 23.6%)
INFO: ✅ Transaction successful!
```

## 🎯 Key Benefits

1. **Zero Risk**: Tidak mungkin rugi karena transaksi unprofitable ditolak
2. **Automatic**: Tidak perlu manual calculation, semua otomatis
3. **Transparent**: Log yang jelas menunjukkan profit margin setiap transaksi
4. **Adaptive**: Fee otomatis menyesuaikan dengan gas price
5. **Fair**: Revenue split yang adil (70/30) untuk kedua pihak

## 🔧 Advanced Configuration

### Custom Profit Margin
```python
# Set custom minimum profit margin (default: 20%)
tools.MIN_PROFIT_MARGIN = 0.30  # 30% minimum margin

# Set custom safety buffer (default: 30%)
tools.SAFETY_BUFFER = 1.50  # 50% safety buffer
```

### Manual Fee Update (Owner Only)
```python
# Calculate optimal fee
min_fee_wei, min_fee_eth, gas_cost = tools._calculate_minimum_profitable_fee()

# Update fee manually (requires owner)
tools.contract.functions.setFeePerUse(min_fee_wei).transact({
    'from': tools.account,
    'gasPrice': tools.w3.eth.gas_price
})
```

## 📝 Summary

iPayTools Anti-Loss Protection System memastikan:
- ✅ **Tidak ada transaksi yang rugi**
- ✅ **Profit margin minimum 20%**
- ✅ **Auto-adjustment untuk gas price changes**
- ✅ **Transparent logging dan error messages**
- ✅ **Fair revenue split (70/30)**

**Sistem ini MENJAMIN profitabilitas untuk iPay Team dan App Developers!** 🎉
