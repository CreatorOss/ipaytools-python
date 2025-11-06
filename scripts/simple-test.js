async function main() {
  console.log("🧪 Simple Contract Test...");
  
  // Deploy fresh contract
  const iPayTools = await ethers.getContractFactory("iPayTools");
  const contract = await iPayTools.deploy();
  await contract.deployed();
  
  console.log("✅ New contract deployed to:", contract.address);
  
  // Test basic functions
  console.log("💰 Fee per use:", (await contract.feePerUse()).toString());
  console.log("👑 Owner:", await contract.owner());
  console.log("📊 Total transactions:", (await contract.totalTransactions()).toString());
  
  // Save new address
  require('fs').writeFileSync('new-address.txt', contract.address);
  console.log("🎉 Contract is WORKING!");
}

main().catch(console.error);
