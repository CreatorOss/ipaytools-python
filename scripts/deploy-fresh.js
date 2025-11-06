const { ethers } = require("hardhat");

async function deployFresh() {
    try {
        console.log("🚀 Deploying fresh iPayTools contract...");
        
        // Deploy baru
        const iPayTools = await ethers.getContractFactory("iPayTools");
        const contract = await iPayTools.deploy();
        await contract.deployed();
        
        console.log("✅ New contract deployed:", contract.address);
        
        // Test semua fungsi
        console.log("\n🧪 Testing all functions...");
        
        const [owner, user] = await ethers.getSigners();
        
        // Test 1: Fungsi view
        console.log("1. Testing view functions...");
        const ownerAddress = await contract.owner();
        const fee = await contract.feePerUse();
        const balance = await contract.getContractBalance();
        
        console.log("   ✅ Owner:", ownerAddress);
        console.log("   ✅ Fee per use:", ethers.utils.formatEther(fee), "ETH");
        console.log("   ✅ Contract balance:", ethers.utils.formatEther(balance), "ETH");
        
        // Test 2: registeredApps (seharusnya false untuk address baru)
        console.log("2. Testing registeredApps...");
        const isRegistered = await contract.registeredApps(user.address);
        console.log("   ✅ registeredApps:", isRegistered);
        
        // Test 3: Register app
        console.log("3. Testing registerApp...");
        const tx = await contract.connect(user).registerApp();
        await tx.wait();
        console.log("   ✅ registerApp success");
        
        // Test 4: Verify registration
        console.log("4. Verifying registration...");
        const isRegisteredAfter = await contract.registeredApps(user.address);
        console.log("   ✅ registeredApps after:", isRegisteredAfter);
        
        // Test 5: developerEarnings
        console.log("5. Testing developerEarnings...");
        const earnings = await contract.getDeveloperEarnings(user.address);
        console.log("   ✅ developerEarnings:", ethers.utils.formatEther(earnings), "ETH");
        
        console.log("\n🎉 ALL TESTS PASSED!");
        console.log("📝 Contract address:", contract.address);
        
        return contract.address;
        
    } catch (error) {
        console.error("❌ Deployment failed:", error.message);
        return null;
    }
}

deployFresh().then(address => {
    if (address) {
        console.log("\n💾 Save this address in your Python code!");
    }
});
