"""
BRICS Exchange Rate Management
"""
import requests
import json
import time
from datetime import datetime, timedelta
from web3 import Web3
from .config import BRICS_CURRENCIES, BRICS_FEE_STRUCTURE, EXCHANGE_RATE_SOURCES
import logging

class BRICSExchangeRateManager:
    def __init__(self, w3):
        self.w3 = w3
        self.logger = logging.getLogger('ipaytools.brics')
        self.rates = {}
        self.last_updated = {}
        
    def get_brics_exchange_rate(self, currency, amount_idr=1):
        """
        Get exchange rate for BRICS currency to IDR
        """
        if currency not in BRICS_CURRENCIES:
            raise ValueError(f"Unsupported BRICS currency: {currency}")
            
        # For demo - in production, integrate with real exchange rate APIs
        demo_rates = {
            'CNY': 2100,  # 1 CNY = 2100 IDR
            'INR': 180,   # 1 INR = 180 IDR  
            'SAR': 3900,  # 1 SAR = 3900 IDR
            'AED': 3800,  # 1 AED = 3800 IDR
            'RUB': 150,   # 1 RUB = 150 IDR
            'BRL': 2800,  # 1 BRL = 2800 IDR
            'ZAR': 800,   # 1 ZAR = 800 IDR
            'EGP': 700    # 1 EGP = 700 IDR
        }
        
        rate = demo_rates.get(currency, 1)
        self.rates[currency] = rate
        self.last_updated[currency] = datetime.now()
        
        self.logger.info(f"💰 BRICS Exchange Rate: 1 {currency} = {rate} IDR")
        return rate
        
    def calculate_brics_payment(self, from_currency, to_currency, amount, fee_type='individual'):
        """
        Calculate BRICS payment with fees
        """
        if from_currency not in BRICS_CURRENCIES and from_currency != 'IDR':
            raise ValueError(f"Unsupported from currency: {from_currency}")
            
        if to_currency not in BRICS_CURRENCIES and to_currency != 'IDR':
            raise ValueError(f"Unsupported to currency: {to_currency}")
            
        # Get exchange rates
        if from_currency == 'IDR':
            rate = self.get_brics_exchange_rate(to_currency)
            foreign_amount = amount / rate
            base_currency = to_currency
        else:
            rate = self.get_brics_exchange_rate(from_currency) 
            foreign_amount = amount * rate
            base_currency = from_currency
            
        # Calculate fees
        if fee_type == 'bundle':
            fee_percent = BRICS_FEE_STRUCTURE['bundle']['all_currencies']  # 0.8% bundle fee
        else:
            fee_percent = BRICS_FEE_STRUCTURE['individual'].get(base_currency, 0.015)
            
        fee_amount = foreign_amount * fee_percent
        final_amount = foreign_amount - fee_amount
        
        return {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'exchange_rate': rate,
            'foreign_amount': foreign_amount,
            'fee_percent': fee_percent * 100,
            'fee_amount': fee_amount,
            'final_amount': final_amount,
            'timestamp': datetime.now().isoformat()
        }
        
    def get_brics_currency_info(self, currency):
        """
        Get detailed info for a BRICS currency
        """
        if currency not in BRICS_CURRENCIES:
            raise ValueError(f"Unsupported BRICS currency: {currency}")
            
        info = BRICS_CURRENCIES[currency].copy()
        info['current_rate'] = self.get_brics_exchange_rate(currency)
        info['fee_individual'] = BRICS_FEE_STRUCTURE['individual'].get(currency, 0.015) * 100
        info['fee_bundle'] = BRICS_FEE_STRUCTURE['bundle']['all_currencies'] * 100
        info['rate_sources'] = EXCHANGE_RATE_SOURCES.get(currency, [])
        
        return info
        
    def get_all_brics_rates(self):
        """
        Get exchange rates for all BRICS currencies
        """
        rates = {}
        for currency in BRICS_CURRENCIES:
            rates[currency] = {
                'rate': self.get_brics_exchange_rate(currency),
                'name': BRICS_CURRENCIES[currency]['name'],
                'symbol': BRICS_CURRENCIES[currency]['symbol'],
                'last_updated': self.last_updated.get(currency)
            }
        return rates
