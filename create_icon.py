"""
簿記３級アプリ オリジナルアイコン作成
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"

def make_icon(size, filename):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    pad = int(size * 0.06)
    r = int(size * 0.22)

    # ── 背景：深緑グラデーション風（2段重ね）
    draw.rounded_rectangle([pad, pad, size-pad, size-pad], radius=r,
                            fill=(26, 122, 74, 255))
    # 上部ハイライト
    draw.rounded_rectangle([pad, pad, size-pad, size//2], radius=r,
                            fill=(44, 160, 100, 200))

    cx, cy = size // 2, size // 2

    # ── 帳簿ページ（白い台形ページ風）
    book_w = int(size * 0.60)
    book_h = int(size * 0.44)
    bx = cx - book_w // 2
    by = int(size * 0.22)
    br = int(size * 0.06)
    draw.rounded_rectangle([bx, by, bx+book_w, by+book_h], radius=br,
                            fill=(255, 255, 255, 240), outline=(200, 230, 210, 180), width=2)

    # ── 帳簿の縦線（勘定科目線）
    line_x = bx + int(book_w * 0.36)
    draw.line([line_x, by+8, line_x, by+book_h-8],
              fill=(26, 122, 74, 180), width=2)

    # ── 帳簿の横線（行線）
    row_count = 4
    row_gap = (book_h - 20) // (row_count + 1)
    for i in range(1, row_count + 1):
        ry = by + 10 + row_gap * i
        draw.line([bx+8, ry, bx+book_w-8, ry],
                  fill=(180, 210, 190, 160), width=1)

    # ── 左上：借方 ラベル
    try:
        lbl_font = ImageFont.truetype(FONT_PATH, int(size * 0.085))
    except:
        lbl_font = ImageFont.load_default()

    lbl_d = "借"
    lbl_c = "貸"
    bb = draw.textbbox((0,0), lbl_d, font=lbl_font)
    lw = bb[2]-bb[0]
    draw.text((bx + (line_x-bx)//2 - lw//2, by+6), lbl_d,
              font=lbl_font, fill=(26,100,60,220))
    bb2 = draw.textbbox((0,0), lbl_c, font=lbl_font)
    lw2 = bb2[2]-bb2[0]
    draw.text((line_x + (bx+book_w-line_x)//2 - lw2//2, by+6), lbl_c,
              font=lbl_font, fill=(26,100,60,220))

    # ── 金額の数字っぽいライン（細い黒帯）
    for i, row_vals in enumerate([(0.55, 0.30), (0.60, 0.25), (0.45, 0.40)]):
        ry = by + 10 + row_gap * (i+1)
        # 左側金額バー
        bar_w_l = int((line_x - bx - 16) * row_vals[0])
        bar_h = max(2, row_gap - 12)
        if bar_w_l > 4:
            draw.rounded_rectangle([bx+8, ry+4, bx+8+bar_w_l, ry+4+bar_h],
                                    radius=2, fill=(60,60,60,80))
        # 右側金額バー
        bar_w_r = int((bx+book_w - line_x - 16) * row_vals[1])
        if bar_w_r > 4:
            draw.rounded_rectangle([line_x+8, ry+4, line_x+8+bar_w_r, ry+4+bar_h],
                                    radius=2, fill=(60,60,60,80))

    # ── 鉛筆アイコン（右下）
    pen_cx = bx + book_w + int(size*0.02)
    pen_cy = by + book_h - int(size*0.04)
    pen_size = int(size * 0.16)
    angle = -40  # degrees
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    def rot(px, py):
        return (pen_cx + px*cos_a - py*sin_a,
                pen_cy + px*sin_a + py*cos_a)

    pw = int(pen_size * 0.25)
    ph = pen_size
    pts_body = [rot(-pw, -ph//2), rot(pw, -ph//2),
                rot(pw,  ph//2), rot(-pw,  ph//2)]
    draw.polygon(pts_body, fill=(255, 210, 60, 240), outline=(180,140,20,200))
    # 先端
    tip_pts = [rot(-pw, ph//2), rot(pw, ph//2), rot(0, ph//2 + int(pen_size*0.35))]
    draw.polygon(tip_pts, fill=(245, 230, 200, 255), outline=(180,140,20,200))
    # 消しゴム
    eraser_pts = [rot(-pw, -ph//2), rot(pw, -ph//2),
                  rot(pw, -ph//2-int(pen_size*0.2)), rot(-pw, -ph//2-int(pen_size*0.2))]
    draw.polygon(eraser_pts, fill=(255, 140, 140, 240))

    # ── 上部テキスト「３級」
    try:
        top_font = ImageFont.truetype(FONT_BOLD if os.path.exists(FONT_BOLD) else FONT_PATH,
                                      int(size * 0.12))
    except:
        top_font = ImageFont.load_default()

    txt = "３　級"
    bb3 = draw.textbbox((0,0), txt, font=top_font)
    tw = bb3[2]-bb3[0]
    tx = cx - tw // 2
    ty = int(size * 0.07)
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,-2),(-2,2),(2,2)]:
        draw.text((tx+dx, ty+dy), txt, font=top_font, fill=(0,80,40,160))
    draw.text((tx, ty), txt, font=top_font, fill=(255,255,255,255))

    # ── 下部テキスト「簿記」
    try:
        main_font = ImageFont.truetype(FONT_BOLD if os.path.exists(FONT_BOLD) else FONT_PATH,
                                       int(size * 0.16))
    except:
        main_font = ImageFont.load_default()

    txt2 = "簿　記"
    bb4 = draw.textbbox((0,0), txt2, font=main_font)
    tw2 = bb4[2]-bb4[0]
    th2 = bb4[3]-bb4[1]
    tx2 = cx - tw2 // 2
    ty2 = size - pad - th2 - int(size * 0.07)
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,-2),(-2,2),(2,2)]:
        draw.text((tx2+dx, ty2+dy), txt2, font=main_font, fill=(0,80,40,160))
    draw.text((tx2, ty2), txt2, font=main_font, fill=(255,255,255,255))

    img.save(os.path.join(OUT_DIR, filename))
    print(f"  作成: {filename} ({size}x{size})")


if __name__ == "__main__":
    print("簿記3級アプリ アイコン作成中...")
    make_icon(512, "icon_512.png")   # Webアプリ用・高解像度
    make_icon(192, "icon_192.png")   # PWA manifest用
    make_icon(96,  "icon_96.png")    # ファビコン用
    print("完了！")
