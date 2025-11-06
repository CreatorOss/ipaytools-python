async function main() {
  console.log("🚀 Deploying iPayTools Contract...");
  
  // Gunakan "iPayTools" (huruf kecil i)
  const iPayTools = await ethers.getContractFactory("iPayTools");
  console.log("📦 Deploying contract...");
  
  const ipayTools = await iPayTools.deploy();
  await ipayTools.deployed();
  
  console.log("✅ iPayTools deployed to:", ipayTools.address);
  console.log("💰 Fee per use:", (await ipayTools.feePerUse()).toString());
  console.log("👑 Owner:", await ipayTools.owner());
  
  // Save deployment info
  const fs = require('fs');
  fs.writeFileSync('deployed-address.txt', ipayTools.address);
  
  const deploymentInfo = {
    contract: "iPayTools",
    address: ipayTools.address,
    network: "localhost",
    fee: (await ipayTools.feePerUse()).toString(),
    owner: await ipayTools.owner(),
    timestamp: new Date().toISOString()
  };
  
  fs.writeFileSync('deployment-info.json', JSON.stringify(deploymentInfo, null, 2));
  console.log("💾 Deployment info saved!");
  console.log("🎉 Contract ready for use!");
}

main().catch(console.error);
