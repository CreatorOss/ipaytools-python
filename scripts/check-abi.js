const { ethers } = require("hardhat");

async function checkABI() {
    const iPayTools = await ethers.getContractFactory("iPayTools");
    const abi = iPayTools.interface.fragments;
    
    console.log("📋 Full ABI:");
    abi.forEach(fragment => {
        if (fragment.type === "function") {
            console.log(`🔹 ${fragment.name}(${fragment.inputs.map(i => i.type).join(', ')})`);
        }
    });
}

checkABI();
