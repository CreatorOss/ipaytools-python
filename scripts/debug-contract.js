// debug-contract.js
const { ethers } = require("hardhat");

async function debugContract() {
    try {
        const contractAddress = "YOUR_CONTRACT_ADDRESS_HERE";
        
        // Get contract instance
        const iPpayTools = await ethers.getContractFactory("iPpayTools");
        const contract = await iPayTools.attach(contractAddress);
        
        console.log("📋 Contract Info:");
        console.log("Address:", contract.address);
        console.log("---");
        
        // Check available functions
        console.log("🔍 Available Functions:");
        Object.keys(contract.interface.functions).forEach(func => {
            console.log("  -", func);
        });
        
        console.log("---");
        
        // Check if registerApp function exists
        const functionExists = contract.interface.functions["registerApp(address,string,string,uint256)"];
        console.log("✅ registerApp function exists:", !!functionExists);
        
    } catch (error) {
        console.error("❌ Debug error:", error);
    }
}

debugContract();
