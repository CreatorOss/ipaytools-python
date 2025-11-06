const hre = require("hardhat");

async function main() {
  console.log("🔄 Updating iPayTools fee to 0.0002 ETH...");
  
  const [owner] = await hre.ethers.getSigners();
  const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  
  // Get contract instance
  const iPayTools = await hre.ethers.getContractAt("iPayTools", contractAddress);
  
  // Check current fee
  const currentFee = await iPayTools.feePerUse();
  console.log("📊 Current fee:", hre.ethers.formatEther(currentFee), "ETH");
  
  // Update fee to 0.0002 ETH
  console.log("🔄 Setting new fee to 0.0002 ETH...");
  const tx = await iPayTools.setFeePerUse(hre.ethers.parseEther("0.0002"));
  await tx.wait();
  
  // Verify new fee
  const newFee = await iPayTools.feePerUse();
  console.log("✅ New fee:", hre.ethers.formatEther(newFee), "ETH");
  console.log("🎉 Fee updated successfully!");
}

main().catch(console.error);
