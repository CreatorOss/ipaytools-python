from ipaytools import iPayTools

# Initialize
tools = iPayTools()

# Register application (FREE)
tools.register_app("MyApp")

# Process payment (0.0001 ETH fee)
tools.use_tool()

# Check earnings
earnings = tools.get_developer_earnings()
print(f"Your earnings: {earnings} ETH")

# Withdraw earnings
tools.withdraw_earnings()
