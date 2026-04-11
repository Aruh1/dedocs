# OOP — Studi Kasus: `vsscale` dari vs-jetpack

Dokumen ini membahas tiga pilar **Object-Oriented Programming (OOP)** menggunakan studi kasus nyata dari modul [`vsscale`](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsscale/) milik [Jaded Encoding Thaumaturgy (JET)](https://github.com/Jaded-Encoding-Thaumaturgy), sebuah library Python untuk rescaling video anime menggunakan VapourSynth.

!!!
Setiap pilar dijawab menggunakan kerangka **Apa → Kenapa → Bagaimana → Kapan** sesuai materi di kelas.
!!!

---

## 1. Encapsulation

### Apa itu Encapsulation?

**Encapsulation** adalah prinsip OOP yang membungkus data (atribut) dan perilaku (method) ke dalam satu unit class, sekaligus menyembunyikan detail implementasi dari luar.

Di `vsscale`, class seperti `ArtCNN` membungkus seluruh logika neural network ONNX — bobot model, preprocessing, inference — ke dalam satu objek. Pengguna tidak perlu tahu bagaimana model dijalankan di dalam; cukup panggil `.scale()`.

```python
from vsscale import ArtCNN
from vstools import core, depth, get_y, set_output

src = core.lsmas.LWLibavSource(r"Anime.mkv")
clip = depth(get_y(src), 32)

# Semua kompleksitas ONNX tersembunyi di dalam class
upscaled = ArtCNN.R8F64.scale(clip, clip.width * 2, clip.height * 2)

set_output(upscaled, "ArtCNN Upscale")
```

---

### Kenapa menggunakan Encapsulation?

Tanpa encapsulation, setiap kali kita ingin memakai `ArtCNN`, kita harus mengurus sendiri:

- Path model ONNX
- Backend inference (CUDA, CPU, TensorRT)
- Format input/output clip
- Preprocessing bit depth

Dengan encapsulation, semua itu tersembunyi. Pengguna cukup memilih varian model (`R8F64`, `C4F16`, `R16F96`, dll.) dan langsung gunakan. Ini juga memastikan tidak ada kesalahan konfigurasi yang tidak disengaja dari luar class.

---

### Bagaimana Encapsulation diimplementasikan di `vsscale`?

Class `ArtCNN` adalah sebuah `Enum`-like class yang setiap anggotanya adalah object dengan atribut dan method yang sudah terkapsulasi:

```python
# Contoh konseptual struktur internal ArtCNN (disederhanakan)
class ArtCNN:
    class R8F64:
        _model_path = "/path/to/ArtCNN_R8F64.onnx"  # tersembunyi
        _backend    = Backend.ORT_CUDA               # tersembunyi

        @classmethod
        def scale(cls, clip, width, height):
            # Detail inference ONNX tersembunyi di sini
            return _run_onnx(cls._model_path, clip, width, height)

    class C4F16:
        _model_path = "/path/to/ArtCNN_C4F16.onnx"  # tersembunyi
        _backend    = Backend.ORT_CPU                # tersembunyi

        @classmethod
        def scale(cls, clip, width, height): ...
```

Dari luar, pengguna hanya melihat antarmuka `ArtCNN.R8F64.scale(clip, w, h)` — bersih dan konsisten.

---

### Kapan Encapsulation diterapkan?

Encapsulation wajib diterapkan sejak awal ketika:

1. Implementasi internal kompleks dan bisa berubah (misal: ganti backend dari ORT ke TensorRT).
2. Ada parameter yang bisa menghasilkan output rusak jika diset sembarangan.
3. Class akan dipakai banyak orang — library publik seperti vs-jetpack selalu menerapkan ini.

---

## 2. Polymorphism

### Apa itu Polymorphism?

**Polymorphism** adalah kemampuan satu antarmuka (interface) yang sama untuk bekerja dengan banyak tipe objek yang berbeda. Di `vsscale` dan `vskernels`, semua scaler — baik neural network maupun kernel klasik — punya method `.scale()` yang sama, tapi hasilnya berbeda sesuai algoritma masing-masing.

```python
from vskernels import Bilinear, Catrom, Lanczos
from vsscale import ArtCNN
from vstools import core, depth, get_y, set_output

src = core.lsmas.LWLibavSource(r"Anime.mkv")
clip = depth(get_y(src), 32)

# Fungsi yang sama dipanggil pada semua scaler
scalers = [
    Bilinear(),
    Catrom(),
    Lanczos(taps=3),
    ArtCNN.R8F64,
]

for scaler in scalers:
    out = scaler.scale(clip, 1920, 1080)
    name = scaler.__class__.__name__
    set_output(out, f"{name} Scale")
```

Semua scaler diperlakukan seragam — `scaler.scale(clip, w, h)` — meskipun di balik layar algoritmanya sama sekali berbeda.

---

### Kenapa Polymorphism membuat kode lebih baik?

Bayangkan tanpa polymorphism:

```python
# Tanpa polymorphism — nightmare maintenance
if scaler_type == "bilinear":
    result = apply_bilinear(clip, 1920, 1080)
elif scaler_type == "catrom":
    result = apply_catrom(clip, 1920, 1080)
elif scaler_type == "lanczos":
    result = apply_lanczos(clip, taps, 1920, 1080)
elif scaler_type == "artcnn":
    result = apply_artcnn_onnx(model_path, backend, clip, 1920, 1080)
# ...dan seterusnya
```

Dengan polymorphism, menambah scaler baru tidak perlu mengubah satu baris pun di kode yang sudah ada. Cukup buat class baru yang implementasikan `.scale()`.

---

### Bagaimana Polymorphism diimplementasikan di `vsscale`?

Semua scaler di vs-jetpack mengikuti base protocol yang sama (abstract base class / duck typing):

```python
from vskernels import Bilinear, Hermite
from vsscale import ArtCNN

# Fungsi ini menerima scaler APAPUN secara polymorphic
def build_rescale_pipeline(clip, upscaler, downscaler, native_w, native_h):
    # Descale ke native resolution
    desc = Bilinear().descale(clip, native_w, native_h)

    # Upscale — bisa ArtCNN, Waifu2x, atau kernel biasa
    # Tidak perlu if-else, cukup panggil .scale()
    doubled = upscaler.scale(desc, native_w * 2, native_h * 2)

    # Downscale balik ke resolusi sumber
    final = downscaler.scale(doubled, clip.width, clip.height)
    return final

# Memanggil dengan berbagai kombinasi — polymorphism!
result_artcnn  = build_rescale_pipeline(clip, ArtCNN.R8F64, Hermite(linear=True), 960, 540)
result_catrom  = build_rescale_pipeline(clip, Catrom(),     Hermite(linear=True), 960, 540)
```

---

### Kapan Polymorphism digunakan?

Polymorphism paling berguna ketika:

1. Membuat fungsi pipeline yang harus bisa menerima berbagai jenis scaler tanpa perubahan kode.
2. Memberi pengguna kebebasan memilih algoritma (user-configurable pipeline).
3. Di vs-aa: parameter `downscaler` dan `supersampler` juga polymorphic — bisa kernel apapun selama punya method `.scale()`.

---

## 3. Inheritance (Canggih)

### Apa itu Inheritance?

**Inheritance** adalah mekanisme dimana sebuah class (subclass/child) mewarisi atribut dan method dari class lain (superclass/parent). Di vs-jetpack, ada hierarki class yang dibangun dengan inheritance:

```
Scaler (abstract base)
  └── Kernel
        ├── Bicubic
        │     ├── Catrom       (b=0, c=0.5)
        │     ├── BicubicSharp (b=0, c=1)
        │     └── Hermite      (b=0, c=0)
        ├── Bilinear
        ├── Lanczos
        └── Spline

  └── OnnxScaler (abstract, dari vsscale)
        ├── ArtCNN
        │     ├── ArtCNN.R8F64
        │     ├── ArtCNN.C4F16
        │     └── ArtCNN.R16F96
        └── Waifu2x
              ├── Waifu2x.Anime
              └── Waifu2x.AnimeJPEG
```

---

### Kenapa Inheritance dipakai di `vsscale`?

Semua scaler — baik kernel klasik maupun neural network — punya perilaku dasar yang sama: menerima clip, width, height, dan mengembalikan clip baru. Dengan inheritance:

1. **Tidak ada duplikasi kode** — validasi input, format conversion, dan utilities cukup ditulis satu kali di base class.
2. **Mudah diperluas** — membuat scaler baru hanya perlu override bagian yang berbeda.
3. **Konsistensi terjamin** — semua subclass dijamin punya interface yang sama karena mewarisi dari base yang sama.

```python
# Contoh: OnnxScaler sebagai base class (disederhanakan)
class OnnxScaler:
    """Base class untuk semua ONNX-based upscaler."""

    _model_path: str   # Diisi oleh subclass
    _scale: int = 2    # Default scale factor 2x

    def scale(self, clip, width, height):
        # Logika umum: validasi, load model, run inference
        # Ini diwarisi oleh ArtCNN, Waifu2x, dll.
        clip = self._preprocess(clip)
        out  = self._run_onnx(clip)
        return self._postprocess(out, width, height)

    def _preprocess(self, clip):  # method yang bisa di-override
        return clip

    def _run_onnx(self, clip):    # method yang bisa di-override
        raise NotImplementedError


# ArtCNN inherit dari OnnxScaler
class ArtCNN_R8F64(OnnxScaler):
    _model_path = "ArtCNN_R8F64.onnx"

    # Tidak perlu tulis ulang .scale() — diwarisi dari OnnxScaler
    # Cukup tentukan model path dan override jika perlu


# Waifu2x juga inherit dari OnnxScaler
class Waifu2x_Anime(OnnxScaler):
    _model_path = "waifu2x_anime.onnx"
    _scale = 2
```

---

### Bagaimana Inheritance diimplementasikan secara konkret?

Contoh nyata pipeline rescaling yang memanfaatkan hierarki inheritance vs-jetpack:

```python
from vskernels import Bilinear, Hermite
from vsscale import ArtCNN
from vstools import core, depth, get_y, set_output

src  = core.lsmas.LWLibavSource(r"Anime.mkv")
clip = depth(get_y(src), 32)

native_res = dict(width=1356, height=763)

# ArtCNN.R8F64 mewarisi kemampuan .scale() dari OnnxScaler
# Bilinear mewarisi .descale() dari Kernel base class
desc    = Bilinear().descale(clip, **native_res)
doubled = ArtCNN.R8F64.scale(desc, native_res["width"] * 2, native_res["height"] * 2)

# Hermite mewarisi .scale() dari Bicubic yang mewarisi dari Kernel
final   = Hermite(linear=True).scale(doubled, clip.width, clip.height)

set_output(src,   "Source")
set_output(desc,  "Descaled (Bilinear)")
set_output(final, "Rescaled (ArtCNN R8F64 + Hermite)")
```

Setiap class hanya bertanggung jawab pada bagian yang berbeda, sisanya diwarisi dari parent.

---

### Kapan menggunakan Inheritance vs membuat class dari nol?

| Kondisi | Pilihan |
|---|---|
| Class baru adalah "versi khusus" dari class yang ada | **Inheritance** |
| Class baru berbagi banyak logika dengan class lain | **Inheritance** |
| Class baru sama sekali berbeda dan tidak berbagi logika | **Class baru** |
| Ingin "meminjam" method tapi bukan hubungan is-a | **Composition** |

Contoh yang tepat: `Catrom` adalah Bicubic dengan `b=0, c=0.5` → pakai inheritance. Membuat scaler berbasis shader GLSL yang sama sekali berbeda dari ONNX → class baru yang inherit dari base abstrak yang lebih umum (`Scaler`).

---

## Referensi

- [vs-jetpack — JET GitHub](https://github.com/Jaded-Encoding-Thaumaturgy/vs-jetpack)
- [vsscale API Docs](https://jaded-encoding-thaumaturgy.github.io/vs-jetpack/api/vsscale/)
- [Cara Descale yang baik dan benar — docs.pololer.my.id](https://docs.pololer.my.id/encoding/teori-descaling/)
- [JET Encoding Guide](https://github.com/Jaded-Encoding-Thaumaturgy/JET-guide)
