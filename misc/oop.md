# OOP (Object-Oriented Programming)

OOP adalah paradigma pemrograman yang mengorganisir kode menjadi **object** — sebuah unit yang menggabungkan data (atribut) dan perilaku (method).

Tiga pilar utama OOP:

- **Encapsulation** — menyembunyikan data di dalam class
- **Polymorphism** — satu method, banyak bentuk
- **Inheritance** — pewarisan sifat antar class

---

## Encapsulation

### Apa itu Encapsulation?

Encapsulation adalah teknik menyembunyikan data (atribut) di dalam class dan hanya mengizinkan akses melalui method tertentu (getter/setter). Data bersifat `private` agar tidak bisa diubah sembarangan dari luar class.

### Kenapa perlu Encapsulation?

Agar data terlindungi dari perubahan yang tidak disengaja. Contoh: nilai NIM mahasiswa tidak boleh diubah sembarangan. Dengan encapsulation, perubahan hanya bisa dilakukan lewat method yang sudah divalidasi.

### Bagaimana cara menerapkannya?

Buat atribut dengan modifier `private`, lalu buat method `get` (untuk membaca) dan `set` (untuk menulis) yang bersifat `public`.

```python
class Mahasiswa:
    def __init__(self, nim, nama):
        self.__nim = nim    # private
        self.nama = nama

    def get_nim(self):      # getter
        return self.__nim
```

### Kapan menggunakan Encapsulation?

Selalu digunakan ketika membuat class. Terutama saat ada data sensitif seperti password, saldo rekening, atau data pribadi yang tidak boleh diakses langsung dari luar class.

---

## Polymorphism

### Apa itu Polymorphism?

Polymorphism artinya "banyak bentuk". Satu method dengan nama yang sama bisa berperilaku berbeda tergantung class yang menggunakannya. Ada dua jenis:

- **Overloading** — method sama, parameter berbeda
- **Overriding** — method parent diubah di class anak

### Kenapa perlu Polymorphism?

Agar kode lebih fleksibel dan mudah diperluas. Tidak perlu membuat method berbeda untuk setiap jenis object. Contoh: method `cetak()` bisa digunakan untuk mencetak KRS mahasiswa S1 maupun S2 dengan format berbeda.

### Bagaimana cara kerjanya?

Dengan **method overriding**: class anak mendefinisikan ulang method yang sudah ada di class induk.

```python
class Mahasiswa:
    def info(self):
        return f"[Mahasiswa] {self.nama}"

class MahasiswaS1(Mahasiswa):
    def info(self):             # override
        return f"[S1] {self.nama} | Skripsi: {self.skripsi}"
```

### Kapan menggunakan Polymorphism?

Saat ada beberapa class yang memiliki perilaku serupa tapi implementasinya berbeda. Contoh: `MahasiswaS1` dan `MahasiswaS2` sama-sama punya method `hitungIPK()` tapi rumus perhitungannya berbeda.

---

## Inheritance (Canggih)

### Apa itu Inheritance?

Inheritance (Pewarisan) adalah kemampuan class anak untuk mewarisi atribut dan method dari class induk. Class anak bisa menambah atau mengubah perilaku yang diwarisi tanpa harus menulis ulang dari awal.

### Kenapa perlu Inheritance?

