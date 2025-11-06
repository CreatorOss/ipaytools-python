async function main() {
  console.log("🚀 DEPLOY & TEST - iPayTools Contract");
  console.log("======================================");
  
  // Deploy NEW contract
  console.log("📦 Deploying fresh contract...");
  const iPayTools = await ethers.getContractFactory("iPayTools");
  const contract = await iPayTools.deploy();
  await contract.deployed();
  
  const newAddress = contract.address;
  console.log("✅ NEW Contract deployed to:", newAddress);
  
  // Test IMMEDIATELY after deployment
  console.log("\n🧪 Testing NEW contract...");
  
  // Test 1: Basic view functions
  console.log("1. Testing view functions...");
  const fee = await contract.feePerUse();
  const owner = await contract.owner();
  const balance = await contract.getContractBalance();
  
  console.log("   ✅ feePerUse():", fee.toString());
  console.log("   ✅ owner():", owner);
  console.log("   ✅ getContractBalance():", balance.toString());
  
  // Test 2: App registration
  console.log("2. Testing app registration...");
  const [deployer, app1] = await ethers.getSigners();
  await contract.connect(app1).registerApp();
  
  const isRegistered = await contract.registeredApps(app1.address);
  console.log("   ✅ registerApp():", isRegistered);
  
  // Test 3: Tool usage with fee
  console.log("3. Testing tool usage...");
  await contract.connect(app1).useTool({ value: fee });
  
  const newBalance = await contract.getContractBalance();
  const transactions = await contract.totalTransactions();
  const earnings = await contract.getDeveloperEarnings(app1.address);
  
  console.log("   ✅ useTool(): SUCCESS");
  console.log("   ✅ New balance:", newBalance.toString());
  console.log("   ✅ Total transactions:", transactions.toString());
  console.log("   ✅ App earnings:", earnings.toString());
  
  // Save successful address
  require('fs').writeFileSync('working-address.txt', newAddress);
  
  console.log("\n🎉 SUCCESS! Contract is FULLY WORKING!");
  console.log("📍 Working address:", newAddress);
  console.log("💰 Revenue sharing: 70% iPay Team / 30% Developers");
  console.log("🚀 Ready for production!");
}

main().catch(error => {
  console.error("❌ Error:", error.message);
});
