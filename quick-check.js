// quick-check.js
const { ethers } = require("hardhat");

async function quickCheck() {
    const contract = await ethers.getContractAt("IpayTools", "YOUR_CONTRACT_ADDRESS");
    console.log("Functions:", Object.keys(contract.interface.functions));
}

quickCheck();