Untuk menghindari duplikasi kode (prinsip DRY — *Don't Repeat Yourself*). Contoh: `MahasiswaS1` dan `MahasiswaS2` sama-sama punya NIM dan nama. Daripada menulis dua kali, cukup buat class `Mahasiswa` sebagai induk.

### Bagaimana cara menggunakannya?

Gunakan keyword `extends` (Java/PHP) atau cukup tulis nama class induk di dalam kurung (Python).

```python
class MahasiswaS1(Mahasiswa):   # mewarisi class Mahasiswa
    def __init__(self, nim, nama, prodi, skripsi):
        super().__init__(nim, nama, prodi)
        self.skripsi = skripsi
```

### Kapan menggunakan Inheritance?

Saat ada hubungan **"adalah sebuah"** (*is-a relationship*). Contoh: `MahasiswaS1` *adalah* `Mahasiswa` → cocok pakai inheritance. Hindari jika hanya ada hubungan "menggunakan" (*has-a*), karena itu lebih cocok menggunakan komposisi.

---

## Study Kasus: Sistem Informasi Akademik

Contoh nyata penerapan OOP pada sistem akademik sederhana dengan tiga class utama.

### Diagram Class

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│      Mahasiswa      │     │     Matakuliah      │     │   RencanaStudi      │
├─────────────────────┤     ├─────────────────────┤     │      (KRS)          │
│ - nim: string       │     │ - kode: string      │     ├─────────────────────┤
│ - nama: string      │     │ - nama: string      │     │ - nim: string       │
│ - prodi: string     │     │ - sks: int          │     │ - semester: int     │
├─────────────────────┤     │ - semester: int     │     │ - kode_mk: string   │
│ + simpan()          │     ├─────────────────────┤     ├─────────────────────┤
│ + update()          │     │ + simpan()          │     │ + daftar()          │
│ + hapus()           │     │ + update()          │     │ + batalkan()        │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

**Relasi antar class:**

- Satu `Mahasiswa` bisa memiliki banyak `RencanaStudi` (KRS) → relasi 1 ke banyak
- Satu `RencanaStudi` berisi banyak `Matakuliah` → relasi banyak ke banyak
- `Mahasiswa` bisa diwariskan ke `MahasiswaS1` atau `MahasiswaS2` → Inheritance

### Implementasi Lengkap (Python)

```python
# ── Class Induk ────────────────────────────────────────────
class Mahasiswa:
    def __init__(self, nim, nama, prodi):
        self.__nim = nim        # private (encapsulation)
        self.nama = nama
        self.prodi = prodi

    def get_nim(self):          # getter
        return self.__nim

    def simpan(self):
        print(f"Mahasiswa {self.nama} disimpan")

    def update(self, nama_baru):
        self.nama = nama_baru
        print(f"Data diperbarui: {self.nama}")

    def hapus(self):
        print(f"Data {self.nama} dihapus")

    def info(self):             # untuk polymorphism
        return f"[Mahasiswa] {self.nama}"


# ── Inheritance: MahasiswaS1 mewarisi Mahasiswa ────────────
class MahasiswaS1(Mahasiswa):
    def __init__(self, nim, nama, prodi, skripsi):
        super().__init__(nim, nama, prodi)
        self.skripsi = skripsi

    def info(self):             # polymorphism (override)
        return f"[S1] {self.nama} | Skripsi: {self.skripsi}"


# ── Class Matakuliah ───────────────────────────────────────
class Matakuliah:
    def __init__(self, kode, nama, sks, semester):
        self.kode = kode
        self.nama = nama
        self.sks = sks
        self.semester = semester

    def simpan(self):
        print(f"Matakuliah {self.nama} ({self.sks} SKS) disimpan")


# ── Class RencanaStudi (KRS) ───────────────────────────────
class RencanaStudi:
    def __init__(self, nim, semester):
        self.nim = nim
        self.semester = semester
        self.daftar_mk = []

    def daftar(self, matakuliah):
        self.daftar_mk.append(matakuliah)
        print(f"Daftar: {matakuliah.nama} ({matakuliah.sks} SKS)")

    def batalkan(self, kode_mk):
        self.daftar_mk = [mk for mk in self.daftar_mk
                          if mk.kode != kode_mk]
        print(f"Matakuliah {kode_mk} dibatalkan")

    def total_sks(self):
        return sum(mk.sks for mk in self.daftar_mk)


# ── Contoh penggunaan ──────────────────────────────────────
mhs = MahasiswaS1("2021001", "Budi Santoso", "Informatika", "AI")
mhs.simpan()

mk1 = Matakuliah("IF301", "Basis Data", 3, 5)
mk2 = Matakuliah("IF302", "OOP", 3, 5)
mk3 = Matakuliah("IF303", "Jaringan Komputer", 2, 5)

krs = RencanaStudi(mhs.get_nim(), 5)
krs.daftar(mk1)
krs.daftar(mk2)
krs.daftar(mk3)

print(f"Total SKS: {krs.total_sks()}")

# Polymorphism — method info() berperilaku berbeda
print(mhs.info())   # output: [S1] Budi Santoso | Skripsi: AI
```

### Skenario Penggunaan

**Skenario 1 — Mahasiswa baru mendaftar KRS:**

1. Object `Mahasiswa` dibuat dengan nim, nama, prodi
2. Method `simpan()` dipanggil → data tersimpan ke database
3. Object `RencanaStudi` dibuat dengan nim mahasiswa tersebut
4. Method `daftar()` dipanggil untuk setiap matakuliah yang dipilih
5. KRS berhasil terbuat

**Skenario 2 — Perubahan data mahasiswa:**

1. Cari object `Mahasiswa` berdasarkan nim
2. Ubah atribut yang diinginkan (misal: nama)
3. Panggil method `update()` → data diperbarui di database

!!!info Encapsulation berperan di sini
NIM tidak boleh diubah karena bersifat `private`. Hanya atribut seperti `nama` dan `prodi` yang bisa diperbarui melalui method `update()`.
!!!

---

*Materi ini dibuat berdasarkan catatan kuliah OOP.*
