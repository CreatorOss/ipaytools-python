#!/bin/bash
cd /root/dragon/software/ipay/ipay-tools-final

echo "🔧 Fixing for Python 3.13..."
source venv/bin/activate

# Clean install compatible versions
pip uninstall eth-abi parsimonious web3 -y
pip install "eth-abi==4.2.1" "parsimonious==0.8.1" "web3==5.31.3" "python-dotenv"

echo "🧪 Testing..."
python -c "from ipaytools import iPayTools; print('✅ Import BERHASIL!')"

if [ $? -eq 0 ]; then
    echo "🎉 Python 3.13 compatibility FIXED!"
    echo "🚀 Ready for PyPI publish!"
else
    echo "❌ Still having issues, trying Python 3.12..."
    deactivate
    python3.12 -m venv venv312
    source venv312/bin/activate
    pip install web3 python-dotenv
    pip install -e .
    python -c "from ipaytools import iPayTools; print('✅ Python 3.12 working!')"
fi
