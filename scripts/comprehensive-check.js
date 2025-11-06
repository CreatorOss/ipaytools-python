// comprehensive-check.js
const { ethers } = require("hardhat");

async function comprehensiveCheck() {
    const contractAddress = "YOUR_CONTRACT_ADDRESS_HERE";
    
    console.log("🔍 Comprehensive Contract Check");
    console.log("=================================");
    
    try {
        // 1. Get contract
        const IpayTools = await ethers.getContractFactory("IpayTools");
        const contract = IpayTools.attach(contractAddress);
        
        // 2. Check contract connection
        console.log("1. Contract Connection:");
        console.log("   ✅ Connected to:", contract.address);
        
        // 3. Check all functions
        console.log("2. Available Functions:");
        const functions = contract.interface.functions;
        Object.keys(functions).forEach((func, index) => {
            console.log(`   ${index + 1}. ${func}`);
        });
        
        // 4. Check if registerApp exists
        console.log("3. Register Function Check:");
        const registerFunctions = Object.keys(functions).filter(f => 
            f.includes("register")
        );
        
        if (registerFunctions.length > 0) {
            console.log("   ✅ Register functions found:");
            registerFunctions.forEach(f => console.log(`      - ${f}`));
        } else {
            console.log("   ❌ No register functions found!");
        }
        
        // 5. Try to estimate gas for registerApp (if exists)
        console.log("4. Function Test:");
        const [owner] = await ethers.getSigners();
        
        // Try different function signatures
        const testCases = [
            {
                name: "registerApp with 3 params",
                params: ["TestApp", "https://test.com", ethers.utils.parseEther("0.0001")]
            },
            {
                name: "registerApp with 4 params", 
                params: [owner.address, "TestApp", "https://test.com", ethers.utils.parseEther("0.0001")]
            }
        ];
        
        for (let test of testCases) {
            try {
                const gasEstimate = await contract.estimateGas["registerApp"](...test.params);
                console.log(`   ✅ ${test.name}: ${gasEstimate.toString()} gas`);
            } catch (e) {
                console.log(`   ❌ ${test.name}: ${e.reason || e.message}`);
            }
        }
        
    } catch (error) {
        console.error("❌ Comprehensive check failed:", error.message);
    }
}

comprehensiveCheck();
