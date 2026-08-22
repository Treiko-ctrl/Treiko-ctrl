# -*- coding: utf-8 -*-
"""
Generiert die GitHub-Profilkarten dark.svg und light.svg.

Links ein Panel mit dem Profilbild als ASCII-Matrix, rechts ein Info-Panel
mit Punkt-Leader-Zeilen. Inhalte stehen in ROWS, Farben in THEMES.

Aufruf:  python generate_card.py
"""
import os
from html import escape

AVATAR_FILE = "avatar.png"

# ---------- Profilbild -> ASCII ----------

RAMP = " .`':,^;~-+=*csvo?tzxjJ$&%@#"   # dunkel -> hell
ART_COLS = 78
ART_ROWS = 40


def avatar_ascii():
    """Rendert avatar.png als ASCII-Matrix [[(zeichen, helligkeit 0..1), ...], ...]."""
    if not os.path.exists(AVATAR_FILE):
        return None
    from PIL import Image, ImageEnhance, ImageOps

    img = Image.open(AVATAR_FILE).convert("RGB")
    side = min(img.size)
    left, top = (img.width - side) // 2, (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = img.resize((ART_COLS, ART_ROWS), Image.LANCZOS)

    rows = []
    for y in range(ART_ROWS):
        row = []
        for x in range(ART_COLS):
            r, g, b = img.getpixel((x, y))
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            row.append((RAMP[min(len(RAMP) - 1, int(lum * len(RAMP)))], lum))
        rows.append(row)
    return rows


