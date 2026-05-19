#!/usr/bin/env python3
# Renders aad/keymap.json to aad-keymap-layout.svg (all layers, Corne split shape).
# Run from anywhere:  python3 gen_kbd_svg.py
import json, html, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "aad-keymap-layout.svg")

def load_layers():
    """Read layers from keymap.json if present, else parse keymap.c."""
    jp = os.path.join(HERE, "keymap.json")
    cp = os.path.join(HERE, "keymap.c")
    if os.path.exists(jp):
        raw = open(jp).read()
        raw = "\n".join(l for l in raw.splitlines()
                        if not l.lstrip().startswith("//"))
        return json.loads(raw)["layers"]
    src = open(cp).read()
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = "\n".join(line.split("//")[0] for line in src.splitlines())
    macro = "LAYOUT_corne_hlc("
    layers, i = [], 0
    while True:
        j = src.find(macro, i)
        if j < 0:
            break
        k = j + len(macro)
        depth, buf = 1, []
        while depth > 0:
            c = src[k]
            depth += (c == "(") - (c == ")")
            if depth > 0:
                buf.append(c)
            k += 1
        i = k
        toks, d, cur = [], 0, ""
        for c in "".join(buf):
            if c == "(":
                d += 1; cur += c
            elif c == ")":
                d -= 1; cur += c
            elif c == "," and d == 0:
                toks.append(cur.strip()); cur = ""
            else:
                cur += c
        if cur.strip():
            toks.append(cur.strip())
        layers.append(toks)
    return layers

layers = load_layers()

# Physical layout for LAYOUT_corne_hlc, in the SAME order the keymap.json arrays use.
# (x in key-units, y in key-units, width). Module row (last 10) omitted from the
# diagram - with HLC_NONE it is only encoder-mute / KC_NO.
# Per-column vertical stagger of the Corne.
col_stagger = {0:0.35,1:0.35,2:0.10,3:0.00,4:0.10,5:0.22,
               9:0.22,10:0.10,11:0.00,12:0.10,13:0.35,14:0.35}

pos = []  # list of (x, y, w) matching keymap index order, only the 42 std keys
# rows 0,1,2 : left x=0..5, right x=9..14
for row in range(3):
    for x in range(0,6):
        pos.append((x, row + col_stagger[x], 1.0))
    for x in range(9,15):
        pos.append((x, row + col_stagger[x], 1.0))
# thumb row (6): L21 x4, L20 x5, L19 x6 w1.5 | R19 x8 w1.5, R20 x9, R21 x10
pos += [(4,3.85,1.0),(5,3.85,1.0),(6,3.35,1.5),
        (8,3.35,1.5),(9,3.85,1.0),(10,3.85,1.0)]

NKEYS = len(pos)  # 42

# ---- keycode -> human label (main, sub) ----
SIMPLE = {
 "KC_NO":"", "XXXXXXX":"", "KC_TRNS":"▽", "_______":"▽",
 "KC_ESC":"Esc","KC_BSPC":"Bspc","KC_ENT":"Enter","KC_SPC":"Space","KC_TAB":"Tab",
 "KC_DEL":"Del","KC_HOME":"Home","KC_END":"End","KC_PGUP":"PgUp","KC_PGDN":"PgDn",
 "KC_CAPS":"Caps","KC_LSFT":"LShift","KC_RSFT":"RShift","KC_LCTL":"LCtrl",
 "KC_RCTL":"RCtrl","KC_LGUI":"LGUI","KC_RGUI":"RGUI","KC_LALT":"LAlt","KC_RALT":"RAlt",
 "KC_LEFT":"←","KC_RIGHT":"→","KC_UP":"↑","KC_DOWN":"↓",
 "KC_SCLN":";","KC_QUOT":"'","KC_COMM":",","KC_DOT":".","KC_SLSH":"/",
 "KC_EXLM":"!","KC_AT":"@","KC_HASH":"#","KC_DLR":"$","KC_PERC":"%","KC_CIRC":"^",
 "KC_AMPR":"&","KC_ASTR":"*","KC_BSLS":"\\","KC_GRV":"`","KC_TILD":"~","KC_UNDS":"_",
 "KC_PIPE":"|","KC_EQL":"=","KC_PLUS":"+","KC_MINS":"-","KC_LT":"<","KC_GT":">",
 "KC_LBRC":"[","KC_RBRC":"]","KC_LCBR":"{","KC_RCBR":"}","KC_LPRN":"(","KC_RPRN":")",
 "KC_WBAK":"WBack","KC_WFWD":"WFwd","QK_BOOT":"BOOT",
}
MODSHORT = {"MOD_LGUI":"GUI","MOD_RGUI":"GUI","MOD_LALT":"Alt","MOD_RALT":"AltGr",
            "MOD_LCTL":"Ctrl","MOD_RCTL":"Ctrl","MOD_LSFT":"Shift","MOD_RSFT":"Shift"}

def simple(k):
    if k in SIMPLE: return SIMPLE[k]
    if re.fullmatch(r"KC_F\d+", k): return k[3:]
    if re.fullmatch(r"KC_\d", k): return k[3:]
    if re.fullmatch(r"KC_[A-Z]", k): return k[3:]
    return k.replace("KC_","")

