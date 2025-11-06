#!/usr/bin/env python3
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ipaytools.core import iPayTools

def test_python_registration():
    try:
        print("🧪 Testing Python registration...")
        
        # Initialize iPayTools
        ipay = iPayTools()
        
        # Test registration
        print("1. Registering app...")
        result = ipay.register_app("TestApp")
        print("   ✅ Registration result:", result)
        
        print("2. Checking if registered...")
        is_registered = ipay.is_registered()
        print("   ✅ Is registered:", is_registered)
        
        print("🎉 Python test completed successfully!")
        
    except Exception as e:
        print("❌ Python test failed:", str(e))

if __name__ == "__main__":
    test_python_registration()
