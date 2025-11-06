## [0.1.1] - 2024-11-06

### Added
- GitHub repository integration
- Updated author information
- Better documentation

### Fixed
- Updated GitHub URL in setup.py

## v0.2.1 ($(date +%Y-%m-%d))
### Fixed
- Memperbaiki kesalahan perhitungan profitability 
- Meningkatkan proteksi anti-loss protection
- Memperbaiki error attribute 'default_address'
- Optimasi algoritma fee adjustment

### Features
- Auto fee adjustment pada initialization
- Transaction rejection untuk fee yang tidak profitable
- Minimum 20% profit margin requirement
- 30% safety buffer dalam perhitungan fee

### Testing
- Semua test anti-loss protection passed
- Profitability verification working
- System sekarang aman dari kerugian

## v0.3.0 ($(date +%Y-%m-%d))
### ANTI-RUGI REAL-TIME SYSTEM
- **SETIAP transaksi check current gas price**
- **Real-time minimum fee calculation** 
- **Safety buffers: 20% gas price, 30% gas estimate**
- **Auto-rejection untuk unprofitable transactions**
- **Method baru: use_tool_safe() untuk maximum protection**

### Features
- get_current_gas_price() dengan safety buffer
- calculate_minimum_profitable_fee() real-time  
- use_tool_safe() - metode ANTI-RUGI
- Enhanced profitability checks

## v0.3.3 ($(date +%Y-%m-%d))
### Contract Compatibility Fix
- **Fixed contract compatibility** - hanya menggunakan function yang tersedia
- **Simplified transaction** - tanpa function call, hanya transfer ETH
- **Enhanced gas estimation** - menggunakan estimate_gas dasar
- **Better error handling** - untuk berbagai scenario contract

### Features
- Tetap maintain anti-rugi protection
- Real-time gas price checking
- Profitability validation
- Safe transaction execution
