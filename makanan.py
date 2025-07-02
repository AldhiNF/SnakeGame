# makanan.py

import pygame
import random
import sys
# Impor konstanta yang dibutuhkan dari config.py
from config import LEBAR_LAYAR, TINGGI_LAYAR, UKURAN_KOTAK, JALUR_ASET

class Makanan:
    def __init__(self):
        self.posisi = self.buat_posisi_acak() # Posisi awal makanan
        
        # --- Muat dan skala gambar makanan ---
        try:
            self.gambar_makanan = pygame.image.load(JALUR_ASET + "makanan_apel.png").convert_alpha()
            self.gambar_makanan = pygame.transform.scale(self.gambar_makanan, (UKURAN_KOTAK, UKURAN_KOTAK))
        except pygame.error as e:
            # Tangani error jika gambar makanan tidak dapat dimuat
            print(f"ERROR: Gagal memuat aset makanan. Pesan: {e}")
            print(f"Pastikan file 'makanan_apel.png' ada di folder '{JALUR_ASET}' dan namanya benar.")
            sys.exit() # Keluar dari program jika aset penting tidak ada

    def buat_posisi_acak(self):
        """Membuat posisi acak baru untuk makanan di dalam grid layar."""
        # random.randrange(stop) menghasilkan angka dari 0 hingga stop-1
        # Mengalikan dengan UKURAN_KOTAK memastikan posisi sesuai grid
        x = random.randrange(0, LEBAR_LAYAR // UKURAN_KOTAK) * UKURAN_KOTAK
        y = random.randrange(0, TINGGI_LAYAR // UKURAN_KOTAK) * UKURAN_KOTAK
        return [x, y]

    def gambar(self, layar):
        """Menggambar objek makanan ke layar."""
        layar.blit(self.gambar_makanan, (self.posisi[0], self.posisi[1]))