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
