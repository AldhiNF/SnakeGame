# ular.py

import pygame
import sys
# Impor konstanta yang dibutuhkan dari config.py
from config import LEBAR_LAYAR, TINGGI_LAYAR, UKURAN_KOTAK, JALUR_ASET

class Ular:
    def __init__(self):
        # Hitung posisi tengah grid yang merupakan kelipatan UKURAN_KOTAK
        # Ini akan memastikan kepala ular selalu dimulai tepat di sudut kotak grid.
        start_x = (LEBAR_LAYAR // 2 // UKURAN_KOTAK) * UKURAN_KOTAK
        start_y = (TINGGI_LAYAR // 2 // UKURAN_KOTAK) * UKURAN_KOTAK

        self.kepala = [start_x, start_y]
        
        # Badan ular, dimulai dengan 3 segmen ke kiri dari kepala
        self.badan = [[self.kepala[0], self.kepala[1]],
                      [self.kepala[0] - UKURAN_KOTAK, self.kepala[1]],
                      [self.kepala[0] - (2 * UKURAN_KOTAK), self.kepala[1]]]
        self.arah = "KANAN" 
        self.skor = 0       

        # --- MEMUAT SEMUA GAMBAR ULAR ---
        # ... (bagian ini tidak perlu diubah, tetap sama seperti kode terakhir yang saya berikan) ...

        self.gambar_kepala = {}
        self.gambar_badan_lurus = {}
        self.gambar_belokan = {}
        self.gambar_ekor = {}

        try:
            # Memuat dan menskala gambar kepala ular untuk setiap arah
            self.gambar_kepala["ATAS"] = self._load_and_scale_image(JALUR_ASET + "ular_kepala_atas.png")
            self.gambar_kepala["BAWAH"] = self._load_and_scale_image(JALUR_ASET + "ular_kepala_bawah.png")
            self.gambar_kepala["KIRI"] = self._load_and_scale_image(JALUR_ASET + "ular_kepala_kiri.png")
            self.gambar_kepala["KANAN"] = self._load_and_scale_image(JALUR_ASET + "ular_kepala_kanan.png")

            # Memuat dan menskala gambar badan ular untuk arah horizontal dan vertikal
            self.gambar_badan_lurus["VERTIKAL"] = self._load_and_scale_image(JALUR_ASET + "ular_badan_vertikal.png")
            self.gambar_badan_lurus["HORIZONTAL"] = self._load_and_scale_image(JALUR_ASET + "ular_badan_horizontal.png")

            # Belokan Ular
            self.gambar_belokan["ATAS_KANAN"] = self._load_and_scale_image(JALUR_ASET + "ular_belok_atas_kanan.png")
            self.gambar_belokan["KANAN_ATAS"] = self._load_and_scale_image(JALUR_ASET + "ular_belok_kanan_atas.png")
            
            self.gambar_belokan["ATAS_KIRI"] = self._load_and_scale_image(JALUR_ASET + "ular_belok_atas_kiri.png")
            self.gambar_belokan["KIRI_ATAS"] = self._load_and_scale_image(JALUR_ASET + "ular_belok_kiri_atas.png")

            self.gambar_belokan["BAWAH_KANAN"] = self._load_and_scale_image(JALUR_ASET + "ular_belok_bawah_kanan.png")
            self.gambar_belokan["KANAN_BAWAH"] = self._load_and_scale_image(JALUR_ASET + "ular_belok_kanan_bawah.png")

            self.gambar_belokan["BAWAH_KIRI"] = self._load_and_scale_image(JALUR_ASET + "ular_belok_bawah_kiri.png")
            self.gambar_belokan["KIRI_BAWAH"] = self._load_and_scale_image(JALUR_ASET + "ular_belok_kiri_bawah.png")

            # Memuat dan menskala gambar ekor ular untuk setiap arah
            self.gambar_ekor["ATAS"] = self._load_and_scale_image(JALUR_ASET + "ular_ekor_atas.png")
            self.gambar_ekor["BAWAH"] = self._load_and_scale_image(JALUR_ASET + "ular_ekor_bawah.png")
            self.gambar_ekor["KIRI"] = self._load_and_scale_image(JALUR_ASET + "ular_ekor_kiri.png")
            self.gambar_ekor["KANAN"] = self._load_and_scale_image(JALUR_ASET + "ular_ekor_kanan.png")

        except pygame.error as e:
            print(f"ERROR: Gagal memuat aset ular. Pesan: {e}")
            print(f"Pastikan folder '{JALUR_ASET}' ada dan semua file gambar (misalnya 'ular_kepala_atas.png')")
            print("ada di dalamnya dengan nama yang benar (perhatikan huruf besar/kecil dan ekstensi).")
            sys.exit() # Keluar dari program jika aset penting tidak ada

    def _load_and_scale_image(self, path):
        """Fungsi pembantu untuk memuat gambar dan mengubah ukurannya sesuai UKURAN_KOTAK."""
        image = pygame.image.load(path).convert_alpha() # convert_alpha() untuk dukungan transparansi PNG
        return pygame.transform.scale(image, (UKURAN_KOTAK, UKURAN_KOTAK))

    def gerak(self):
        """Menggerakkan kepala ular dan memperbarui posisi badan."""
        # Salin posisi kepala saat ini untuk dijadikan segmen baru di depan
        kepala_lama = list(self.kepala) 

        # Perbarui posisi kepala berdasarkan arah
        if self.arah == "ATAS":
            self.kepala[1] -= UKURAN_KOTAK
        elif self.arah == "BAWAH":
            self.kepala[1] += UKURAN_KOTAK
        elif self.arah == "KIRI":
            self.kepala[0] -= UKURAN_KOTAK
        elif self.arah == "KANAN":
            self.kepala[0] += UKURAN_KOTAK

        # Masukkan posisi kepala yang baru di awal daftar badan
        self.badan.insert(0, list(self.kepala))
        # Hapus segmen terakhir badan (jika ular tidak memanjang)
        self.badan.pop()

    def tambah_badan(self):
        """Memperpanjang badan ular setelah memakan makanan."""
        # Menambahkan kembali segmen yang "dihapus" saat bergerak, sehingga badan memanjang
        self.badan.append(list(self.badan[-1]))

    def gambar(self, layar):
            # Pastikan ada cukup segmen untuk menggambar ekor dan badan.
            # Jika ular hanya punya kepala, gambar kepala saja dan keluar.
            if len(self.badan) < 2:
                layar.blit(self.gambar_kepala[self.arah], (self.badan[0][0], self.badan[0][1]))
                return

            # --- Gambar Ekor Ular ---
            posisi_ekor = self.badan[-1]
            posisi_sebelum_ekor = self.badan[-2]
            
            arah_ekor = None # Inisialisasi arah_ekor dengan None

            # Kasus 1: Ular baru saja memakan buah, segmen terakhir dan sebelum terakhir memiliki posisi yang sama.
            # Ini berarti ekor baru saja diduplikasi dan belum bergerak.
            if posisi_ekor[0] == posisi_sebelum_ekor[0] and posisi_ekor[1] == posisi_sebelum_ekor[1]:
                # Kita perlu menentukan arah ekor berdasarkan segmen sebelumnya yang valid.
                # Ini memerlukan setidaknya 3 segmen badan untuk melihat 'belakang' lagi.
                # Contoh: [K, B1, B2, B2_dup]. Kita ingin arah dari B1 ke B2.
                if len(self.badan) >= 3:
                    # Ambil arah dari segmen ke-3 terakhir menuju segmen ke-2 terakhir
                    arah_ekor = self._get_segment_direction(self.badan[-3], self.badan[-2])
                else:
                    # Kasus sangat langka: ular tumbuh dari 1 segmen ke 2 segmen (K, B_dup)
                    # Dalam skenario ini, arah ekor adalah kebalikan dari arah kepala.
                    # (Catatan: Ular kita dimulai dengan 3 segmen, jadi path ini jarang tercapai kecuali ada modifikasi inisial.)
                    if self.arah == "ATAS": arah_ekor = "BAWAH"
                    elif self.arah == "BAWAH": arah_ekor = "ATAS"
                    elif self.arah == "KIRI": arah_ekor = "KANAN"
                    elif self.arah == "KANAN": arah_ekor = "KIRI"
            else:
                # Kasus 2: Kondisi normal di mana ekor bergerak, dan posisi sebelum ekor berbeda.
                arah_ekor = self._get_segment_direction(posisi_sebelum_ekor, posisi_ekor)

            # PASTIKAN arah_ekor VALID sebelum memanggil blit
            if arah_ekor in self.gambar_ekor: # Periksa apakah kunci ada di dictionary
                layar.blit(self.gambar_ekor[arah_ekor], posisi_ekor)
            # else:
                # Ini adalah fallback jika arah_ekor masih None atau tidak valid
                # Anda bisa menggambar kotak debug untuk melihat lokasi masalah
                # print(f"DEBUG: Masalah menggambar ekor. arah_ekor: {arah_ekor}. Posisi ekor: {posisi_ekor}. Badan Ular: {self.badan}")
                # pygame.draw.rect(layar, (255, 165, 0), (posisi_ekor[0], posisi_ekor[1], UKURAN_KOTAK, UKURAN_KOTAK)) # Kotak oranye untuk debug

            # --- Gambar Badan Ular (dari segmen kedua hingga sebelum ekor) ---
            # ... (bagian ini tidak berubah, tetap sama seperti kode terakhir yang saya berikan) ...
            for i in range(1, len(self.badan) - 1):
                segmen_saat_ini = self.badan[i]
                segmen_sebelumnya = self.badan[i-1]
                segmen_selanjutnya = self.badan[i+1]

                arah_ke_segmen_ini = self._get_segment_direction(segmen_sebelumnya, segmen_saat_ini)
                arah_dari_segmen_ini = self._get_segment_direction(segmen_saat_ini, segmen_selanjutnya)

                if arah_ke_segmen_ini == arah_dari_segmen_ini:
                    # ... (kode badan lurus) ...
                    if arah_ke_segmen_ini == "ATAS" or arah_ke_segmen_ini == "BAWAH":
                        layar.blit(self.gambar_badan_lurus["VERTIKAL"], segmen_saat_ini)
                    else:
                        layar.blit(self.gambar_badan_lurus["HORIZONTAL"], segmen_saat_ini)
                else:
                    # ... (kode belokan) ...
                    belokan_key = None
                    if (arah_ke_segmen_ini == "ATAS" and arah_dari_segmen_ini == "KANAN"): belokan_key = "ATAS_KANAN"
                    elif (arah_ke_segmen_ini == "ATAS" and arah_dari_segmen_ini == "KIRI"): belokan_key = "ATAS_KIRI"
                    elif (arah_ke_segmen_ini == "BAWAH" and arah_dari_segmen_ini == "KANAN"): belokan_key = "BAWAH_KANAN"
                    elif (arah_ke_segmen_ini == "BAWAH" and arah_dari_segmen_ini == "KIRI"): belokan_key = "BAWAH_KIRI"
                    elif (arah_ke_segmen_ini == "KANAN" and arah_dari_segmen_ini == "ATAS"): belokan_key = "KANAN_ATAS"
                    elif (arah_ke_segmen_ini == "KANAN" and arah_dari_segmen_ini == "BAWAH"): belokan_key = "KANAN_BAWAH"
                    elif (arah_ke_segmen_ini == "KIRI" and arah_dari_segmen_ini == "ATAS"): belokan_key = "KIRI_ATAS"
                    elif (arah_ke_segmen_ini == "KIRI" and arah_dari_segmen_ini == "BAWAH"): belokan_key = "KIRI_BAWAH"

                    if belokan_key and belokan_key in self.gambar_belokan:
                        layar.blit(self.gambar_belokan[belokan_key], segmen_saat_ini)
                    # else:
                    #     print(f"Peringatan: Aset belokan tidak ditemukan untuk arah masuk '{arah_ke_segmen_ini}' ke arah keluar '{arah_dari_segmen_ini}' di posisi {segmen_saat_ini}")

            # --- Gambar Kepala Ular ---
            layar.blit(self.gambar_kepala[self.arah], (self.badan[0][0], self.badan[0][1]))

    def _get_segment_direction(self, pos1, pos2):
        """Fungsi pembantu untuk menentukan arah relatif dari pos1 ke pos2."""
        if pos1[0] < pos2[0]:
            return "KANAN"
        elif pos1[0] > pos2[0]:
            return "KIRI"
        elif pos1[1] < pos2[1]:
            return "BAWAH"
        elif pos1[1] > pos2[1]:
            return "ATAS"
        return None # Seharusnya tidak pernah tercapai untuk gerakan valid

    def cek_tabrakan(self):
        """Mengecek apakah ular menabrak dinding atau badannya sendiri."""
        # Tabrakan dengan dinding
        if (self.kepala[0] < 0 or self.kepala[0] >= LEBAR_LAYAR or
            self.kepala[1] < 0 or self.kepala[1] >= TINGGI_LAYAR):
            return True
        # Tabrakan dengan badan sendiri (mulai dari segmen kedua, hindari kepala itu sendiri)
        for segmen in self.badan[1:]:
            if self.kepala == segmen:
                return True
        return False