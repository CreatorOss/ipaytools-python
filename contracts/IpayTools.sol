// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title iPayTools Fee Collection Contract
 * @dev Smart contract untuk fee sharing system
 * 70% untuk iPay team, 30% untuk app developer
 */
contract iPayTools {
    address public owner;
    uint256 public feePerUse = 0.0003 ether; // PROFITABLE FEE - Safe for gas up to 21 Gwei
    uint256 public totalEarnings;
    uint256 public totalTransactions;
    
    mapping(address => bool) public registeredApps;
    mapping(address => uint256) public developerEarnings;
    
    event ToolUsed(address indexed user, address indexed app, uint256 fee);
    event AppRegistered(address indexed app);
    event EarningsWithdrawn(address indexed to, uint256 amount);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }
    
    /**
     * @dev Function untuk menggunakan tools - bayar fee
     */
    function useTool() external payable {
        require(msg.value >= feePerUse, "Insufficient fee");
        require(registeredApps[msg.sender], "App not registered");
        
        totalTransactions++;
        
        // 70% untuk kita, 30% untuk app developer
        uint256 ourShare = (msg.value * 70) / 100;
        uint256 devShare = msg.value - ourShare;
        
        // Update earnings
        totalEarnings += ourShare;
        developerEarnings[msg.sender] += devShare;
        
        emit ToolUsed(tx.origin, msg.sender, msg.value);
    }
    
    /**
     * @dev Register aplikasi baru
     */
    function registerApp() external {
        require(!registeredApps[msg.sender], "App already registered");
        registeredApps[msg.sender] = true;
        emit AppRegistered(msg.sender);
    }
    
    /**
     * @dev Developer bisa withdraw earnings mereka
     */
    function withdrawEarnings() external {
        uint256 amount = developerEarnings[msg.sender];
        require(amount > 0, "No earnings to withdraw");
        
        developerEarnings[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
        
        emit EarningsWithdrawn(msg.sender, amount);
    }
    
    /**
     * @dev Owner bisa withdraw earnings iPay team
     */
    function withdrawOwnerEarnings() external onlyOwner {
        uint256 amount = totalEarnings;
        require(amount > 0, "No earnings to withdraw");
        
        totalEarnings = 0;
        payable(owner).transfer(amount);
        
        emit EarningsWithdrawn(owner, amount);
    }
    
    /**
     * @dev Update fee amount (hanya owner)
     */
    function setFeePerUse(uint256 _newFee) external onlyOwner {
        feePerUse = _newFee;
    }
    
    /**
     * @dev Get contract balance
     */
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
    
    /**
     * @dev Get developer earnings
     */
    function getDeveloperEarnings(address _developer) external view returns (uint256) {
        return developerEarnings[_developer];
    }
}
