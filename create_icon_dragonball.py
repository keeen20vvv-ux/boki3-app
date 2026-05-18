"""
ドラゴンボール風 簿記３級アイコン
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"

def font(size, bold=True):
    path = FONT_BOLD if (bold and os.path.exists(FONT_BOLD)) else FONT_PATH
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def outline_text(draw, x, y, text, fnt, fill, outline, width=3):
    for dx in range(-width, width+1):
        for dy in range(-width, width+1):
            if dx*dx + dy*dy <= width*width + 1:
                draw.text((x+dx, y+dy), text, font=fnt, fill=outline)
    draw.text((x, y), text, font=fnt, fill=fill)

def draw_star(draw, cx, cy, r, color, outline_color, outline_w=2):
    pts = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(angle), cy + rad * math.sin(angle)))
    draw.polygon(pts, fill=color, outline=outline_color)
    # 外枠を再描画
    from PIL import ImageDraw as ID
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i+1)%len(pts)]
        draw.line([x1,y1,x2,y2], fill=outline_color, width=outline_w)

def make_dragonball_icon(size, filename):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    pad = int(size * 0.05)
    r_bg = int(size * 0.22)

    # ── 背景：オレンジ〜黄色グラデーション
    for y in range(pad, size - pad):
        t = (y - pad) / (size - 2*pad)
        rc = int(255 * 1.0)
        gc = int(160 - t*60)
        bc = int(0)
        draw.line([(pad, y), (size-pad, y)], fill=(rc, gc, bc, 255))
    # 角丸マスク用：角の外を消す
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([pad, pad, size-pad, size-pad], radius=r_bg, fill=255)
    img.putalpha(mask)
    draw = ImageDraw.Draw(img, "RGBA")

    cx, cy = size // 2, size // 2

    # ── オーラ放射線（背景エフェクト）
    aura_cx, aura_cy = cx, int(size * 0.55)
    for i in range(24):
        angle = math.radians(i * 15)
        length = int(size * 0.75)
        ex = aura_cx + int(length * math.cos(angle))
        ey = aura_cy + int(length * math.sin(angle))
        draw.line([aura_cx, aura_cy, ex, ey], fill=(255, 220, 80, 50), width=max(1, size//100))

    # ── ドラゴンボール本体（大きな球）
    ball_r = int(size * 0.30)
    ball_cx = cx
    ball_cy = int(size * 0.50)

    # 球の影
    draw.ellipse([ball_cx - ball_r + 6, ball_cy - ball_r + 6,
                  ball_cx + ball_r + 6, ball_cy + ball_r + 6],
                 fill=(180, 80, 0, 120))

    # 球本体（オレンジ）
    draw.ellipse([ball_cx - ball_r, ball_cy - ball_r,
                  ball_cx + ball_r, ball_cy + ball_r],
                 fill=(255, 140, 20, 255), outline=(180, 60, 0, 255),
                 width=max(2, size//80))

    # 球のハイライト（白い光沢）
    hl_r = int(ball_r * 0.55)
    hl_cx = ball_cx - int(ball_r * 0.20)
    hl_cy = ball_cy - int(ball_r * 0.22)
    # グラデーション状に複数楕円
    for i in range(5):
        alpha = 120 - i * 22
        dr = int(hl_r * (1 - i*0.18))
        draw.ellipse([hl_cx - dr, hl_cy - int(dr*0.6),
                      hl_cx + dr, hl_cy + int(dr*0.6)],
                     fill=(255, 255, 255, alpha))

    # 球の輪郭を強調
    draw.ellipse([ball_cx - ball_r, ball_cy - ball_r,
                  ball_cx + ball_r, ball_cy + ball_r],
                 outline=(140, 40, 0, 255), width=max(3, size//60))

    # ── 星（３個：３級を表す）
    star_positions = [
        (ball_cx,               ball_cy - int(ball_r*0.30)),
        (ball_cx - int(ball_r*0.35), ball_cy + int(ball_r*0.20)),
        (ball_cx + int(ball_r*0.35), ball_cy + int(ball_r*0.20)),
    ]
    star_r = int(ball_r * 0.17)
    for (sx, sy) in star_positions:
        draw_star(draw, sx, sy, star_r, (220, 40, 40, 255), (100, 0, 0, 255), max(1, size//150))

    # ── 上部テキスト「簿記」（マンガ風太字）
    fs_main = int(size * 0.19)
    fnt_main = font(fs_main)
    txt_main = "簿　記"
    bb = draw.textbbox((0,0), txt_main, font=fnt_main)
    tw = bb[2]-bb[0]; th = bb[3]-bb[1]
    tx = cx - tw // 2
    ty = int(size * 0.05)
    outline_text(draw, tx, ty, txt_main, fnt_main,
                 fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=max(3, size//100))

    # ── 下部テキスト「３級」（オレンジ縁取り）
    fs_sub = int(size * 0.14)
    fnt_sub = font(fs_sub)
    txt_sub = "３　級"
    bb2 = draw.textbbox((0,0), txt_sub, font=fnt_sub)
    tw2 = bb2[2]-bb2[0]; th2 = bb2[3]-bb2[1]
    tx2 = cx - tw2 // 2
    ty2 = size - pad - th2 - int(size * 0.06)
    outline_text(draw, tx2, ty2, txt_sub, fnt_sub,
                 fill=(255, 240, 60, 255), outline=(0, 0, 0, 255), width=max(3, size//100))

    # ── 装飾スパーク（四隅）
    spark_r = int(size * 0.04)
    sparks = [
        (pad + int(size*0.12), pad + int(size*0.12)),
        (size - pad - int(size*0.12), pad + int(size*0.12)),
    ]
    for (sx, sy) in sparks:
        draw_star(draw, sx, sy, spark_r, (255, 255, 100, 220), (180, 120, 0, 200), max(1, size//150))

    img.save(os.path.join(OUT_DIR, filename))
    print(f"  作成: {filename} ({size}x{size})")


if __name__ == "__main__":
    print("ドラゴンボール風アイコン作成中...")
    make_dragonball_icon(512, "icon_512.png")
    make_dragonball_icon(192, "icon_192.png")
    make_dragonball_icon(96,  "icon_96.png")
    print("完了！")
