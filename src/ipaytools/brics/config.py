"""
BRICS Currency Configuration
"""

BRICS_CURRENCIES = {
    'CNY': {
        'name': 'Chinese Yuan',
        'symbol': '¥',
        'country': 'China',
        'trade_volume_idr': 100_000_000_000,  # $100B+ trade with Indonesia
        'priority': 1,
        'decimal_places': 2
    },
    'INR': {
        'name': 'Indian Rupee', 
        'symbol': '₹',
        'country': 'India',
        'trade_volume_idr': 30_000_000_000,   # $30B+ trade
        'priority': 2,
        'decimal_places': 2
    },
    'SAR': {
        'name': 'Saudi Riyal',
        'symbol': '﷼',
        'country': 'Saudi Arabia', 
        'trade_volume_idr': 8_000_000_000,    # $8B+ trade
        'priority': 3,
        'decimal_places': 2
    },
    'AED': {
        'name': 'UAE Dirham',
        'symbol': 'د.إ',
        'country': 'United Arab Emirates',
        'trade_volume_idr': 6_000_000_000,    # $6B+ trade
        'priority': 4,
        'decimal_places': 2
    },
    'RUB': {
        'name': 'Russian Ruble',
        'symbol': '₽',
        'country': 'Russia',
        'trade_volume_idr': 3_000_000_000,    # $3B+ trade
        'priority': 5,
        'decimal_places': 2
    },
    'BRL': {
        'name': 'Brazilian Real',
        'symbol': 'R$',
        'country': 'Brazil',
        'trade_volume_idr': 2_000_000_000,    # $2B+ trade
        'priority': 6,
        'decimal_places': 2
    },
    'ZAR': {
        'name': 'South African Rand',
        'symbol': 'R',
        'country': 'South Africa',
        'trade_volume_idr': 1_000_000_000,    # $1B+ trade
        'priority': 7,
        'decimal_places': 2
    },
    'EGP': {
        'name': 'Egyptian Pound',
        'symbol': '£',
        'country': 'Egypt',
        'trade_volume_idr': 500_000_000,      # $500M+ trade
        'priority': 8,
        'decimal_places': 2
    }
}

# Fee structure for BRICS currencies
BRICS_FEE_STRUCTURE = {
    'individual': {
        'CNY': 0.010,  # 1.0%
        'INR': 0.012,  # 1.2%
        'SAR': 0.015,  # 1.5%
        'AED': 0.015,  # 1.5%
        'RUB': 0.020,  # 2.0%
        'BRL': 0.020,  # 2.0%
        'ZAR': 0.020,  # 2.0%
        'EGP': 0.025   # 2.5%
    },
    'bundle': {
        'all_currencies': 0.008,  # 0.8% for all BRICS currencies
        'volume_discount': {
            'threshold_1m': 0.005,  # 0.5% for $1M+ monthly volume
            'threshold_5m': 0.003   # 0.3% for $5M+ monthly volume
        }
    }
}

# Target exchange rate providers for each currency
EXCHANGE_RATE_SOURCES = {
    'CNY': ['bank_indonesia', 'icbc', 'bank_of_china'],
    'INR': ['bank_indonesia', 'sbi', 'icici_bank'],
    'SAR': ['bank_indonesia', 'samba', 'sabb'],
    'AED': ['bank_indonesia', 'emirates_nbd', 'mashreq'],
    'RUB': ['bank_indonesia', 'sberbank', 'vtb'],
    'BRL': ['bank_indonesia', 'itau', 'bradesco'],
    'ZAR': ['bank_indonesia', 'standard_bank', 'absa'],
    'EGP': ['bank_indonesia', 'national_bank_egypt', 'cib']
}
