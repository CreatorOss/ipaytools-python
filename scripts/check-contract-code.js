const { ethers } = require("hardhat");

async function checkContractCode() {
    const address = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
    
    console.log("🔍 Checking contract code at:", address);
    
    const code = await ethers.provider.getCode(address);
    console.log("Contract code length:", code.length);
    console.log("Is contract?", code !== '0x');
    
    if (code === '0x') {
        console.log("❌ Contract has self-destructed!");
    } else {
        console.log("✅ Contract code exists");
    }
}

checkContractCode();
