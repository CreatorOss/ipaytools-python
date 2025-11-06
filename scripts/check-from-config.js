// check-from-config.js
const { ethers, network } = require("hardhat");

async function checkFromConfig() {
    console.log("⚙️ Checking from hardhat config...");
    
    // Get all signers (accounts)
    const [deployer] = await ethers.getSigners();
    console.log("👤 Deployer:", deployer.address);
    
    // Check balance
    const balance = await deployer.getBalance();
    console.log("💰 Balance:", ethers.utils.formatEther(balance), "ETH");
    
    // Check if contract is deployed in this session
    console.log("\n🔍 Looking for IpayTools contract...");
    
    try {
        // Try to get contract factory
        const IpayTools = await ethers.getContractFactory("IpayTools");
        console.log("✅ IpayTools contract factory loaded");
        
        // Check if we have deployments
        const deployments = require('hardhat').deployments;
        if (deployments) {
            const ipayToolsDeployment = await deployments.get('IpayTools');
            console.log("🎯 Deployed IpayTools at:", ipayToolsDeployment.address);
            return ipayToolsDeployment.address;
        }
    } catch (error) {
        console.log("❌ Cannot get contract factory:", error.message);
    }
    
    return null;
}

checkFromConfig().then(address => {
    if (address) {
        console.log("\n✅ USE THIS ADDRESS:", address);
    }
});
