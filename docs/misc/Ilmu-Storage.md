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

## Cara Perhitungannya

Mari kita hitung mengapa **1 TB** (Desimal) menjadi **931 GB** (Biner/GiB di Windows).

1.  **Ambil jumlah bytes dalam 1 TB Desimal:**
    $$1 \text{ TB} = 1,000,000,000,000 \text{ bytes}$$

2.  **Bagi dengan nilai 1 GB Biner (1 GiB):**
    $$1 \text{ GiB} = 1,073,741,824 \text{ bytes}$$

3.  **Lakukan pembagian:**
    $$\frac{1,000,000,000,000}{1,073,741,824} \approx 931.322$$

Jadi, **1 TB (Desimal) $\approx$ 931 GiB (Biner)**.

Karena Windows menampilkan GiB sebagai "GB", maka yang Anda lihat di properti drive adalah **931 GB**.

### Tabel Konversi Umum

| Label Produsen (Desimal) | Terbaca di Windows (Biner) |
| :--- | :--- |
| 500 GB | ~465 GB |
| 1 TB | ~931 GB |
| 2 TB | ~1.81 TB (1862 GB) |
| 4 TB | ~3.63 TB |
