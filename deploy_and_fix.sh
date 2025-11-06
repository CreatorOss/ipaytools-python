#!/bin/bash
cd /root/dragon/software/ipay/ipay-tools-final

echo "🚀 Deploying contract to running node..."
npx hardhat run scripts/deploy.js --network localhost

echo "📝 Updating contract address..."
NEW_CONTRACT=$(cat deployed-address.txt)
echo "New contract: $NEW_CONTRACT"

# Update Python files
sed -i "s/DEFAULT_CONTRACT_ADDRESS = \".*\"/DEFAULT_CONTRACT_ADDRESS = \"$NEW_CONTRACT\"/" src/ipaytools/core.py
echo "$NEW_CONTRACT" > working-address.txt

echo "📦 Reinstalling..."
pip install -e .

echo "🧪 Testing..."
python quick_start.py

if [ $? -eq 0 ]; then
    echo "🎉 SUCCESS! Contract deployed and working!"
else
    echo "❌ Something went wrong"
fi
