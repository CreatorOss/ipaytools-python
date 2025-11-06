const { ethers } = require("hardhat");

async function testRegister() {
    try {
        console.log("🧪 Testing registerApp function...");
        
        const iPayTools = await ethers.getContractFactory("iPayTools");
        const contract = await iPayTools.attach("0x5FbDB2315678afecb367f032d93F642f64180aa3");
        
        const [deployer, user] = await ethers.getSigners();
        
        console.log("👤 Testing with address:", user.address);
        
        // Check jika sudah registered
        const isRegistered = await contract.registeredApps(user.address);
        console.log("📋 Already registered?", isRegistered);
        
        if (!isRegistered) {
            console.log("🆕 Registering new app...");
            
            // Register tanpa parameter
            const tx = await contract.connect(user).registerApp();
            await tx.wait();
            
            console.log("✅ Registration successful!");
            
            // Verify registration
            const registered = await contract.registeredApps(user.address);
            console.log("📋 Registration verified:", registered);
        } else {
            console.log("ℹ️ Already registered");
        }
        
        // Check contract balance
        const balance = await contract.getContractBalance();
        console.log("💰 Contract balance:", ethers.utils.formatEther(balance), "ETH");
        
    } catch (error) {
        console.error("❌ Test failed:", error.message);
    }
}

testRegister();
