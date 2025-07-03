# main_game.py
import pygame
import sys

# Impor kelas dan konstanta dari file lain
from config import (
    LEBAR_LAYAR, TINGGI_LAYAR, UKURAN_KOTAK, PUTIH, FONT, HIJAU_MUDA, HIJAU_TUA,
    FPS_AWAL_GAME, SKOR_PER_PENINGKATAN_FPS, PENINGKATAN_FPS, FPS_MAKSIMAL_GAME 
)
from ular import Ular
from makanan import Makanan

# --- Inisialisasi Pygame ---
pygame.init()

# --- Pengaturan Jendela Game ---
LAYAR = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
pygame.display.set_caption("Game Snake Classic")

# --- Fungsi untuk Menggambar Background Berpola Dua Warna ---
def gambar_background_pola(layar_game):
    """Menggambar background game dengan pola kotak-kotak dua warna."""
    jumlah_kotak_x = LEBAR_LAYAR // UKURAN_KOTAK
    jumlah_kotak_y = TINGGI_LAYAR // UKURAN_KOTAK

    for x in range(jumlah_kotak_x):
        for y in range(jumlah_kotak_y):
            if (x + y) % 2 == 0:
                warna = HIJAU_MUDA
            else:
                warna = HIJAU_TUA
            
            pygame.draw.rect(layar_game, warna, (x * UKURAN_KOTAK, y * UKURAN_KOTAK, UKURAN_KOTAK, UKURAN_KOTAK))

# --- Fungsi Layar Game Over ---
def game_over_layar(skor_akhir):
    """Menampilkan layar 'GAME OVER' dengan skor akhir dan opsi untuk restart/keluar."""
    layar_game_over_aktif = True
    # Buat clock lokal untuk layar game over agar responsif tapi tidak membebani CPU
    clock_go = pygame.time.Clock()
    FPS_GO = 30 # FPS untuk layar Game Over

    while layar_game_over_aktif:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game() # Panggil ulang fungsi main_game untuk restart
                    return # Penting: Keluar dari loop game over setelah restart dipicu
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        gambar_background_pola(LAYAR) 

        pesan_go = FONT.render("GAME OVER!", True, PUTIH)
        pesan_skor = FONT.render(f"Skor Anda: {skor_akhir}", True, PUTIH)
        pesan_restart = FONT.render("Tekan 'R' untuk Restart, 'Q' untuk Keluar", True, PUTIH)

        LAYAR.blit(pesan_go, (LEBAR_LAYAR // 2 - pesan_go.get_width() // 2, TINGGI_LAYAR // 2 - 50))
        LAYAR.blit(pesan_skor, (LEBAR_LAYAR // 2 - pesan_skor.get_width() // 2, TINGGI_LAYAR // 2))
        LAYAR.blit(pesan_restart, (LEBAR_LAYAR // 2 - pesan_restart.get_width() // 2, TINGGI_LAYAR // 2 + 50))
        
        pygame.display.flip()
        clock_go.tick(FPS_GO) # Kontrol FPS untuk layar Game Over

# --- Fungsi Utama Game ---
def main_game():
    """Fungsi utama yang menjalankan seluruh logika dan rendering permainan Snake."""
    ular = Ular()
    makanan = Makanan()
    
    # Inisialisasi FPS game berdasarkan konstanta dari config (BARU)
    FPS_saat_ini = FPS_AWAL_GAME 
    clock = pygame.time.Clock() # Objek Clock untuk mengontrol FPS

    # Variabel untuk melacak target skor peningkatan kecepatan (BARU)
    skor_untuk_peningkatan_fps = SKOR_PER_PENINGKATAN_FPS

    game_berjalan = True
    while game_berjalan:
        # --- Penanganan Event (Input Pemain) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_berjalan = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and ular.arah != "BAWAH":
                    ular.arah = "ATAS"
                elif event.key == pygame.K_DOWN and ular.arah != "ATAS":
                    ular.arah = "BAWAH"
                elif event.key == pygame.K_LEFT and ular.arah != "KANAN":
                    ular.arah = "KIRI"
                elif event.key == pygame.K_RIGHT and ular.arah != "KIRI":
                    ular.arah = "KANAN"

        # --- Logika Game Utama ---
        ular.gerak() # Gerakkan ular setiap frame

        # Deteksi tabrakan kepala ular dengan posisi makanan
        if ular.kepala == makanan.posisi:
            ular.skor += 10
            ular.tambah_badan()
            
            # --- Cek dan tingkatkan kecepatan game (FPS) (BARU) ---
            if ular.skor >= skor_untuk_peningkatan_fps:
                if FPS_saat_ini < FPS_MAKSIMAL_GAME:
                    FPS_saat_ini += PENINGKATAN_FPS
                    # Pastikan FPS tidak melebihi batas maksimal
                    if FPS_saat_ini > FPS_MAKSIMAL_GAME:
                        FPS_saat_ini = FPS_MAKSIMAL_GAME
                    print(f"Kecepatan game meningkat! FPS saat ini: {FPS_saat_ini}") # Debugging
                    skor_untuk_peningkatan_fps += SKOR_PER_PENINGKATAN_FPS # Atur target skor berikutnya

            # Hasilkan posisi makanan baru, pastikan tidak muncul di badan ular
            while True:
                makanan.posisi = makanan.buat_posisi_acak()
                if makanan.posisi not in ular.badan:
                    break

        # Deteksi game over (ular menabrak dinding atau badannya sendiri)
        if ular.cek_tabrakan():
            game_over_layar(ular.skor) # Panggil layar game over
            game_berjalan = False # Penting: Hentikan loop game utama setelah game over layar selesai
                                  # atau jika game_over_layar memanggil main_game() lagi

        # --- Proses Menggambar / Rendering ---
        gambar_background_pola(LAYAR)
        ular.gambar(LAYAR)
        makanan.gambar(LAYAR)

        # Tampilkan skor saat ini di sudut kiri atas layar
        teks_skor = FONT.render(f"Skor: {ular.skor}", True, PUTIH)
        LAYAR.blit(teks_skor, (10, 10))

        pygame.display.flip()

        # Atur kecepatan game (jumlah frame per detik)
        clock.tick(FPS_saat_ini) # Gunakan FPS_saat_ini yang dinamis

    # --- Keluar dari Game ---
    pygame.quit()
    sys.exit()

# --- Titik Masuk Utama Program ---
if __name__ == "__main__":
    main_game()
