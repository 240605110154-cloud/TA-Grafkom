# Gabungkan file karakter terpisah (piko.blend, rami.blend, ...) menjadi satu file.
# Dasar: piko.blend (ekspresi, animasi, lampu, alas mushaf tetap utuh).
# Jalankan: blender -b piko.blend --python gabung_karakter.py -- karakter_debu.blend
import bpy, math, os, sys
from mathutils import Vector

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
DIR = os.path.dirname(OUT)
sc = bpy.context.scene

# karakter tambahan: file, objek di file itu -> nama baru, posisi x, tinggi akhir
TAMBAHAN = [
    {"file": "rami.blend", "nama": "Rami", "x": 0.85, "tinggi": 1.6,
     "objek": {"world": "Rami_Ctrl", "geometry_0": "Rami_Badan"},
     "material": {"Material_0": "Mat_Rami_Tekstur"}},
]

# ---------- Piko geser ke kiri ----------
bpy.data.objects["Piko_Master_Ctrl"].location.x = -0.9

# ---------- karakter tambahan ----------
for k in TAMBAHAN:
    with bpy.data.libraries.load(os.path.join(DIR, k["file"]), link=False) as (src, dst):
        dst.objects = list(k["objek"])
    col = bpy.data.collections.new(f"{k['nama']}_Utama")
    sc.collection.children.link(col)
    for lama, baru in k["objek"].items():
        o = next(o for o in dst.objects if o.name.startswith(lama))
        o.name = baru
        col.objects.link(o)
    for lama, baru in k["material"].items():
        bpy.data.materials[lama].name = baru
    ctrl = bpy.data.objects[f"{k['nama']}_Ctrl"]
    badan = bpy.data.objects[f"{k['nama']}_Badan"]
    zs = [(badan.matrix_world @ Vector(c)).z for c in badan.bound_box]
    s = k["tinggi"] / (max(zs) - min(zs))
    ctrl.scale = (s, s, s)
    ctrl.location = (k["x"], 0, -min(zs) * s)        # alas badan tepat di atas sampul mushaf

# ---------- kamera membingkai semua karakter ----------
cam = bpy.data.objects["Kamera_Piko"]
cam.name = cam.data.name = "Kamera_Karakter"
cam.location = (0.0, -7.6, 1.7)
cam.rotation_euler = (Vector((0, 0, 0.8)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.camera = cam

bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SELESAI", OUT)
