# Fix Summary: Contract Function Signature Mismatch

## Problem
The Python code was calling smart contract functions with incorrect parameters, causing the error:
```
web3.exceptions.ContractLogicError: execution reverted: function selector was not recognized and there's no fallback function
```

## Root Cause
The ABI definitions in `src/ipaytools/core.py` did not match the actual smart contract functions in `contracts/IpayTools.sol`:

1. **useTool()** - Python ABI expected a `data` parameter, but the contract function takes NO parameters
2. **registerApp()** - Python ABI expected an `appName` parameter, but the contract function takes NO parameters
3. **Missing registration** - The contract requires apps to be registered before calling `useTool()`, but the Python code wasn't registering automatically

## Changes Made

### 1. Fixed `useTool()` ABI Definition
**Before:**
```python
{
    "inputs": [{"internalType": "string", "name": "data", "type": "string"}],
    "name": "useTool",
    ...
}
```

**After:**
```python
{
    "inputs": [],
    "name": "useTool",
    ...
}
```

### 2. Fixed `registerApp()` ABI Definition
**Before:**
```python
{
    "inputs": [{"internalType": "string", "name": "appName", "type": "string"}],
    "name": "registerApp",
    ...
}
```

**After:**
```python
{
    "inputs": [],
    "name": "registerApp",
    ...
}
```

### 3. Updated All Function Calls
- `self.contract.functions.useTool("test")` → `self.contract.functions.useTool()`
- `self.contract.functions.useTool(data)` → `self.contract.functions.useTool()`
- Updated `use_tool_safe()` method signature to remove the `data` parameter

### 4. Added Automatic App Registration
Added code in `__init__()` to automatically register the app if not already registered:
```python
# Register app if not already registered
try:
    is_registered = self.contract.functions.registeredApps(self.account).call()
    if not is_registered:
        self.logger.info("📝 Registering app...")
        tx_hash = self.contract.functions.registerApp().transact({'from': self.account})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        self.logger.info("✅ App registered successfully")
    else:
        self.logger.info("✅ App already registered")
except Exception as e:
    self.logger.error(f"❌ App registration failed: {e}")
    raise
```

### 5. Added `registeredApps` to ABI
Added the view function to check registration status:
```python
{
    "inputs": [{"internalType": "address", "name": "", "type": "address"}],
    "name": "registeredApps",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "view",
    "type": "function"
}
```

### 6. Improved Gas Estimation
Changed gas estimation to use the current fee instead of a hardcoded low value that would fail:
```python
# Use current fee for estimation, or a reasonable default
try:
    estimate_value = self.get_fee()
except:
    estimate_value = self.w3.to_wei(0.0003, 'ether')
```

## Testing
All changes have been tested and verified to work correctly. The profitability check now runs without errors.

## Files Modified
- `src/ipaytools/core.py` - All ABI definitions and function calls updated

## Result
✅ The original error "function selector was not recognized" is now **COMPLETELY FIXED**.

## Current Status
The code now works correctly with the deployed smart contract. All function calls use the correct signatures.

### Note on "Insufficient fee" errors
You may still see "Insufficient fee" errors in some scenarios. This is **NOT** the same error - this is the smart contract correctly rejecting transactions where the fee is below the contract's `feePerUse` setting. This is expected behavior and indicates the contract's fee validation is working properly.

To avoid "Insufficient fee" errors:
1. Ensure the contract's `feePerUse` is set to a profitable amount
2. Use `use_tool_safe()` which automatically calculates the minimum profitable fee
3. Or manually pass a sufficient `value_eth` parameter to `use_tool_safe()`
