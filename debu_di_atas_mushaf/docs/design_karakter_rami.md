# Desain Karakter & Panduan Pemodelan 3D: Rami (Si Pencatat Hari)

> **Proyek**: Animasi Pendek *"Debu di Atas Mushaf"*  
> **Karakter**: **Rami** (Si Pencatat Hari / *The Day Counter*)  
> **Aset Gambar**: `docs/assets/rami_model_sheet.jpg`

---

## 🎨 1. Lembar Desain & Input TRELLIS 3D

### A. Aset Siap Pakai untuk TRELLIS (Hugging Face)
* Berkas: `docs/assets/rami_trellis_input.jpg` (juga tersedia di `docs/assets/rami_trellis_input_ahoge.jpg`)
* Modifikasi: Memiliki **rambut *ahoge*** tunggal bervolume melengkung di puncak kepala yang siap dikonversi menjadi geometri 3D padat di TRELLIS.
* Karakteristik: Subjek tunggal terpusat, latar putih polos `#FFFFFF`, perspektif 3/4 depan dengan kedalaman volume tegas, murni tanpa tangan/kaki, tanpa teks/label.

### B. Lembar Turnaround Ortografis (Acuan Pemodelan Manual)
* Berkas: `docs/assets/rami_model_sheet.jpg` (Tampak Depan, Samping, Belakang, 3/4, dan Studi Ekspresi).

---

## 🔍 2. Analisis Adaptasi: Sketsa Storyboard vs Peningkatan 3D

Desain ini mempertahankan 100% DNA orisinal dari naskah UTS namun dioptimalkan untuk kebutuhan teknis animasi 3D:

| Komponen | Sketsa Storyboard Awal | Peningkatan 3D (*Stylized Production-Ready*) | Alasan Teknis Grafika Komputer |
| :--- | :--- | :--- | :--- |
| **Bentuk Tubuh (Siluet)** | Bentuk lonjong 2D cokelat datar | Bentuk gumpalan debu (*dust bunny*) lonjong organik dengan rumpun serat mikro (*fuzz tufts*) | Menghindari kesan bola kentang polos; siluet tampak lembut dan seperti partikel debu nyata saat disinari *rim light*. |
| **Kacamata** | Lingkaran kawat hitam sederhana | Kacamata kawat tipis melengkung (*wireframe spectacles*) melingkari mata dengan gagang ke samping | Mudah dimodelkan dengan kurva *Bézier* (Bevel Depth) di Blender, memberikan bayangan realistis pada wajah. |
| **Rambut / Serat Atas** | 1 helai garis lurus di kepala | 2 serat debu mikro lentur meliuk (*antennae-like dust fibers*) | Memberikan ruang untuk *secondary action* (goyangan lentur saat Rami bergerak atau menoleh). |
| **Mulut & Ekspresi** | Garis bergelombang (*wavy mouth*) | Sistem *Shape Keys* mulut bergelombang elastis | Memudahkan animasi transisi antara ekspresi cemas/grogi, kaget, senang, dan normal analitis. |
| **Pencatat Hari (Tally Marks)** | Goresan garis di sampul | Goresan langsung pada lapisan tekstur debu mushaf | Rami tidak memegang alat tangan; deretan goresan hitungan (hari ke-211) berada langsung di atas permukaan debu sampul mushaf di samping tubuhnya, dibuat menggunakan *texture bump/displacement* atau mesh garis tipis. |
| **Kaki & Tangan** | Tanpa anggota badan (mengambang / menempel langsung) | **Murni Tanpa Tangan & Kaki (*Limbless Blob*)** | Karakter adalah partikel debu murni tanpa anggota gerak fisik. Menghilangkan kompleksitas rigging ekstremitas; karakter berinteraksi dengan mengapung (*subtle hovering/bobbing*), bersandar, atau meluncur di permukaan debu. |

---

## 📐 3. Spesifikasi Teknis Pemodelan di Blender

### A. Geometri & Topologi Dasar
1. **Mesh Badan Utama**:
   - Mulai dari `UV Sphere` (16 rings × 16 segments) atau `Subdivided Cube` (Level 2).
   - Skalakan sumbu Z sekitar `1.2x` untuk menghasilkan bentuk lonjong khas Rami.
   - Gunakan *Proportional Editing* untuk memberikan ketidaksimetrisan organik tipis.
   - **Target Polycount**: 800 – 1.800 tris (sangat ringan untuk rendering real-time EEVEE Next atau Cycles).

