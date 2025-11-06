#!/bin/bash
cd /root/dragon/software/ipay/ipay-tools-final

echo "🎯 FINAL TEST - iPayTools"

# Test 1: Basic connectivity
echo "1. 🔗 Testing blockchain connection..."
python3 -c "
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
print('   ✅ Connected:', w3.is_connected())
print('   ✅ Accounts:', len(w3.eth.accounts))
print('   ✅ Block:', w3.eth.block_number)
"

# Test 2: Contract access
echo "2. 📝 Testing contract access..."
CONTRACT="0x5FbDB2315678afecb367f032d93F642f64180aa3"
python3 -c "
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
contract_address = '$CONTRACT'
code = w3.eth.get_code(contract_address)
print('   ✅ Contract code size:', len(code))
print('   ✅ Is contract:', len(code) > 0)
"

# Test 3: iPayTools SDK
echo "3. 🛠️ Testing iPayTools SDK..."
python quick_start.py

echo "🎉 TESTING COMPLETED!"
