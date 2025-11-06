const { ethers } = require("hardhat");
const fs = require('fs');
const path = require('path');

async function getNewABI() {
    try {
        const iPayTools = await ethers.getContractFactory("iPayTools");
        const fullABI = iPayTools.interface.format(ethers.utils.FormatTypes.full);
        
        console.log("📋 NEW ABI:");
        console.log(JSON.stringify(JSON.parse(fullABI), null, 2));
        
        // Save to file
        const abiPath = path.join(__dirname, '..', 'abi.json');
        fs.writeFileSync(abiPath, fullABI);
        console.log("💾 ABI saved to abi.json");
        
        return fullABI;
    } catch (error) {
        console.error("❌ Error getting ABI:", error);
    }
}

getNewABI();
