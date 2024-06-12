# Panduan Menggunakan Adblock untuk Mendownload Anime: Userscript, DNS, dan VPN

Mendownload anime dari situs tertentu sering kali dihadapkan dengan tantangan berupa iklan yang berlebihan dan mengganggu. Iklan-iklan ini tidak hanya memperlambat proses browsing tetapi juga bisa berisiko karena beberapa mungkin mengarahkan ke situs berbahaya. Dalam panduan ini, kita akan membahas cara-cara efektif untuk memblokir iklan tersebut menggunakan Userscript, DNS, dan VPN, dengan layanan seperti AdGuard dan Cloudflare 1.1.1.1 untuk pengalaman yang lebih aman dan nyaman.

## Langkah-langkah Menggunakan Userscript:
1. Kalian bisa install Tampermonkey atau Greasemonkey, ekstensi yang mendukung penggunaan Userscript.
2. Cari userscript yang cocok buat kalian, tapi aku menggunakan [Bypass All Shortlinks](https://greasyfork.org/en/scripts/431691-bypass-all-shortlinks) dari [bloggerpemula](https://greasyfork.org/en/users/810571-bloggerpemula) dan menginstallnya.

### Kelebihan:
- **Spesifik untuk Situs**: Banyak Userscript yang dirancang khusus untuk situs tertentu sehingga lebih efektif.
- **Kustomisasi Tinggi**: Anda dapat menyesuaikan skrip sesuai kebutuhan.

### Kekurangan:
- **Memerlukan Pengetahuan Teknis**: Menyesuaikan skrip bisa membutuhkan pemahaman teknis.
- **Hanya Berlaku di Browser**: Skrip ini hanya memblokir iklan pada halaman web di browser yang mendukungnya.

## Memblokir Iklan dengan DNS
Di sini ada metode dua cara dengan menggunakan Adguard atau Cloudflare Family.

1. Konfigurasi AdGuard DNS:
   - AdGuard DNS memblokir iklan dan pelacak secara otomatis.
   - Konfigurasikan perangkat atau router Anda. Aku saranin setting di router kalian.
    - Panduan lengkap pengaturan dapat ditemukan di [AdGuard DNS Setup](https://adguard-dns.io/en/public-dns.html).
2. Cloudflare 1.1.1.1 dengan Opsi Filter:
   - Cloudflare 1.1.1.1 menawarkan pengaturan DNS yang cepat dan dapat ditingkatkan dengan menggunakan [1.1.1.1 Family](https://one.one.one.one/family/).
3. Menambahkan Daftar Blokir Kustom:
   - Anda dapat menambahkan daftar blokir domain yang sering digunakan oleh situs iklan di pengaturan DNS atau router Anda.
   - Contoh daftar blokir: [StevenBlack/hosts](https://github.com/StevenBlack/hosts).

### Kelebihan:
- **Mudah diatur**: Pengaturan DNS mudah dan cepat.
- **Efektif di Semua Perangkat**: Berlaku untuk semua perangkat yang menggunakan jaringan yang sama.

### Kekurangan:
- **Pemblokiran Global**: Memblokir berdasarkan domain, tidak bisa menargetkan iklan spesifik di halaman tertentu.
- **Tidak Fleksibel**: Kurang cocok untuk pengguna yang membutuhkan kontrol granular atas pemblokiran iklan.

## Memblokir Iklan dengan VPN
VPN dapat memberikan lapisan keamanan tambahan dan memblokir iklan di tingkat jaringan.

### Menggunakan VPN untuk Memblokir Iklan:
VPN dapat memberikan lapisan keamanan tambahan dan memblokir iklan di tingkat jaringan.

Saya sarankan menggunakan [Adguard](https://adguard-dns.io.).

### Kelebihan:
- **Keamanan dan Privasi Tambahan**: VPN mengenkripsi lalu lintas Anda dan melindungi dari pelacakan.
- **Pemblokiran di Semua Aplikasi**: Memblokir iklan di semua aplikasi dan perangkat yang terhubung melalui VPN.

### Kekurangan:
- **Biaya Berlangganan**: VPN berkualitas biasanya memerlukan langganan berbayar.
- **Kecepatan**: Penggunaan VPN dapat mengurangi kecepatan internet tergantung pada server dan lokasi.

## Kesimpulan:
Memblokir iklan saat mendownload anime dapat dilakukan melalui Userscript, DNS, dan VPN. Masing-masing metode menawarkan kelebihan dan kekurangan yang unik. Userscript memberikan kontrol spesifik pada halaman web, sementara DNS dan VPN menawarkan solusi yang lebih global dan komprehensif. Dengan menggunakan layanan seperti AdGuard dan Cloudflare 1.1.1.1, Anda dapat menikmati pengalaman mendownload anime yang lebih aman dan bebas dari gangguan iklan.

## Referensi
- [Cloudflare 1.1.1.1](https://one.one.one.one/)
- [Tampermonkey](https://www.tampermonkey.net/)
- [GreasyFork](https://greasyfork.org)
- [StevenBlack/hosts](https://github.com/StevenBlack/hosts)
- [ChatGPT 4-o](https://chatgpt.com/)