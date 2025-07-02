# config.py

import pygame

# Inisialisasi modul font Pygame (diperlukan untuk teks skor/game over)
pygame.font.init()

# --- Pengaturan Layar ---
LEBAR_LAYAR = 1200   # Lebar jendela game dalam piksel
TINGGI_LAYAR = 800  # Tinggi jendela game dalam piksel
UKURAN_KOTAK = 40   # Ukuran setiap "kotak" grid di game, sesuai ukuran aset 40x40

# --- Definisi Warna (RGB) ---
PUTIH = (255, 255, 255) # Warna putih untuk teks
HITAM = (0, 0, 0)       # Warna hitam, bisa untuk teks atau latar belakang debug

# Warna spesifik untuk background berpola
HIJAU_MUDA = (170, 215, 81) # Warna hijau muda untuk pola background
HIJAU_TUA = (162, 209, 73)   # Warna hijau tua untuk pola background

# --- Pengaturan Font ---
# Menggunakan font default Pygame dengan ukuran 36
FONT = pygame.font.Font(None, 36)

# --- Pengaturan Aset Gambar ---
# Jalur ke folder tempat semua gambar aset disimpan.
# Pastikan folder 'aset' berada di direktori yang sama dengan file .py ini.
JALUR_ASET = "C:/PURWADHIKA/GAMEPYTHON/SNAKE/aset/"

# Pengaturan Kecepatan Game (BARU - ini yang perlu Anda tambahkan/perbarui)
FPS_AWAL_GAME = 3 # Frames per second awal game (ular bergerak 3 kotak/detik)
SKOR_PER_PENINGKATAN_FPS = 50 # Setiap 50 skor, kecepatan game akan meningkat
PENINGKATAN_FPS = 2 # FPS akan bertambah 2 setiap kali meningkat
FPS_MAKSIMAL_GAME = 33 # Batas kecepatan game tertinggi (Ular tidak akan lebih cepat dari ini)