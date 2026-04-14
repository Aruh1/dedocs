# OOP dalam Encoding Anime: Studi Kasus `vsscale` dari vs-jetpack

Object-Oriented Programming (OOP) sering terasa abstrak saat dipelajari lewat contoh "hewan" atau "kendaraan". Artikel ini mencoba menjawab tiga pilar OOP — **Enkapsulasi**, **Polimorfisme**, dan **Pewarisan** — dengan studi kasus yang lebih nyata: library [`vsscale`](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsscale/) dari [Jaded Encoding Thaumaturgy (JET)](https://github.com/Jaded-Encoding-Thaumaturgy), yang dipakai dalam pipeline rescaling video anime menggunakan VapourSynth.

!!!
Artikel ini menggunakan API `vsscale` versi terbaru dari `vs-jetpack`. Pastikan kamu sudah menginstall dengan `pip install vsjetpack`.
!!!

---

## Pertanyaan yang Akan Kita Jawab

Sebelum masuk ke materi, berikut pertanyaan-pertanyaan yang akan dijawab:

**Enkapsulasi**
1. Apa itu enkapsulasi, dan bagaimana class `Rescale` menerapkannya?
2. Kenapa atribut seperti `_kernel`, `_upscaler`, dan `_line_mask` dibuat privat (underscore)?
3. Bagaimana cara mengakses state internal `Rescale` dengan aman dari luar?

**Polimorfisme**
4. Apa itu polimorfisme, dan kenapa parameter `upscaler` di `Rescale` bisa menerima scaler apapun?
5. Bagaimana `Rescale` mendukung penggantian upscaler (dari `ArtCNN` ke `Hermite`, dll.) tanpa mengubah kode utama?
6. Apa keuntungan nyata polimorfisme dalam pipeline encoding yang kompleks?

**Pewarisan**
7. Apa itu pewarisan, dan bagaimana `Rescale` mewarisi dari `RescaleBase`?
8. Kenapa JET memisahkan `RescaleBase` dan `Rescale` menjadi dua class berbeda?
9. Kapan kamu perlu membuat subclass dari `Rescale` untuk kasus encoding yang spesifik?

---

## 1. Enkapsulasi

### Apa itu Enkapsulasi?

Enkapsulasi adalah prinsip OOP yang **membungkus data dan perilaku ke dalam satu unit class**, sekaligus **menyembunyikan detail implementasi** dari luar. Tujuannya agar pengguna class tidak perlu tahu *bagaimana* sesuatu bekerja di dalam — cukup tahu *apa* yang bisa dilakukan.

### Bagaimana `Rescale` Menerapkan Enkapsulasi?

Perhatikan konstruktor `Rescale`:

```python
Rescale(
    clip,
    height,
    kernel,
    upscaler=ArtCNN,
    downscaler=Hermite(linear=True),
    ...
)
```

Di balik layar, `Rescale.__init__` menyimpan semua state ke atribut **privat** (diawali underscore):

```python
# Dari source code vsscale/rescale.py — semua ini TERSEMBUNYI dari luar
self._line_mask   = None
self._credit_mask = None
self._ignore_mask = None
self._crop        = crop or CropRel()
self._pre         = clip
self._clipy       = ...   # luminance plane saja
self._kernel      = ComplexKernel.ensure_obj(kernel)
self._upscaler    = Scaler.ensure_obj(upscaler)
self._downscaler  = Scaler.ensure_obj(downscaler)
```

Pengguna tidak mengakses ini secara langsung. Mereka hanya berinteraksi lewat **properti publik**:

```python
rs = Rescale(clip, 720, Bilinear)

rs.descale      # → clip yang sudah di-descale
rs.doubled      # → clip yang di-upscale 2x oleh ArtCNN
rs.rescale      # → clip yang di-rescale balik dengan kernel yang sama
rs.upscale      # → hasil akhir yang siap dipakai
```

### Studi Kasus Enkapsulasi: Pipeline Rescaling Dasar

Dalam praktik encoding anime, kita sering hanya butuh tiga baris:

```python
from vsscale import Rescale
from vskernels import Bilinear
from vstools import core, set_output

src = core.lsmas.LWLibavSource(r"Anime_Episode01.mkv")

# Semua kompleksitas tersembunyi di dalam object rs
rs = Rescale(src, 720, Bilinear)

set_output(src,       "Source 1080p")
set_output(rs.descale, "Descaled 720p")
set_output(rs.upscale, "Upscaled kembali ke 1080p")
```

Kita tidak perlu tahu:
- Bagaimana `ScalingArgs` dihitung untuk fractional descale
- Bagaimana luma dan chroma dipisah lalu digabung kembali
- Bagaimana cache dikelola agar `.upscale` tidak dihitung ulang berkali-kali

Semuanya **terenkapulasi** dalam `Rescale`.

---

### Menjawab Pertanyaan Enkapsulasi

**Q1: Apa itu enkapsulasi dan bagaimana `Rescale` menerapkannya?**

> Enkapsulasi adalah mekanisme menyembunyikan state internal (data) dan hanya mengekspos antarmuka publik yang terkontrol. `Rescale` menerapkan ini dengan menyimpan semua atribut penting (`_kernel`, `_upscaler`, `_clipy`, dll.) sebagai privat, dan hanya mengekspos properti seperti `.upscale`, `.descale`, dan `.doubled` sebagai antarmuka publik.

**Q2: Kenapa atribut seperti `_kernel` dibuat privat?**

> Karena jika `_kernel` bisa diubah sembarangan dari luar, cache properti seperti `.descale` dan `.upscale` akan menjadi stale (tidak valid). Dengan membuatnya privat, `Rescale` bisa mengontrol kapan cache harus di-invalidate — ini dilakukan secara otomatis lewat `cachedproperty`.

**Q3: Bagaimana cara mengakses state internal `Rescale` dengan aman?**

> Lewat properti dan method publik. Untuk mengubah mask misalnya, gunakan:
> ```python
> rs.default_line_mask()        # generate dan assign line mask
> rs.default_credit_mask(thr=0.216)  # generate dan assign credit mask
> rs.line_mask = custom_mask    # atau assign langsung lewat setter
> ```

---

## 2. Polimorfisme

### Apa itu Polimorfisme?

Polimorfisme adalah kemampuan **satu antarmuka yang sama bekerja dengan banyak tipe objek berbeda**. Kamu memanggil method yang sama, tapi hasilnya berbeda tergantung objek mana yang dipakai.

### Bagaimana `Rescale` Mendukung Polimorfisme?

Parameter `upscaler` dan `downscaler` di `Rescale` bertipe `ScalerLike` — artinya bisa menerima objek apapun yang punya kemampuan scaling:

```python
Rescale(
    clip,
    height,
    kernel,
    upscaler: ScalerLike = ArtCNN,          # ← menerima scaler apapun
    downscaler: ScalerLike = Hermite(linear=True),  # ← menerima scaler apapun
)
```

Secara internal, `Rescale` memanggil:
```python
self._upscaler = Scaler.ensure_obj(upscaler)
```

`Scaler.ensure_obj()` mengubah input (baik string, class, maupun instance) menjadi object scaler yang valid. Setelah itu, `.scale()` dipanggil secara polimorfik — tidak peduli apakah itu `ArtCNN`, `Catrom`, atau `Waifu2x`.

### Studi Kasus Polimorfisme: Eksperimen Multi-Upscaler

Dalam workflow cek native resolution, kita sering ingin membandingkan hasil beberapa upscaler:

```python
from vsscale import Rescale
from vskernels import Bilinear, Hermite, Catrom
from vsscale import ArtCNN
from vstools import core, set_output

src = core.lsmas.LWLibavSource(r"Anime_Episode01.mkv")

# Daftar upscaler yang ingin dibandingkan
upscalers = [
    ("ArtCNN R8F64",  ArtCNN.R8F64),
    ("ArtCNN C4F16",  ArtCNN.C4F16),
    ("Catrom",        Catrom()),
    ("Hermite",       Hermite(linear=True)),
]

set_output(src, "Source")

for name, upscaler in upscalers:
    # Polimorfisme: Rescale tidak peduli upscaler mana yang dipakai
    # Interface-nya selalu sama: .upscale
    rs = Rescale(src, 720, Bilinear, upscaler=upscaler)
    set_output(rs.upscale, f"Upscale: {name}")
```

Tidak ada `if-elif` untuk masing-masing upscaler. `Rescale` cukup memanggil `.scale()` pada apapun yang di-pass sebagai `upscaler`.

### Studi Kasus Polimorfisme: Fungsi Pipeline Fleksibel

```python
from vsscale import Rescale
from vskernels import Bilinear, Lanczos, BicubicSharp

def cek_semua_kernel(clip, native_h, upscaler=ArtCNN.R8F64):
    """
    Fungsi ini polimorfik terhadap kernel descaling.
    Bisa menerima kernel apapun tanpa diubah.
    """
    kernels = [Bilinear(), Lanczos(taps=3), BicubicSharp()]
    results = []

    for kernel in kernels:
        rs = Rescale(clip, native_h, kernel, upscaler=upscaler)
        # Error map: semakin gelap semakin cocok kernelnya
        err = core.std.Expr(
            [rs.descale, kernel.scale(rs.descale, clip.width, clip.height)],
            "x y - abs 10 *"
        )
        results.append((kernel.__class__.__name__, rs.upscale, err))

    return results
```

---

### Menjawab Pertanyaan Polimorfisme

**Q4: Apa itu polimorfisme dan kenapa `upscaler` bisa menerima scaler apapun?**

> Polimorfisme memungkinkan satu parameter (`upscaler`) bekerja dengan banyak tipe objek (`ArtCNN`, `Hermite`, `Catrom`, dll.) selama semuanya punya method `.scale()`. `Rescale` tidak perlu tahu detail implementasi masing-masing scaler — cukup panggil `.scale()` dan Python menentukan sendiri implementasi yang dijalankan.

**Q5: Bagaimana `Rescale` mendukung penggantian upscaler tanpa mengubah kode?**

> Lewat parameter `upscaler` di constructor. Cukup pass objek scaler yang berbeda saat membuat instance `Rescale`. Kode internal `Rescale` tidak berubah sama sekali.

**Q6: Apa keuntungan nyata polimorfisme dalam encoding?**

> Bisa membuat satu fungsi pipeline yang bisa dipakai untuk semua kombinasi kernel dan upscaler. Menambah upscaler baru (misal Waifu2x generasi berikutnya) tidak perlu mengubah kode pipeline yang sudah ada.

---

## 3. Pewarisan (Inheritance)

### Apa itu Pewarisan?

Pewarisan adalah mekanisme dimana sebuah **class (child) mewarisi atribut dan method dari class lain (parent)**, sehingga tidak perlu menulis ulang kode yang sudah ada.

### Hierarki Class di `vsscale`

```
VSObjectABC         ← base abstrak paling atas
  └── RescaleBase   ← definisi interface & state dasar
        └── Rescale ← implementasi lengkap dengan masking & cropping
```

`RescaleBase` mendefinisikan semua state dan properti inti:

```python
class RescaleBase(VSObjectABC):
    def __init__(self, clip, kernel, upscaler=ArtCNN,
                 downscaler=Hermite(linear=True), ...):
        self._clipy, *chroma = split(clip)  # pisah luma & chroma
        self._kernel    = ComplexKernel.ensure_obj(kernel)
        self._upscaler  = Scaler.ensure_obj(upscaler)
        self._downscaler = Scaler.ensure_obj(downscaler)
        ...

    # Properti yang DIWARISI oleh Rescale:
    descale    # → clip yang di-descale
    doubled    # → clip yang di-upscale 2x
    rescale    # → clip yang di-rescale dengan kernel yang sama
    upscale    # → hasil akhir dengan chroma digabung kembali
```

`Rescale` mewarisi semuanya lalu **menambahkan** fitur masking dan fractional descaling:

```python
class Rescale(RescaleBase):
    def __init__(self, clip, height, kernel, upscaler=ArtCNN,
                 downscaler=Hermite(linear=True), width=None,
                 base_height=None, base_width=None,
                 crop=None, shift=(0, 0), ...):

        # Fitur TAMBAHAN dari Rescale (tidak ada di RescaleBase):
        self._line_mask   = None
        self._credit_mask = None
        self._ignore_mask = None
        self._crop        = crop or CropRel()

        # Hitung ScalingArgs untuk fractional descale
        self.descale_args = ScalingArgs.from_args(
            clip, height, width, base_height, base_width, ...
        )

        # Panggil parent constructor (RescaleBase)
        super().__init__(clip, kernel, upscaler, downscaler, ...)

    # Method TAMBAHAN yang hanya ada di Rescale:
    def default_line_mask(self, ...): ...
    def default_credit_mask(self, ...): ...
```

### Studi Kasus Pewarisan: Membuat Custom Rescale untuk Anime dengan Letterbox

Misal kita sering encode anime dengan letterbox di atas dan bawah. Kita bisa buat subclass yang sudah pre-configured:

```python
from vsscale import Rescale
from vskernels import Bilinear
from vstools import core, set_output

class RescaleLetterbox(Rescale):
    """
    Subclass Rescale yang otomatis menangani letterbox crop.
    Mewarisi SEMUA fitur Rescale (masking, fractional, dll.)
    dan hanya menambahkan default untuk crop & shift.
    """

    def __init__(self, clip, height, kernel,
                 letterbox_top=138, letterbox_bottom=138,
                 upscaler=ArtCNN, downscaler=Hermite(linear=True)):

        # Panggil parent (Rescale) dengan crop sudah di-set
        super().__init__(
            clip,
            height,
            kernel,
            upscaler=upscaler,
            downscaler=downscaler,
            crop=(0, 0, letterbox_top, letterbox_bottom),
        )


# Pemakaian — jauh lebih bersih
src = core.lsmas.LWLibavSource(r"Movie_Letterbox.mkv")

rs = RescaleLetterbox(src, 874, Bilinear)
rs.default_line_mask()
rs.default_credit_mask(thr=0.216)

set_output(rs.upscale, "Final Rescale")
```

`RescaleLetterbox` tidak menulis ulang logika masking, caching, atau fractional descaling — semuanya **diwarisi** dari `Rescale` dan `RescaleBase`.

### Studi Kasus Pewarisan: Pipeline Lengkap dengan AA dan Dehalo

```python
from vsscale import Rescale
from vskernels import Bilinear, Hermite
from vsscale import ArtCNN
from vsaa import based_aa
from vsdehalo import fine_dehalo
from vstools import core, depth, set_output

src = core.lsmas.LWLibavSource(r"Anime_Episode01.mkv")
src = depth(src, 32)

# 1. Buat Rescale object — Encapsulation & Inheritance bekerja di sini
rs = Rescale(
    src,
    height=720,           # native resolution
    kernel=Bilinear,      # kernel yang dipakai studio
    upscaler=ArtCNN.R8F64,           # upscaler AI
    downscaler=Hermite(linear=True), # downscale di linear light
)

# 2. Modifikasi doubled clip sebelum upscale — Encapsulation: setter properti
aa_clip     = based_aa(rs.doubled, supersampler=False)
dehalo_clip = fine_dehalo(aa_clip)
rs.doubled  = dehalo_clip  # assign kembali lewat setter — cache otomatis di-update

# 3. Load mask — Polymorphism: default_line_mask() bisa pakai scaler apapun
rs.default_line_mask()
rs.default_credit_mask(thr=0.216, ranges=[(1000, 2500), (5000, 6200)])

# 4. Output — semua kompleksitas tersembunyi di .upscale
set_output(src,        "Source")
set_output(rs.descale, "Descaled 720p")
set_output(rs.doubled, "Doubled + AA + Dehalo")
set_output(rs.upscale, "Final Upscale")
```

---

### Menjawab Pertanyaan Pewarisan

**Q7: Apa itu pewarisan dan bagaimana `Rescale` mewarisi dari `RescaleBase`?**

> Pewarisan adalah mekanisme dimana `Rescale` (child) secara otomatis mendapat semua atribut dan properti dari `RescaleBase` (parent) — termasuk `descale`, `doubled`, `rescale`, `upscale`, dan seluruh logika pengelolaan state. `Rescale` lalu menambahkan fitur masking dan fractional descaling di atasnya.

**Q8: Kenapa JET memisahkan `RescaleBase` dan `Rescale`?**

> Agar developer yang ingin membuat rescaler custom bisa inherit dari `RescaleBase` (lebih ringan, tanpa masking overhead) atau dari `Rescale` (dengan semua fitur). Ini adalah prinsip *Open/Closed* — terbuka untuk di-extend, tertutup untuk dimodifikasi.

**Q9: Kapan perlu membuat subclass dari `Rescale`?**

> Ketika ada konfigurasi yang selalu sama di setiap episode, seperti:
> - Anime dengan letterbox tetap → subclass dengan default `crop`
> - Anime dengan native shift tertentu → subclass dengan default `shift`
> - Studio dengan kernel khusus → subclass dengan kernel di-hardcode

---

## Rangkuman

| Pilar OOP | Implementasi di `vsscale` |
|---|---|
| **Enkapsulasi** | State privat (`_kernel`, `_upscaler`, `_clipy`, dll.) diakses lewat properti publik (`.upscale`, `.descale`, `.doubled`). Cache dikelola otomatis. |
| **Polimorfisme** | Parameter `upscaler` dan `downscaler` menerima `ScalerLike` apapun. Fungsi pipeline tidak perlu tahu jenis scaler yang dipakai. |
| **Pewarisan** | `Rescale` inherit dari `RescaleBase` yang inherit dari `VSObjectABC`. Setiap level menambahkan fitur tanpa menulis ulang yang sudah ada. |

!!!warning Catatan Versi
Artikel ini menggunakan `vsscale.rescale.Rescale` dari `vs-jetpack`. API ini menggantikan `RescaleBuilder` dari `vodesfunc` yang mungkin kamu temukan di tutorial lama.
!!!

---

## Referensi

- [vsscale API Docs — vs-jetpack](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsscale/rescale/)
- [vs-jetpack GitHub](https://github.com/Jaded-Encoding-Thaumaturgy/vs-jetpack)
- [Cara Descale yang Baik dan Benar — docs.pololer.my.id](https://docs.pololer.my.id/encoding/teori-descaling/)
- [JET Encoding Guide](https://github.com/Jaded-Encoding-Thaumaturgy/JET-guide)

[Edit this page](https://github.com/Aruh1/dedocs/edit/master/docs/misc/oop-vsscale.md)
