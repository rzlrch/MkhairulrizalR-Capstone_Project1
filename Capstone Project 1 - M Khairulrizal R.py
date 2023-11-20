import os
import json

class SistemRentalMobil:
    def __init__(self):
        self.mobil = {}
        self.transaksi = []
        self.id_mobil_counter = 1
        self.data_file = 'mobil.json'
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.mobil = data.get('mobil', {})
                self.transaksi = data.get('transaksi', [])
        except FileNotFoundError:
            self.mobil = {}
            self.transaksi = []
        except json.JSONDecodeError:
            self.mobil = {}
            self.transaksi = []

    def save_data(self):
        data = {'mobil': self.mobil, 'transaksi': self.transaksi}

        try:
            json.dumps(data)
        except json.JSONDecodeError:
            print("Data tidak valid. Gagal menyimpan.")
            return

        with open(self.data_file, 'w') as file:
            json.dump(data, file)

    def generate_mobil_id(self):
        mobil_id = str(self.id_mobil_counter)
        self.id_mobil_counter += 1
        return mobil_id

    def tampilkan_menu(self):
        self.clear_screen()
        print("=" * 60)
        print("       HELLO!  WELCOME TO")
        print("       RIZAL  TRANSLUXURY")
        print("=" * 60, "\n")
        print("1. TAMPILKAN MOBIL TERSEDIA")
        print("2. SEWA MOBIL")
        print("3. KEMBALIKAN MOBIL")
        print("4. TAMPILKAN TRANSAKSI")
        print("5. TAMBAHKAN DATA MOBIL BARU")
        print("6. HAPUS DATA MOBIL")
        print("7. HAPUS RIWAYAT TRANSAKSI\n")
        print("8. KELUAR\n")
        print("=" * 60)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def tampilkan_mobil(self):
        self.clear_screen()
        print("-" * 60, "\n")
        print("MOBIL TERSEDIA : ")
        print("\n{:<10} | {:<15} | {:<15} | {:<15} | {:<20} | {:<15}".format("ID", "MEREK", "TRANSMISI", "TAHUN", "HARGA SEWA (Rp/hari)", "STATUS"))
        print("=" * 106)
        for mobil_id, info in self.mobil.items():
            print("{:<10} | {:<15} | {:<15} | {:<15} | {:<20} | {:<15}".format(mobil_id, info['merek'], info['transmisi'], info['tahun'], info['harga'], "Tersedia" if info['tersedia'] else "Tidak Tersedia"))
        print("=" * 106)

        for transaksi in self.transaksi:
            mobil_id = transaksi['mobil_id']
            if mobil_id in self.mobil and not self.mobil[mobil_id]['tersedia']:
                self.mobil[mobil_id]['tersedia'] = True

        input("\n--- TEKAN 'ENTER' UNTUK KEMBALI KE MENU UTAMA ---   ")

    def tambah_mobil(self, merek, transmisi, tahun, harga):
        self.clear_screen()

        mobil_id = self.generate_mobil_id()
        while mobil_id in self.mobil:
            mobil_id = self.generate_mobil_id()

        self.mobil[mobil_id] = {'merek': merek, 'transmisi': transmisi, 'tahun': tahun, 'harga': harga, 'tersedia': True}

        print(f"Data mobil {merek} dengan ID {mobil_id} terdaftar!")

        self.save_data()
        input("\n--- TEKAN 'ENTER' UNTUK KEMBALI KE MENU UTAMA ---   ")

    def hapus_mobil(self, mobil_id):
        self.clear_screen()
        if mobil_id in self.mobil and self.mobil[mobil_id]['tersedia']:
            del self.mobil[mobil_id]
            print(f"\nMobil dengan ID {mobil_id} berhasil dihapus dari sistem.")
        elif mobil_id in self.mobil and not self.mobil[mobil_id]['tersedia']:
            print("\nMobil tidak dapat dihapus karena sedang disewa.")
        else:
            print("\nMobil tidak ditemukan.")
        input("\n--- TEKAN 'ENTER' UNTUK KEMBALI KE MENU UTAMA ---   ")

    def sewa_mobil(self, mobil_id, hari):
        self.clear_screen()
        print("-" * 60, "\n")
        
        if not self.mobil:
            print("\nData mobil belum ditambahkan ke Cart. Silakan tambahkan mobil terlebih dahulu.")
        elif mobil_id not in self.mobil:
            print("\nID mobil tidak valid. Silakan masukkan ID yang benar.")
        elif not self.mobil[mobil_id]['tersedia']:
            print("\nMobil tidak tersedia untuk disewa.")
        else:
            try:
                hari = int(hari)
                if hari <= 0:
                    raise ValueError("Jumlah hari harus lebih dari 0.")
                
                harga = self.mobil[mobil_id]['harga']
                total_biaya = harga * hari
                transaksi = {'merek': self.mobil[mobil_id]['merek'], 'mobil_id': mobil_id, 'hari': hari, 'total_biaya': total_biaya}
                self.transaksi.append(transaksi)
                self.mobil[mobil_id]['tersedia'] = False
                print(f"\nMobil       : {self.mobil[mobil_id]['merek']}\nDengan ID   : {mobil_id}\nDisewa      : {hari} hari\nTotal Biaya : Rp {total_biaya}")

                self.save_data()
            except ValueError as e:
                print(f"\nError: {str(e)}")
                print("Masukkan jumlah hari yang valid.")

        input("\n--- TEKAN 'ENTER' UNTUK KEMBALI KE MENU UTAMA ---   ")

    def kembalikan_mobil(self, mobil_id):
        self.clear_screen()
        print("-" * 60, "\n")

        if mobil_id not in self.mobil:
            print("\nMobil tidak ditemukan.")
        elif self.mobil[mobil_id]['tersedia']:
            print("\nMobil tidak sedang disewa.")
        else:
            self.mobil[mobil_id]['tersedia'] = True
            print(f"\nMobil {self.mobil[mobil_id]['merek']} dengan ID {mobil_id} dikembalikan. Terima kasih!")

        input("\n--- TEKAN 'ENTER' UNTUK KEMBALI KE MENU UTAMA ---   ")

    def tampilkan_transaksi(self):
        self.clear_screen()
        print("-" * 60, "\n")
        print("RIWAYAT TRANSAKSI :\n")
        if not self.transaksi:
            print("-- BELUM ADA TRANSAKSI --")
        else:
            total_pendapatan = 0
            for transaksi in self.transaksi:
                mobil_id = transaksi['mobil_id']
                merek_mobil = self.mobil[mobil_id]['merek']
                print(f"Mobil Merek : {merek_mobil} \nJumlah Hari : {transaksi['hari']} \nTotal Biaya : Rp {transaksi['total_biaya']}\n")
                total_pendapatan += transaksi['total_biaya']

            print(f"Total Pendapatan: Rp {total_pendapatan}\n")
        input("\n--- TEKAN 'ENTER' UNTUK KEMBALI KE MENU UTAMA ---   ")

    def hapus_riwayat_transaksi(self):
        self.clear_screen()
        print("-" * 60, "\n")
        konfirmasi = input("Apakah Anda yakin ingin menghapus riwayat transaksi? (ya/tidak): ").lower()
        if konfirmasi == 'ya':
            self.transaksi = []
            print("\nRiwayat transaksi berhasil dihapus.")
        elif konfirmasi == 'tidak':
            print("\nPenghapusan riwayat transaksi dibatalkan.")
        else:
            print("Input tidak valid. Harap masukkan 'ya' atau 'tidak'.")
        input("\n--- TEKAN 'ENTER' UNTUK KEMBALI KE MENU UTAMA ---   ")

    def input_angka(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Masukkan harus berupa angka. Coba lagi.")

# EKSEKUSI PROGRAM
if __name__ == "__main__":
    sistem_rental = SistemRentalMobil()

    while True:
        sistem_rental.tampilkan_menu()
        pilihan = input("\nMasukkan pilihan Menu, Untuk melanjutkan program! (1-8) : ")

        if pilihan == '1':
            sistem_rental.tampilkan_mobil()
        elif pilihan == '2':
            mobil_id = input("\nMasukkan ID mobil yang ingin Anda sewa: ")
            hari = input("Masukkan jumlah hari untuk disewa: ")
            sistem_rental.sewa_mobil(mobil_id, hari)
        elif pilihan == '3':
            mobil_id = input("\nMasukkan ID mobil yang ingin Anda kembalikan: ")
            sistem_rental.kembalikan_mobil(mobil_id)
        elif pilihan == '4':
            sistem_rental.tampilkan_transaksi()
        elif pilihan == '5':
            sistem_rental.tambah_mobil(
                input("\nMasukkan merek mobil yang ingin ditambahkan: "),
                input("Masukkan jenis transmisi mobil: "),
                sistem_rental.input_angka("Masukkan tahun mobil: "),
                sistem_rental.input_angka("Masukkan harga sewa per hari: ")
            )
        elif pilihan == '6':
            mobil_id_to_delete = input("\nMasukkan ID mobil yang ingin dihapus: ")
            sistem_rental.hapus_mobil(mobil_id_to_delete)
        elif pilihan == '7':
            sistem_rental.hapus_riwayat_transaksi()
        elif pilihan == '8':
            konfirmasi = input("\n\nApakah Anda yakin ingin keluar dari program? (ya/tidak) : ").lower()
            if konfirmasi == 'ya':
                sistem_rental.save_data()
                print('=' * 60 + "\n" 
                      '''\nTerima kasih telah menggunakan aplikasi RIZAL TRANSLUXURY\n- STAY LUXURIOUS! -
                            \n''' + '=' * 60)
                break
            elif konfirmasi == 'tidak':
                print("\nKeluar program dibatalkan. Kembali ke menu utama.")
            else:
                print("\nInput tidak valid. Harap masukkan 'ya' atau 'tidak'.\n")