def mix(c1, c2, f):
    """Blendet zwei Hex-Farben; f = 0 -> c1, f = 1 -> c2."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))


# ---------- Inhalt des Info-Panels ----------
# ("kv", Schluessel, Wert) | ("sec", Titel, "") | ("gap", "", "") | ("note", Text, "")

ROWS = [
    ("kv", "Subject", "Treiko"),
    ("kv", "Role", "Full-Stack Dev · Discord-Bot-Entwickler"),
    ("kv", "Origin", "Deutschland"),
    ("kv", "Focus", "NexCore — All-in-One Discord-Bot"),
    ("kv", "Status", "Building • Selfhosting • Shipping"),
    ("kv", "ToolChain", "VS Code, Git, Docker, nginx"),
    ("gap", "", ""),
    ("kv", "Core.Lang", "JavaScript, TypeScript, Python"),
    ("kv", "Core.Frontend", "React, Next.js, HTML, CSS"),
    ("kv", "Core.Backend", "Node.js, Flask, FastAPI, REST APIs"),
    ("kv", "Core.Database", "MySQL, MongoDB"),
    ("kv", "Core.Infra", "Linux, Docker, nginx, Cloudflare"),
    ("gap", "", ""),
    ("sec", "Projects", ""),
    ("kv", "Bot.NexCore", "Discord-Bot mit Web-Panel"),
    ("kv", "Sport.IronHub", "Ironman-Trainingsplattform"),
    ("kv", "Game.TanoaVice", "Arma-3-RP-Infrastruktur"),
    ("kv", "Logi.GRTLHub", "ETS2-Speditions-Tracker"),
    ("gap", "", ""),
    ("sec", "Contact", ""),
    ("kv", "Grid.Mail", "kontakt@nexcoredev.de"),
    ("kv", "Grid.Web", "nexcoredev.de"),
    ("kv", "Grid.Discord", "NexCore Development"),
    ("kv", "Grid.Github", "Treiko-ctrl"),
    ("gap", "", ""),
    ("sec", "Live Stats", ""),
    ("note", "Triathlon-Modus aktiv · Ziel: Ironman", ""),
]

HOST = "treiko@nexcore"
TITLE = "treiko@nexcore ~ % ./profile.sh --live"

# ---------- Themes ----------

THEMES = {
    "dark": dict(
        bgA="#071026", bgB="#03060f", chrome="#0a1526", panel="#050d1c",
        border="#1d5f7a", label="#3fe0f0", key="#3fe0f0", keyDim="#2a93ad",
        value="#dfe9f5", dots="#1b3a52", note="#9fb6cc", tag="#6f8aa5",
        artDark="#0e2f6b", artLite="#8fe3ff", live="#ff4d5e",
    ),
    "light": dict(
        bgA="#eef4fb", bgB="#e2ebf6", chrome="#dbe6f2", panel="#f7fbff",
        border="#7fb3c9", label="#0d6c85", key="#0d6c85", keyDim="#3f8ea3",
        value="#16283a", dots="#b7cbdb", note="#41586e", tag="#5b7893",
        artDark="#d7e6f4", artLite="#0b3f7a", live="#c62b3a",
    ),
}

# ---------- Geometrie ----------

W, H = 1180, 610
BAR_H = 34
PAD = 14
LEFT = dict(x=PAD, y=48, w=488, h=H - 48 - PAD)
RIGHT = dict(x=512, y=48, w=W - 512 - PAD, h=H - 48 - PAD)

INFO_SIZE = 14
CHAR_W = INFO_SIZE * 0.6
INFO_X = RIGHT["x"] + 16
INFO_COLS = int((RIGHT["w"] - 32) / CHAR_W)
INFO_Y = RIGHT["y"] + 46
INFO_ROW = 18.2

ART_SIZE = 10
ART_ROW_H = 11.2
ART_X = LEFT["x"] + (LEFT["w"] - ART_COLS * ART_SIZE * 0.6) / 2
ART_Y = LEFT["y"] + 48

AVATAR = avatar_ascii()
SEP = chr(10) + "    "


def panel(t, box, label):
    """Rahmen mit Beschriftung, die in der oberen Kante sitzt."""
    lx, ly = box["x"] + 18, box["y"]
    return (
        f'<rect x="{box["x"]}" y="{box["y"]}" width="{box["w"]}" height="{box["h"]}" '
        f'rx="4" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1"/>'
        f'<rect x="{lx - 6}" y="{ly - 9}" width="{len(label) * 7.4 + 12}" height="18" '
        f'fill="{t["panel"]}"/>'
        f'<text x="{lx}" y="{ly + 5}" class="label">{escape(label)}</text>'
    )


def leader_row(t, kind, key, value):
    """Baut eine Zeile des Info-Panels als <tspan>-Kette."""
    if kind == "gap":
        return f'<tspan fill="{t["dots"]}">.</tspan>'

    if kind == "sec":
        dashes = "─" * max(1, INFO_COLS - len(key) - 5)
        return (
            f'<tspan fill="{t["keyDim"]}">─ </tspan>'
            f'<tspan fill="{t["label"]}" font-weight="700">{escape(key)}</tspan>'
            f'<tspan fill="{t["dots"]}"> {dashes}</tspan>'
        )

    if kind == "note":
        return (
            f'<tspan fill="{t["key"]}">&gt; </tspan>'
            f'<tspan fill="{t["note"]}">{escape(key)}</tspan>'
        )

    head, _, tail = key.partition(".")
    n_dots = max(1, INFO_COLS - 4 - len(key) - len(value))
    parts = [f'<tspan fill="{t["dots"]}">. </tspan>']
    if tail:
        parts.append(f'<tspan fill="{t["keyDim"]}" font-weight="700">{escape(head)}.</tspan>')
        parts.append(f'<tspan fill="{t["key"]}" font-weight="700">{escape(tail)}</tspan>')
    else:
        parts.append(f'<tspan fill="{t["key"]}" font-weight="700">{escape(head)}</tspan>')
    parts.append(f'<tspan fill="{t["keyDim"]}">:</tspan>')
    parts.append(f'<tspan fill="{t["dots"]}"> {"." * n_dots} </tspan>')
    parts.append(f'<tspan fill="{t["value"]}">{escape(value)}</tspan>')
    return "".join(parts)


def build(theme_name):
    t = THEMES[theme_name]

    # --- ASCII-Portrait, Farbe nach Helligkeit ---
    art_rows = []
    if AVATAR:
        for r, row in enumerate(AVATAR):
            spans, cur, run = [], None, ""
            for ch, lum in row:
                bucket = round(lum * 6) / 6          # Farbstufen zusammenfassen
                if bucket != cur:
                    if run:
                        spans.append(
                            f'<tspan fill="{mix(t["artDark"], t["artLite"], cur)}">'
                            f"{escape(run)}</tspan>"
                        )
                    cur, run = bucket, ""
                run += ch
            if run:
                spans.append(
                    f'<tspan fill="{mix(t["artDark"], t["artLite"], cur)}">'
                    f"{escape(run)}</tspan>"
                )
            art_rows.append(
                f'<text x="{ART_X:.1f}" y="{ART_Y + r * ART_ROW_H:.1f}" class="art" '
                f'xml:space="preserve">{"".join(spans)}</text>'
            )
    art = SEP.join(art_rows)

    # --- Info-Zeilen mit Tipp-Animation ---
    clips, lines = [], []
    for i, (kind, key, value) in enumerate(ROWS):
        y = INFO_Y + i * INFO_ROW
        begin = round(0.55 + i * 0.075, 3)
        clips.append(
            f'<clipPath id="r{i}"><rect x="{INFO_X}" y="{y - 14}" width="0" height="19">'
            f'<animate attributeName="width" from="0" to="{RIGHT["w"]}" dur="0.3s" '
            f'begin="{begin}s" fill="freeze"/></rect></clipPath>'
        )
        lines.append(
            f'<text x="{INFO_X}" y="{y:.1f}" class="info" xml:space="preserve" '
            f'clip-path="url(#r{i})">{leader_row(t, kind, key, value)}</text>'
        )
    cursor_y = INFO_Y + len(ROWS) * INFO_ROW - 13
    last = round(0.55 + len(ROWS) * 0.075, 3)
    host_dashes = "─" * max(1, INFO_COLS - len(HOST) - 3)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Treiko - Profilkarte">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="{t['bgA']}"/>
      <stop offset="100%" stop-color="{t['bgB']}"/>
    </linearGradient>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{t['label']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t['label']}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{t['label']}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="scanlines" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="1" fill="{t['label']}" opacity="0.035"/>
    </pattern>
    <clipPath id="card"><rect x="0" y="0" width="{W}" height="{H}" rx="10"/></clipPath>
    <clipPath id="artReveal">
      <rect x="{LEFT['x']}" y="{LEFT['y']}" width="{LEFT['w']}" height="0">
        <animate attributeName="height" from="0" to="{LEFT['h']}" dur="1.9s"
                 begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
      </rect>
    </clipPath>
    {''.join(clips)}
  </defs>

  <style>
    text {{ font-family: "JetBrains Mono","Fira Code","SFMono-Regular",Consolas,monospace; }}
    .art  {{ font-size: {ART_SIZE}px; }}
    .info {{ font-size: {INFO_SIZE}px; }}
    .label {{ font-size: 11px; fill: {t['label']}; letter-spacing: 0.16em; }}
    .host {{ font-size: {INFO_SIZE}px; font-weight: 700; fill: {t['label']}; }}
    .tag  {{ font-size: 12px; fill: {t['tag']}; letter-spacing: 0.04em; }}
    .live {{ font-size: 11px; fill: {t['live']}; letter-spacing: 0.18em; }}
  </style>

  <rect width="{W}" height="{H}" rx="10" fill="url(#bg)"/>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#scanlines)"/>
    <rect x="0" y="-140" width="{W}" height="140" fill="url(#scanGrad)">
      <animate attributeName="y" from="-140" to="{H}" dur="7s" repeatCount="indefinite"/>
    </rect>

    <!-- Fensterleiste -->
    <rect x="0" y="0" width="{W}" height="{BAR_H}" fill="{t['chrome']}"/>
    <circle cx="18" cy="{BAR_H / 2}" r="5" fill="#ff5f57"/>
    <circle cx="36" cy="{BAR_H / 2}" r="5" fill="#febc2e"/>
    <circle cx="54" cy="{BAR_H / 2}" r="5" fill="#28c840"/>
    <text x="{W / 2}" y="{BAR_H / 2 + 4}" class="tag" text-anchor="middle">{escape(TITLE)}</text>
    <circle cx="{W - 96}" cy="{BAR_H / 2}" r="4" fill="{t['live']}">
      <animate attributeName="opacity" values="1;0.15;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <text x="{W - 84}" y="{BAR_H / 2 + 4}" class="live">SCANNING</text>

    <!-- Panels -->
    {panel(t, LEFT, "VISUAL.MAP")}
    {panel(t, RIGHT, "SYSTEM.INFO")}

    <!-- Profilbild als ASCII -->
    <g clip-path="url(#artReveal)">
    {art}
    </g>

    <!-- Info-Panel -->
    <text x="{INFO_X}" y="{RIGHT['y'] + 26}" class="host" xml:space="preserve">{escape(HOST)}<tspan fill="{t['dots']}" font-weight="400"> {host_dashes}</tspan></text>
    {SEP.join(lines)}
    <rect x="{INFO_X}" y="{cursor_y:.1f}" width="8" height="16" fill="{t['label']}" opacity="0">
      <animate attributeName="opacity" values="1;0;1" dur="1.1s" begin="{last}s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="none"
        stroke="{t['border']}" stroke-width="1"/>
</svg>
"""


if __name__ == "__main__":
    for name in THEMES:
        with open(f"{name}.svg", "w", encoding="utf-8") as f:
            f.write(build(name))
        print(f"{name}.svg geschrieben")
