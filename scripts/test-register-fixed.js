const { ethers } = require("hardhat");

async function testRegisterFixed() {
    try {
        console.log("🧪 Testing registerApp function (Fixed)...");
        
        const iPayTools = await ethers.getContractFactory("iPayTools");
        const contract = await iPayTools.attach("0x5FbDB2315678afecb367f032d93F642f64180aa3");
        
        const [deployer, user] = await ethers.getSigners();
        
        console.log("👤 Testing with address:", user.address);
        
        // Test 1: Coba panggil registerApp tanpa parameter
        console.log("1. Testing registerApp() without parameters...");
        try {
            const tx = await contract.connect(user).registerApp();
            await tx.wait();
            console.log("   ✅ registerApp() success!");
        } catch (e) {
            console.log("   ❌ registerApp() failed:", e.message);
        }
        
        // Test 2: Cek registeredApps dengan cara yang benar
        console.log("2. Checking registration status...");
        try {
            const isRegistered = await contract.registeredApps(user.address);
            console.log("   ✅ registeredApps check:", isRegistered);
        } catch (e) {
            console.log("   ❌ registeredApps check failed:", e.message);
        }
        
        // Test 3: Cek fungsi lain untuk verifikasi kontrak berfungsi
        console.log("3. Testing other functions...");
        try {
            const owner = await contract.owner();
            const fee = await contract.feePerUse();
            const balance = await contract.getContractBalance();
            
            console.log("   ✅ Owner:", owner);
            console.log("   ✅ Fee per use:", ethers.utils.formatEther(fee), "ETH");
            console.log("   ✅ Contract balance:", ethers.utils.formatEther(balance), "ETH");
        } catch (e) {
            console.log("   ❌ Other functions failed:", e.message);
        }
        
    } catch (error) {
        console.error("❌ Test failed:", error.message);
    }
}

testRegisterFixed();
