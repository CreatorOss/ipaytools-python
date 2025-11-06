const { ethers } = require("hardhat");

async function debugContract() {
    try {
        console.log("🔍 Debug iPayTools Contract...");
        
        // Get contract factory dengan nama yang benar
        const iPayTools = await ethers.getContractFactory("iPayTools");
        console.log("✅ iPayTools contract factory loaded");
        
        // Coba cari alamat kontrak dari deployments
        const fs = require('fs');
        const path = require('path');
        const deploymentsPath = path.join(__dirname, '..', 'deployments');
        
        let contractAddress = null;
        
        if (fs.existsSync(deploymentsPath)) {
            console.log("📁 Checking deployments folder...");
            const networks = fs.readdirSync(deploymentsPath);
            
            for (const network of networks) {
                const networkPath = path.join(deploymentsPath, network);
                const files = fs.readdirSync(networkPath);
                const jsonFiles = files.filter(f => f.endsWith('.json') && !f.startsWith('.'));
                
                for (const file of jsonFiles) {
                    const filePath = path.join(networkPath, file);
                    const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
                    console.log(`📍 ${file}: ${content.address}`);
                    
                    if (file.includes('iPayTools') || file.includes('IPayTools')) {
                        contractAddress = content.address;
                        console.log(`🎯 Found iPayTools contract: ${contractAddress}`);
                    }
                }
            }
        }
        
        // Jika tidak ditemukan, coba deploy baru
        if (!contractAddress) {
            console.log("🆕 No existing contract found. Deploying new one...");
            const contract = await iPayTools.deploy();
            await contract.deployed();
            contractAddress = contract.address;
            console.log("✅ New contract deployed at:", contractAddress);
        }
        
        // Attach ke contract
        const contract = await iPayTools.attach(contractAddress);
        
        console.log("\n📋 Contract Info:");
        console.log("Address:", contract.address);
        console.log("---");
        
        // Check available functions
        console.log("🔍 Available Functions:");
        const functions = contract.interface.functions;
        Object.keys(functions).forEach((func, index) => {
            console.log(`  ${index + 1}. ${func}`);
        });
        
        console.log("---");
        
        // Check jika registerApp ada
        const registerFunctions = Object.keys(functions).filter(f => 
            f.toLowerCase().includes('register')
        );
        
        if (registerFunctions.length > 0) {
            console.log("✅ Register functions found:");
            registerFunctions.forEach(f => console.log(`   - ${f}`));
        } else {
            console.log("❌ No register functions found!");
        }
        
        return contractAddress;
        
    } catch (error) {
        console.error("❌ Debug error:", error.message);
        return null;
    }
}

debugContract().then(address => {
    if (address) {
        console.log("\n🎯 CONTRACT READY:", address);
    }
});
