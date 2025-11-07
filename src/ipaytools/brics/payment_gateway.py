"""
BRICS Payment Gateway
"""
import time
from web3 import Web3
import logging
from .exchange_rates import BRICSExchangeRateManager
from .config import BRICS_CURRENCIES, BRICS_FEE_STRUCTURE

class BRICSPaymentGateway:
    def __init__(self, w3, contract_address=None):
        self.w3 = w3
        self.contract_address = contract_address
        self.logger = logging.getLogger('ipaytools.brics.gateway')
        self.exchange_manager = BRICSExchangeRateManager(w3)
        
        # Initialize with default account
        if self.w3.eth.accounts:
            self.account = self.w3.eth.accounts[0]
        else:
            raise Exception("No accounts available")
            
    def send_brics_payment(self, to_currency, amount_idr, recipient_address, fee_type='individual'):
        """
        Send payment in BRICS currency
        """
        try:
            self.logger.info(f"🚀 Initiating BRICS payment: {amount_idr} IDR → {to_currency}")
            
            # Calculate payment details
            payment_details = self.exchange_manager.calculate_brics_payment(
                'IDR', to_currency, amount_idr, fee_type
            )
            
            self.logger.info(f"💰 Payment Details:")
            self.logger.info(f"   From: {amount_idr} IDR")
            self.logger.info(f"   To: {payment_details['final_amount']:.2f} {to_currency}")
            self.logger.info(f"   Exchange Rate: 1 {to_currency} = {payment_details['exchange_rate']} IDR")
            self.logger.info(f"   Fee: {payment_details['fee_percent']:.1f}% ({payment_details['fee_amount']:.2f} {to_currency})")
            
            # Simulate payment processing
            transaction_hash = self._simulate_brics_transaction(
                to_currency, 
                payment_details['final_amount'],
                recipient_address
            )
            
            payment_details['transaction_hash'] = transaction_hash
            payment_details['status'] = 'completed'
            
            self.logger.info(f"✅ BRICS payment completed: {transaction_hash}")
            return payment_details
            
        except Exception as e:
            self.logger.error(f"❌ BRICS payment failed: {e}")
            raise
            
    def receive_brics_payment(self, from_currency, amount_foreign, sender_address, fee_type='individual'):
        """
        Receive payment in BRICS currency and convert to IDR
        """
        try:
            self.logger.info(f"🔄 Receiving BRICS payment: {amount_foreign} {from_currency} → IDR")
            
            # Calculate receipt details
            receipt_details = self.exchange_manager.calculate_brics_payment(
                from_currency, 'IDR', amount_foreign, fee_type
            )
            
            self.logger.info(f"💰 Receipt Details:")
            self.logger.info(f"   From: {amount_foreign} {from_currency}")
            self.logger.info(f"   To: {receipt_details['final_amount']:.0f} IDR")
            self.logger.info(f"   Exchange Rate: 1 {from_currency} = {receipt_details['exchange_rate']} IDR")
            self.logger.info(f"   Fee: {receipt_details['fee_percent']:.1f}% ({receipt_details['fee_amount']:.0f} IDR)")
            
            # Simulate receipt processing
            transaction_hash = self._simulate_brics_receipt(
                from_currency,
                amount_foreign,
                sender_address
            )
            
            receipt_details['transaction_hash'] = transaction_hash
            receipt_details['status'] = 'completed'
            
            self.logger.info(f"✅ BRICS receipt completed: {transaction_hash}")
            return receipt_details
            
        except Exception as e:
            self.logger.error(f"❌ BRICS receipt failed: {e}")
            raise
            
    def _simulate_brics_transaction(self, currency, amount, recipient):
        """
        Simulate BRICS transaction (replace with actual banking API in production)
        """
        # Generate fake transaction hash for simulation
        fake_hash = Web3.keccak(text=f"brics_{currency}_{amount}_{recipient}_{int(time.time())}").hex()
        return fake_hash
        
    def _simulate_brics_receipt(self, currency, amount, sender):
        """
        Simulate BRICS receipt (replace with actual banking API in production)
        """
        # Generate fake transaction hash for simulation
        fake_hash = Web3.keccak(text=f"brics_receive_{currency}_{amount}_{sender}_{int(time.time())}").hex()
        return fake_hash
        
    def get_brics_balance(self, currency):
        """
        Get simulated balance for BRICS currency
        """
        # In production, this would check actual bank balances
        demo_balances = {
            'CNY': 100000,  # 100,000 CNY
            'INR': 5000000, # 5,000,000 INR
            'SAR': 50000,   # 50,000 SAR
            'AED': 50000,   # 50,000 AED
            'RUB': 1000000, # 1,000,000 RUB
            'BRL': 100000,  # 100,000 BRL
            'ZAR': 200000,  # 200,000 ZAR
            'EGP': 500000   # 500,000 EGP
        }
        
        return demo_balances.get(currency, 0)
        
    def get_brics_fee_quote(self, from_currency, to_currency, amount, fee_type='individual'):
        """
        Get fee quote for BRICS transaction
        """
        return self.exchange_manager.calculate_brics_payment(
            from_currency, to_currency, amount, fee_type
        )
