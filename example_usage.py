#!/usr/bin/env python3
"""
Contoh Penggunaan iPayTools - Setelah Perbaikan
Menunjukkan cara menggunakan library dengan benar
"""

from src.ipaytools.core import iPayTools
from web3 import Web3

def example_basic():
    """Contoh penggunaan dasar"""
    print("=" * 60)
    print("📘 Contoh 1: Penggunaan Dasar")
    print("=" * 60)
    
    # 1. Initialize iPayTools
    print("\n1. Inisialisasi iPayTools...")
    tools = iPayTools()
    print(f"   ✅ Terhubung ke: {tools.rpc_url}")
    print(f"   ✅ Alamat kontrak: {tools.contract_address}")
    print(f"   ✅ Akun default: {tools.account}")

    # 2. Cek informasi kontrak
    print("\n2. Informasi Kontrak...")
    try:
        # Gunakan contract.functions langsung
        owner = tools.contract.functions.owner().call()
        fee = tools.get_fee()
        balance = tools.get_contract_balance()
        
        print(f"   📋 Owner: {owner}")
        print(f"   💰 Fee per use: {fee} ETH")
        print(f"   🏦 Contract balance: {balance} ETH")
    except Exception as e:
        print(f"   ❌ Error getting contract info: {e}")

    # 3. Cek status registrasi
    print("\n3. Cek Status Registrasi...")
    is_registered = tools.is_registered()
    print(f"   📝 Status: {'✅ Sudah terdaftar' if is_registered else '❌ Belum terdaftar'}")

    # 4. Register jika belum
    if not is_registered:
        print("\n4. Melakukan Registrasi...")
        print("   🔄 Mendaftarkan aplikasi...")
        try:
            result = tools.register_app("MyApp")
            if result:
                print("   ✅ Registrasi berhasil!")
                
                # Verify registration
                is_reg_after = tools.is_registered()
                print(f"   ✅ Verifikasi: {'Berhasil' if is_reg_after else 'Gagal'}")
            else:
                print("   ❌ Registrasi gagal!")
        except Exception as e:
            print(f"   ❌ Error during registration: {e}")
    else:
        print("\n4. Aplikasi sudah terdaftar, skip registrasi")

    # 5. Cek earnings
    print("\n5. Cek Pendapatan...")
    try:
        earnings = tools.get_developer_earnings()
        print(f"   💵 Pendapatan developer: {earnings} ETH")
    except Exception as e:
        print(f"   ❌ Error checking earnings: {e}")

    print("\n" + "=" * 60)

def example_multiple_accounts():
    """Contoh dengan multiple accounts"""
    print("\n" + "=" * 60)
    print("📘 Contoh 2: Multiple Accounts")
    print("=" * 60)

    tools = iPayTools()

    print("\n📊 Status Registrasi Semua Akun:")
    print("-" * 60)

    registered_count = 0
    for i, account in enumerate(tools.w3.eth.accounts[:3], 1):  # Cek 3 akun pertama
        try:
            is_reg = tools.is_registered(account)
            status = "✅ Terdaftar" if is_reg else "❌ Belum terdaftar"
            if is_reg:
                registered_count += 1
            
            earnings = tools.get_developer_earnings(account)
            print(f"   Akun {i}: {account[:10]}...")
            print(f"      Status: {status}")
            print(f"      Earnings: {earnings} ETH")
            print()

        except Exception as e:
            print(f"   ❌ Error checking account {i}: {e}")

    print(f"📈 Total terdaftar: {registered_count}/{len(tools.w3.eth.accounts[:3])}")

    print("\n" + "=" * 60)

def example_use_tool():
    """Contoh penggunaan tool dengan pembayaran"""
    print("\n" + "=" * 60)
    print("📘 Contoh 3: Penggunaan Tool")
    print("=" * 60)

    tools = iPayTools()

    print("\n🔧 Simulasi Penggunaan Tool:")
    print("-" * 40)
    
    # Cek status sebelum
    earnings_before = tools.get_developer_earnings()
    contract_balance_before = tools.get_contract_balance()
    
    print(f"Sebelum:")
    print(f"  💰 Earnings developer: {earnings_before} ETH")
    print(f"  🏦 Contract balance: {contract_balance_before} ETH")
    
    # Gunakan tool (simulasi - comment jika tidak ingin benar-benar bayar)
    print(f"\n🎯 Akan menggunakan tool (Fee: {tools.get_fee()} ETH)")
    
    # UNCOMMENT baris berikut jika ingin benar-benar test pembayaran
    # try:
    #     if tools.use_tool():
    #         print("✅ Tool berhasil digunakan!")
    #     else:
    #         print("❌ Gagal menggunakan tool")
    # except Exception as e:
    #     print(f"❌ Error: {e}")
    
    print("💡 Demo mode - Pembayaran tidak benar-benar dilakukan")
    
    print("\n" + "=" * 60)

