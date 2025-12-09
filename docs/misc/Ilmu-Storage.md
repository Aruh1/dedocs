# Storage: Perbedaan Kapasitas Desimal vs Biner

Seringkali kita membeli harddisk atau SSD dengan label **1 TB**, namun saat dipasang di komputer (terutama Windows), kapasitas yang terbaca hanya sekitar **931 GB**. Hal ini bukan karena harddisk rusak atau dikorupsi, melainkan karena perbedaan cara menghitung satuan penyimpanan antara produsen storage dan sistem operasi komputer.

## Perbedaan Basis Perhitungan

### 1. Produsen Storage (Base 10 / Desimal)
Produsen media penyimpanan menggunakan sistem bilangan **Desimal (Base 10)** untuk memudahkan pemasaran.
* 1 Kilobyte (KB) = 1,000 bytes ($10^3$)
* 1 Megabyte (MB) = 1,000,000 bytes ($10^6$)
* 1 Gigabyte (GB) = 1,000,000,000 bytes ($10^9$)
* 1 Terabyte (TB) = 1,000,000,000,000 bytes ($10^{12}$)

### 2. Komputer / Windows (Base 2 / Biner)
Komputer bekerja dengan sistem bilangan **Biner (Base 2)**. Satuan yang sebenarnya digunakan oleh komputer (dan standar IEC) adalah **Kibibyte (KiB), Mebibyte (MiB), Gibibyte (GiB), dan Tebibyte (TiB)**. Namun, Windows secara historis menampilkan satuan ini sebagai "KB", "MB", "GB", "TB" meskipun perhitungannya menggunakan biner.
* 1 Kibibyte (KiB) = 1,024 bytes ($2^{10}$)
* 1 Mebibyte (MiB) = 1,024 KiB = 1,048,576 bytes ($2^{20}$)
* 1 Gibibyte (GiB) = 1,024 MiB = 1,073,741,824 bytes ($2^{30}$)
* 1 Tebibyte (TiB) = 1,024 GiB = 1,099,511,627,776 bytes ($2^{40}$)

## Analisis Matematis Mendalam

Berikut adalah penjabaran matematis mengapa perbedaan kapasitas ini terjadi dan bagaimana menghitungnya secara presisi.

### 1. Rumus Umum Konversi

Untuk mengonversi kapasitas dari satuan Desimal (iklan) ke Biner (sistem operasi), kita dapat menggunakan rumus berikut:

$$ Kapasitas_{Biner} = Kapasitas_{Desimal} \times \left( \frac{1000}{1024} \right)^n $$

Dimana:
*   $n = 1$ untuk Kilo (KB $\to$ KiB)
*   $n = 2$ untuk Mega (MB $\to$ MiB)
*   $n = 3$ untuk Giga (GB $\to$ GiB)
*   $n = 4$ untuk Tera (TB $\to$ TiB)

**Contoh Perhitungan untuk 1 TB:**
$$ 1 \text{ TB} = 1 \times \left( \frac{1000}{1024} \right)^4 $$
$$ 1 \text{ TB} \approx 1 \times 0.9094947 $$
$$ 1 \text{ TB} \approx 0.909 \text{ TiB} $$

Karena 1 TiB = 1024 GiB, maka:
$$ 0.9094947 \text{ TiB} \times 1024 \approx 931.32 \text{ GiB} $$

### 2. Persentase "Kehilangan" Kapasitas

Semakin besar satuan penyimpanannya, semakin besar persentase perbedaan antara label desimal dan kapasitas biner yang terbaca. Ini disebut sebagai *phantom loss*.

Rumus persentase perbedaan:
$$ \% \text{ Loss} = \left( 1 - \left( \frac{1000}{1024} \right)^n \right) \times 100\% $$

| Satuan | Pangkat ($n$) | Rasio ($1000/1024$)^n | Persentase "Hilang" | Contoh (Label $\to$ Terbaca) |
| :--- | :---: | :--- | :--- | :--- |
| KB | 1 | 0.976 | 2.4% | 1 KB $\to$ 0.97 KiB |
| MB | 2 | 0.953 | 4.7% | 1 MB $\to$ 0.95 MiB |
| GB | 3 | 0.931 | 6.9% | 1 GB $\to$ 0.93 GiB |
| TB | 4 | 0.909 | 9.1% | 1 TB $\to$ 0.90 TiB (931 GiB) |
| PB | 5 | 0.888 | 11.2% | 1 PB $\to$ 0.88 PiB |

### 3. Overhead Filesystem & Partisi

Selain perbedaan konversi matematika di atas, kapasitas yang bisa digunakan (*usable space*) akan berkurang lagi karena faktor teknis sistem operasi:

1.  **Partition Table (GPT/MBR)**: Sebagian kecil ruang di awal dan akhir drive digunakan untuk menyimpan informasi partisi.
2.  **Filesystem Structures**:
    *   **NTFS (Windows)**: Menggunakan *Master File Table* (MFT) yang secara default mereservasi sekitar 12.5% dari ukuran partisi untuk metadata file, meskipun ruang ini bersifat dinamis (bisa dipakai data jika penuh).
    *   **ext4 (Linux)**: Menggunakan *inodes* yang memakan ruang statis.
3.  **Reserved Space**: Windows sering membuat partisi tersembunyi (seperti *System Reserved* atau *Recovery Partition*) berukuran 100MB - 500MB yang tidak terlihat di drive letter utama (C: / D:).

Jadi, jika Anda membeli SSD 1 TB:
*   Secara matematis terbaca: **931 GiB**
*   Dikurangi partisi recovery & overhead filesystem: Mungkin tersisa **~930 GiB** atau sedikit kurang yang benar-benar kosong (*free space*).

