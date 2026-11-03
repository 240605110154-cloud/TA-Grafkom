# Ganti Piko & Rami versi generator di file utama dengan model buatan teman (piko.blend, rami.blend).
# Model baru dipasang sebagai anak Empty karakter lama, jadi posisi, arah hadap, dan kamera panel tetap.
# Mesh lama dipindah ke collection "Cadangan_Tokoh_Lama" (disembunyikan, bisa dikembalikan).
# Jalankan: blender -b ../debu_di_atas_mushaf_lengkap.blend --python gabung_ke_utama.py -- debu_di_atas_mushaf_lengkap.blend
import bpy, os, sys
from mathutils import Vector

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.dirname(OUT)
sc = bpy.context.scene
vl = bpy.context.view_layer

cadangan = bpy.data.collections.new("Cadangan_Tokoh_Lama")
sc.collection.children.link(cadangan)

def tinggi_lama(root):
    zs = [(o.matrix_world @ Vector(c)).z for o in root.children_recursive if o.type == 'MESH' for c in o.bound_box]
    return max(zs) - min(zs)

def simpan_lama(root):
    for o in list(root.children_recursive):
        for c in list(o.users_collection):
            c.objects.unlink(o)
        cadangan.objects.link(o)

def layer_col(nama, lc=None):
    lc = lc or vl.layer_collection
    if lc.name == nama:
        return lc
    for ch in lc.children:
        r = layer_col(nama, ch)
        if r:
            return r

def pasang(ctrl, root, objs):
    """Skala ctrl agar setinggi tokoh lama, lalu taruh alasnya tepat di titik root (permukaan mushaf)."""
    tinggi = tinggi_lama(root)
    ctrl.parent = None
    ctrl.location = (0, 0, 0); ctrl.rotation_euler = (0, 0, 0); ctrl.scale = (1, 1, 1)
    bpy.context.view_layer.update()
    zs = [(o.matrix_world @ Vector(c)).z for o in objs for c in o.bound_box]
    s = tinggi / (max(zs) - min(zs))
    ctrl.parent = root
    ctrl.matrix_parent_inverse.identity()
    ctrl.scale = (s, s, s)
    ctrl.location = (0, 0, -min(zs) * s)
    return tinggi, s

# ---------------- Piko ----------------
piko_root = bpy.data.objects["Piko"]
with bpy.data.libraries.load(os.path.join(DIR, "piko.blend"), link=False) as (src, dst):
    dst.collections = ["Piko_Utama"]
piko_col = dst.collections[0]
bpy.data.collections["Piko"].children.link(piko_col)
simpan_lama(piko_root)
ctrl = bpy.data.objects["Piko_Master_Ctrl"]
for c in piko_col.children:                       # hanya ekspresi Normal yang tampil
    lc = layer_col(c.name)
    lc.hide_viewport = c.name != "Piko_1_Wajah_Normal"
    c.hide_render = c.name != "Piko_1_Wajah_Normal"
tampil = [o for o in piko_col.all_objects if o.type == 'MESH'
          and not any(n in o.name for n in ("_Senang_", "_Kaget_", "_Sedih_"))]
print("PIKO tinggi %.2f skala %.3f" % pasang(ctrl, piko_root, tampil))

# ---------------- Rami ----------------
rami_root = bpy.data.objects["Rami"]
with bpy.data.libraries.load(os.path.join(DIR, "rami.blend"), link=False) as (src, dst):
    dst.objects = ["world", "geometry_0"]
rami_col = bpy.data.collections.new("Rami_Utama")
bpy.data.collections["Rami"].children.link(rami_col)
rctrl, rbadan = dst.objects
rctrl.name, rbadan.name = "Rami_Ctrl", "Rami_Badan"
bpy.data.materials["Material_0"].name = "Mat_Rami_Tekstur"
for o in (rctrl, rbadan):
    rami_col.objects.link(o)
simpan_lama(rami_root)
print("RAMI tinggi %.2f skala %.3f" % pasang(rctrl, rami_root, [rbadan]))

layer_col("Cadangan_Tokoh_Lama").exclude = True
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SELESAI", OUT)
