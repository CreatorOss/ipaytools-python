// find-contract.js
const { ethers } = require("hardhat");

async function findContract() {
    console.log("🔍 Mencari alamat kontrak...");
    
    try {
        // Method 1: Check dari deployment records
        const deployments = await ethers.getSigners();
        const deployer = deployments[0];
        console.log("📦 Deployer address:", deployer.address);
        
        // Method 2: Check dari network
        const network = await ethers.provider.getNetwork();
        console.log("🌐 Network:", network.name, "Chain ID:", network.chainId);
        
        // Method 3: Check transaction history untuk kontrak deployment
        console.log("\n📖 Checking deployment transactions...");
        const blockNumber = await ethers.provider.getBlockNumber();
        console.log("Current block:", blockNumber);
        
        // Check recent blocks untuk contract creation
        for (let i = blockNumber; i > blockNumber - 100; i--) {
            const block = await ethers.provider.getBlockWithTransactions(i);
            
            for (const tx of block.transactions) {
                if (tx.to === null && tx.creates) {
                    console.log("✅ Found contract deployment at block", i);
                    console.log("   Contract address:", tx.creates);
                    console.log("   Tx hash:", tx.hash);
                    
                    // Verify this is our contract
                    try {
                        const code = await ethers.provider.getCode(tx.creates);
                        if (code !== '0x') {
                            console.log("   ✅ Contract code deployed");
                            return tx.creates;
                        }
                    } catch (e) {
                        console.log("   ❌ Cannot verify contract code");
                    }
                }
            }
        }
        
    } catch (error) {
        console.error("❌ Error finding contract:", error);
    }
    
    return null;
}

findContract().then(address => {
    if (address) {
        console.log("\n🎯 CONTRACT FOUND:", address);
    } else {
        console.log("\n❌ No contract found in recent blocks");
    }
});
