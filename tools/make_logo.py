"""Turn the supplied logo (white background JPG) into the web assets.

    python tools/make_logo.py

Writes to assets/img/:
  logo.png          transparent, square, for light backgrounds
  logo-badge.png    logo on an ivory circle, for dark backgrounds
and to the project root:
  favicon.ico, favicon-32.png, apple-touch-icon.png
"""
import pathlib
from PIL import Image, ImageChops, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'tools' / 'logo-source.jpg'
OUT = ROOT / 'assets' / 'img'
IVORY = (244, 242, 234, 255)


def transparent(im):
    """Near-white becomes transparent, with soft edges so anti-aliasing stays smooth."""
    im = im.convert('RGB')
    # How far each pixel is from white (0 = white).
    dist = ImageChops.invert(im).convert('L')
    alpha = dist.point(lambda d: 0 if d < 12 else 255 if d > 60 else int((d - 12) * 255 / 48))
    rgba = im.convert('RGBA')
    rgba.putalpha(alpha)
    return rgba


def square(im, pad_ratio=0.04):
    im = im.crop(im.getbbox())
    side = int(max(im.size) * (1 + 2 * pad_ratio))
    canvas = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
    return canvas


def badge(logo, size):
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(canvas).ellipse((0, 0, size - 1, size - 1), fill=IVORY)
    inner = int(size * 0.74)
    mark = logo.resize((inner, inner), Image.LANCZOS)
    canvas.paste(mark, ((size - inner) // 2, (size - inner) // 2), mark)
    return canvas


def on_ivory(logo, size, pad=0.12):
    canvas = Image.new('RGBA', (size, size), IVORY)
    inner = int(size * (1 - 2 * pad))
    mark = logo.resize((inner, inner), Image.LANCZOS)
    canvas.paste(mark, ((size - inner) // 2, (size - inner) // 2), mark)
    return canvas.convert('RGB')


def main():
    logo = square(transparent(Image.open(SRC)))
    logo.resize((256, 256), Image.LANCZOS).save(OUT / 'logo.png', optimize=True)
    badge(logo, 256).save(OUT / 'logo-badge.png', optimize=True)
    # Favicons: tight crop reads better at 16-32px.
    tight = square(transparent(Image.open(SRC)), pad_ratio=0.0)
    tight.resize((32, 32), Image.LANCZOS).save(ROOT / 'favicon-32.png', optimize=True)
    tight.resize((256, 256), Image.LANCZOS).save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    on_ivory(logo, 180).save(ROOT / 'apple-touch-icon.png', optimize=True)
    for p in ['assets/img/logo.png', 'assets/img/logo-badge.png', 'favicon-32.png', 'favicon.ico', 'apple-touch-icon.png']:
        print(p, (ROOT / p).stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
