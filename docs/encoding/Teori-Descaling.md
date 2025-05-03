# Cara Descale yang baik dan benar

Resizing Anime sama Descaling Anime menghasilkan hal yang berbeda, Descaling menggunakan algoritma lain agar Anime dapat dikembalikan ke resolusi asli (Native Resolution).

Ada beberapa macam kernel yang dipakai sama Web streaming, atau studio animasinya.

Kernel yang sering dipakai biasanya Bilinear untuk upscale Anime dari resolusi asli (tergantung kasus).

Untuk permulaan, buatlah file baru dan tambah kode seperti ini (Ekstensi file: .vpy).

```py
from vskernels import (
    BicubicSharp,
    Bilinear,
    Catrom,
    Lanczos,
)
from vstools import core, depth, get_y, set_output

# Load your clip here
src = core.lsmas.LWLibavSource(r"YourVideo.mkv")

clip = depth(get_y(src), 32)

set_output(src)
set_output(clip)

for kernel in [Bilinear, Catrom, BicubicSharp, Lanczos(3)]:
    desc = kernel.descale(clip, 1600, 900) # Your native resolution
    resc = kernel.scale(desc, clip.width, clip.height)
    err = core.std.Expr([clip, resc], "x y - abs 10 *")

    name = f"{kernel.__name__ if hasattr(kernel, '__name__') else kernel.__class__.__name__}"

    set_output(desc, f"{name} Descale")
    set_output(resc, f"{name} Rescale")
    set_output(err, f"{name} Diff")
```

Dan ngerun menggunakan [vs-preview](https://github.com/Jaded-Encoding-Thaumaturgy/vs-preview) dari [vs-jet](https://github.com/Jaded-Encoding-Thaumaturgy/vs-jet) `vspreview descale.vpy`

Contoh hasilnya seperti [ini](https://slow.pics/c/49QvOKoW).

Dikala Anda sudah mengecek native yang udah fix, aku sarankan menggunakan [RescaleBuilder](https://muxtools.vodes.pw/vodesfunc/rescale/#vodesfunc.rescale.RescaleBuilder) dari [vodesfunc](https://github.com/Vodes/vodesfunc).

Contoh:

```py
dict(width=1356, height=763, src_top = 0.3625, src_height = 762.7, src_width=1355.9, src_left=0.0625)
```

```py
from vodesfunc import RescaleBuilder
from vskernels import Bilinear, Hermite
from vsscale import ArtCNN
from vsmuxtools import src_file
from vstools import set_output

# Source
src = src_file(r"YourVideo.mkv")
src = src.init_cut()

native_res = dict(width=1355.9, height=762.7, base_width=1356, base_height=763, shift=(0.3625, 0.0625))
builder, rescaled = (
    RescaleBuilder(src)
    .descale(Bilinear(), **native_res)
    .double(ArtCNN.R8F64)
    .downscale(Hermite(linear=True))
    .final()
)

set_output(src)
set_output(builder.descaled, "Descale")
set_output(builder.rescaled, "Same Kernel Rescale")

set_output(rescaled, "Upscaled")
```

Analoginya seperti ini: kita telah mendapatkan native resolusi dari anime *Boku no Kokoro no Yabai Yatsu* sebagai contoh.

1. **Descale dengan Kernel Bilinear**  
   Native resolusi yang ditemukan adalah **1355.9x762.7p** dengan basis resolusi **1356x763p**. Ini berarti resolusi asli anime tersebut sedikit bergeser, dengan nilai `src_top=0.3625` dan `src_left=0.0625`. Pergeseran ini berasal dari proses produksi di studio.

2. **Double dengan ArtCNN**  
   Setelah mendapatkan native resolusi, kita melakukan *upscaling* menggunakan **ArtCNN**. ArtCNN adalah *Convolutional Neural Network* yang dirancang untuk meningkatkan resolusi gambar secara detail.

3. **Downscale dengan Kernel Hermite**  
   Setelah *upscaling*, kita menggunakan kernel **Hermite** dengan *Linear Light* untuk melakukan *downscaling* kembali ke resolusi sumber.  
   - **Linear Light** berarti proses resizing dilakukan dalam ruang cahaya linear. Gambar diubah ke ruang cahaya linear sebelum di-*resize*, lalu dikembalikan ke gamma setelahnya.  
   - Kernel Hermite (bicubic dengan `a=0, b=0`) digunakan karena sifatnya yang cocok untuk menjaga detail selama proses resizing.

Dengan langkah-langkah ini, kita dapat merekonstruksi resolusi asli anime dengan lebih baik, sekaligus memastikan hasil akhir tetap sesuai dengan sumbernya.

Sekian dari saya.

Reference by [N4O](https://blog.n4o.xyz/posts/descalingvideo).