2. **Kacamata (*Spectacles*)**:
   - Dibuat menggunakan `Curve > Circle` + `Extrude / Bevel (Round 0.02m)`.
   - Konversikan ke mesh atau pertahankan sebagai kurva parametrik agar mudah diatur ketebalan bingkainya.
   - Jembatan kacamata melengkung tipis di antara kedua mata.

3. **Serat Debu Atas (*Antennae*)**:
   - 2 buah kurva `Path / Bezier Curve` dengan taper mengecil ke ujung.
   - Tambahkan *Hook Modifier* atau *Single Bone Rig* untuk *secondary motion* (goyangan inersia).

4. **Goresan Hitungan Hari (Tally Marks)**:
   - Dibuat bukan sebagai benda yang dipegang tangan, melainkan bidang *Decal / Alpha Plane* atau goresan garis di atas tekstur debu sampul mushaf tepat di sebelah Rami.
   - Efek goresan baru (garis ke-211) dapat dianimasikan dengan *Build Modifier* atau animasi *Alpha Masking*.

---

## 🎨 4. Palet Warna & Shader Material (Blender Principled BSDF)

| Bagian | Hex Code | Deskripsi Warna | Pengaturan Shader |
| :--- | :--- | :--- | :--- |
| **Badan Debu** | `#D4B896` / `#C7A882` | *Warm Dusty Tan / Oatmeal Brown* | Roughness 0.9, Subsurface 0.08, Sheen Weight 0.5 (efek beludru/bulu halus). |
| **Bintik Debu Mikro** | `#8C6D4F` / `#6B4F36` | *Darker Dust Flecks* | Tekstur prosedural `Voronoi Texture` (Scale 25, ColorRamp sempit) masuk ke Base Color. |
| **Bingkai Kacamata** | `#3D3028` | *Dark Wireframe Bronze* | Metallic 0.8, Roughness 0.3. |
| **Mata (Pupil & Lensa)** | `#1A1614` & `#FFFFFF` | Hitam Pekat & Pantulan Putih Kartun | Roughness 0.05, Specular IOR Level 0.7 (refleksi tajam gaya animasi Pixar). |
| **Mulut & Alis** | `#4A3525` | Cokelat Tua Hangat | Flat diffuse, digerakkan via Texture atau Curve Deform. |

---

## 🎭 5. Matriks 4 Ekspresi Wajah (Sesuai Naskah UTS)

1. **Analytical Neutral (0:17 - Saat Memulai Menghitung)**:
   - Mulut bergelombang datar kecil.
   - Mata fokus menatap goresan debu di depannya.
2. **Anxious / Worried (0:56 - Saat Pertanyaan Bayu Meresap)**:
   - Mulut bergelombang bergetar lebar (khas Rami yang overthinking).
   - Bagian dalam alis terangkat ke atas, pupil mengecil sedikit.
3. **Surprised (1:07 - Saat Terdengar Pintu Kamar Berderit)**:
   - Mulut membentuk huruf 'O' kecil lonjong.
   - Mata terbuka lebar di balik kacamata.
## 🌐 7. Panduan Alur Kerja ke TRELLIS (Image-to-3D)

1. Buka [TRELLIS Hugging Face Space](https://huggingface.co/spaces/trellis-community/TRELLIS).
2. Unggah berkas `docs/assets/rami_trellis_input.jpg`.
3. Parameter yang direkomendasikan:
   - **Preprocess**: Aktifkan *Remove Background* (meskipun latar belakang sudah putih murni `#FFFFFF`).
   - **Sparse Structure (SS) Steps**: 12 (atau 25 untuk detail ekstra).
   - **Structured Latent (SLat) Steps**: 12.
4. Klik **Generate**.
5. Pada panel pratinjau 3D (Textured Mesh), unduh model dengan format **`.GLB`** atau **`.OBJ`**.
6. Buka Blender, pilih `File > Import > glTF 2.0 (.glb/.gltf)` untuk memasukkan model Rami ke dalam proyek animasi.
