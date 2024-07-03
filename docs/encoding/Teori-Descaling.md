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

Dikala Anda sudah mengecek native yang udah fix, aku sarankan menggunakan [DescaleTarget](https://muxtools.vodes.pw/vodesfunc/descale/#vodesfunc.descale.DescaleTarget) dari [vodesfunc](https://github.com/Vodes/vodesfunc).

Contoh:

```py
dict(width=1356, height=763, src_top = 0.3625, src_height = 762.7, src_width=1355.9, src_left=0.0625)
```

```py
from vstools import core
from vskernels import Hermite
from vodesfunc import Waifu2x_Doubler, DescaleTarget, set_output

src = core.bs.VideoSource(r"YourVideo.mkv")

descale = DescaleTarget(
    height=762.7,
    base_height=763,
    width=1355.9,
    base_width=1356,
    shift=(0.3625, 0.0625),
    kernel=Bilinear,
    upscaler=Waifu2x_Doubler(),
    downscaler=Hermite(linear=True),
)
rescale = descale.get_upscaled(src)

set_output(src)
set_output(rescale)
```

Sekian dari saya.

Reference by [N4O](https://blog.n4o.xyz/posts/descalingvideo).