def example_custom_config():
    """Contoh dengan konfigurasi custom"""
    print("\n" + "=" * 60)
    print("📘 Contoh 4: Konfigurasi Custom")
    print("=" * 60)

    # Gunakan contract address dan RPC URL custom
    custom_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    custom_rpc = "http://localhost:8545"

    print(f"\n🔧 Menggunakan konfigurasi custom:")
    print(f"   Contract: {custom_address}")
    print(f"   RPC URL: {custom_rpc}")

    try:
        tools = iPayTools(
            contract_address=custom_address,
            rpc_url=custom_rpc
        )

        print(f"\n✅ Berhasil terhubung!")
        print(f"   Akun: {tools.account}")
        
        # Test basic functions
        fee = tools.get_fee()
        balance = tools.get_contract_balance()
        is_reg = tools.is_registered()
        
        print(f"   Fee: {fee} ETH")
        print(f"   Balance: {balance} ETH")
        print(f"   Registered: {'✅ Ya' if is_reg else '❌ Tidak'}")

    except Exception as e:
        print(f"❌ Error dengan konfigurasi custom: {e}")

    print("\n" + "=" * 60)

def example_error_handling():
    """Contoh error handling yang baik"""
    print("\n" + "=" * 60)
    print("📘 Contoh 5: Error Handling")
    print("=" * 60)

    # Test 1: Koneksi normal
    print("\n1. Testing koneksi normal...")
    try:
        tools = iPayTools()
        print("   ✅ Koneksi berhasil")
        print(f"   Akun: {tools.account}")
    except Exception as e:
        print(f"   ❌ Koneksi gagal: {e}")

    # Test 2: Registrasi
    print("\n2. Testing registrasi...")
    try:
        tools = iPayTools()
        if not tools.is_registered():
            result = tools.register_app()
            if result:
                print("   ✅ Registrasi berhasil")
            else:
                print("   ⚠️  Registrasi gagal")
        else:
            print("   ℹ️  Sudah terdaftar sebelumnya")
    except Exception as e:
        print(f"   ❌ Error registrasi: {e}")

    # Test 3: Invalid address
    print("\n3. Testing invalid address...")
    try:
        tools = iPayTools()
        # Coba dengan address yang tidak ada
        is_reg = tools.is_registered("0x0000000000000000000000000000000000000000")
        print(f"   ✅ Check invalid address: {is_reg}")
    except Exception as e:
        print(f"   ❌ Error invalid address: {e}")

    print("\n" + "=" * 60)

def example_withdraw():
    """Contoh withdraw earnings"""
    print("\n" + "=" * 60)
    print("📘 Contoh 6: Withdraw Earnings")
    print("=" * 60)

    tools = iPayTools()

    print("\n💰 Withdraw Simulation:")
    print("-" * 40)
    
    try:
        earnings = tools.get_developer_earnings()
        print(f"   Pendapatan tersedia: {earnings} ETH")
        
        if earnings > 0:
            print("   🎯 Dapat melakukan withdraw")
            # UNCOMMENT untuk benar-benar withdraw
            # if tools.withdraw_earnings():
            #     print("   ✅ Withdraw berhasil!")
            # else:
            #     print("   ❌ Withdraw gagal!")
            print("   💡 Demo mode - Withdraw tidak dilakukan")
        else:
            print("   ℹ️  Tidak ada pendapatan untuk withdraw")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)

def main():
    """Main function - jalankan semua contoh"""
    print("\n" + "🎓 TUTORIAL PENGGUNAAN iPAYTOOLS".center(60, "="))
    print("Setelah Perbaikan - Versi yang Benar\n")

    try:
        # Contoh 1: Basic usage
        example_basic()

        # Contoh 2: Multiple accounts
        example_multiple_accounts()

        # Contoh 3: Use tool
        example_use_tool()

        # Contoh 4: Custom config
        example_custom_config()

        # Contoh 5: Error handling
        example_error_handling()

        # Contoh 6: Withdraw
        example_withdraw()

        print("\n" + "✅ SEMUA CONTOH SELESAI!".center(60, "="))
        print("\n💡 Tips Penggunaan:")
        print("   1. registerApp() - GRATIS, tidak butuh ETH")
        print("   2. useTool() - Berbayar 0.0001 ETH")
        print("   3. withdrawEarnings() - Tarik pendapatan")
        print("   4. Hanya bayar gas fee untuk transaksi")
        print("\n🔧 Fungsi Available:")
        print("   - register_app()")
        print("   - is_registered()") 
        print("   - use_tool()")
        print("   - get_developer_earnings()")
        print("   - withdraw_earnings()")
        print("   - get_fee()")
        print("   - get_contract_balance()")
        print("\n" + "=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Error utama: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