def label(k):
    """return (main, sub)"""
    k = k.strip()
    m = re.fullmatch(r"MT\(\s*(\w+)\s*,\s*(\w+)\s*\)", k)
    if m: return simple(m.group(2)), MODSHORT.get(m.group(1), m.group(1))
    m = re.fullmatch(r"LT\(\s*(\d+)\s*,\s*(\w+)\s*\)", k)
    if m: return simple(m.group(2)), "L"+m.group(1)
    m = re.fullmatch(r"MO\(\s*(\d+)\s*\)", k)
    if m: return "L"+m.group(1), "mo"
    m = re.fullmatch(r"LSFT\(KC_QUOT\)", k)
    if m: return '"', ""
    m = re.fullmatch(r"LCTL\(KC_MINS\)", k)
    if m: return "Ctrl –", "zoom"
    m = re.fullmatch(r"LCTL\(KC_EQL\)", k)
    if m: return "Ctrl +", "zoom"
    m = re.fullmatch(r"LALT\(LCTL\(KC_DEL\)\)", k)
    if m: return "C-A-Del", ""
    return simple(k), ""

def kind(k):
    if k in ("KC_NO","XXXXXXX"): return "no"
    if k in ("KC_TRNS","_______"): return "trns"
    if k == "QK_BOOT": return "boot"
    if k.startswith("MT("): return "mod"
    if k.startswith("LT(") or k.startswith("MO("): return "lyr"
    if k.startswith(("KC_LSFT","KC_LCTL","KC_LGUI","KC_RALT","KC_RGUI","KC_LALT","KC_RCTL","KC_RSFT")):
        return "modk"
    return "key"

FILL = {"key":"#ffffff","mod":"#d9ebff","modk":"#d9ebff","lyr":"#ffe2c2",
        "no":"#f0f0f0","trns":"#f7f7f7","boot":"#ffd0d0"}
STROKE = {"trns":"#cccccc","no":"#dddddd"}

U = 58           # px per key unit
KW = 54          # key inner size
PADX, PADY = 26, 18
TITLEH = 34
LAYER_DESC = [
 "Layer 0 — Base (QWERTY, home-row mods)",
 "Layer 1 — Function / Navigation  (hold left-inner thumb = Tab)",
 "Layer 2 — Numbers / Symbols  (hold right-inner thumb = Bspc)",
 "Layer 3 — Brackets / Media  (hold both inner thumbs)",
 "Layer 4 — System  (BOOT)",
]

maxx = max(x+w for x,y,w in pos)          # ~15
maxy = max(y for x,y,w in pos) + 1        # ~4.85
block_w = PADX*2 + maxx*U
block_h = TITLEH + PADY + maxy*U + PADY
total_h = block_h*len(layers) + 20
total_w = block_w

def esc(s): return html.escape(s, quote=True)

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" '
             f'height="{total_h}" viewBox="0 0 {total_w} {total_h}" '
             f'font-family="DejaVu Sans, Helvetica, Arial, sans-serif">')
parts.append(f'<rect width="{total_w}" height="{total_h}" fill="#fafafa"/>')

for li, layer in enumerate(layers):
    oy = li*block_h + 10
    parts.append(f'<g transform="translate(0,{oy})">')
    parts.append(f'<rect x="6" y="4" width="{block_w-12}" height="{block_h-12}" '
                 f'rx="10" fill="#ffffff" stroke="#e2e2e2"/>')
    parts.append(f'<text x="{PADX}" y="26" font-size="17" font-weight="bold" '
                 f'fill="#222">{esc(LAYER_DESC[li])}</text>')
    gy = TITLEH + PADY
    for i in range(NKEYS):
        kc = layer[i]
        x,y,w = pos[i]
        kx = PADX + x*U
        ky = gy + y*U
        kw = w*U - (U-KW)
        kkind = kind(kc)
        fill = FILL[kkind]
        stroke = STROKE.get(kkind, "#9aa4b0")
        dash = ' stroke-dasharray="3,3"' if kkind in ("trns","no") else ""
        parts.append(f'<rect x="{kx:.1f}" y="{ky:.1f}" width="{kw:.1f}" '
                     f'height="{KW}" rx="7" fill="{fill}" stroke="{stroke}"{dash}/>')
        main, sub = label(kc)
        cx = kx + kw/2
        if sub:
            parts.append(f'<text x="{cx:.1f}" y="{ky+24:.1f}" font-size="14" '
                         f'text-anchor="middle" fill="#1c1c1c">{esc(main)}</text>')
            scol = "#b06a00" if sub.startswith(("L","mo")) else "#1668c1"
            parts.append(f'<text x="{cx:.1f}" y="{ky+40:.1f}" font-size="10" '
                         f'text-anchor="middle" fill="{scol}">{esc(sub)}</text>')
        else:
            fs = 15 if len(main) <= 4 else 12
            parts.append(f'<text x="{cx:.1f}" y="{ky+KW/2+5:.1f}" font-size="{fs}" '
                         f'text-anchor="middle" fill="#1c1c1c">{esc(main)}</text>')
    parts.append('</g>')

parts.append('</svg>')
open(OUT,"w").write("\n".join(parts))
print("wrote", OUT, f"({total_w}x{total_h})")
