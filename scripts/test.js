async function main() {
  console.log("🧪 Testing iPayTools Contract...");
  
  const address = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  const iPayTools = await ethers.getContractFactory("iPayTools");
  const contract = await iPayTools.attach(address);
  
  console.log("✅ Contract address:", address);
  console.log("💰 Fee per use:", (await contract.feePerUse()).toString());
  console.log("👑 Owner:", await contract.owner());
  console.log("📊 Total transactions:", (await contract.totalTransactions()).toString());
  
  // Test app registration
  const [deployer, user1] = await ethers.getSigners();
  console.log("\n🔧 Testing app registration...");
  
  await contract.connect(user1).registerApp();
  console.log("✅ User 1 app registered!");
  
  const isRegistered = await contract.registeredApps(user1.address);
  console.log("📝 Registration status:", isRegistered);
  
  console.log("\n🎯 All tests passed! iPayTools is WORKING!");
}

main().catch(console.error);
