from __future__ import annotations
from pathlib import Path

try:
    from PIL import Image, ImageTk, ImageEnhance
except Exception:  # Pillow puede no estar instalado aun
    Image = None
    ImageTk = None
    ImageEnhance = None

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / 'assets'


def asset_path(name: str) -> Path:
    return ASSETS_DIR / name


def load_image(path: str | Path, size: tuple[int, int] | None = None, *, cover: bool = False, darken: float | None = None):
    """Carga imagen para Tkinter usando Pillow.

    - size=(w,h): redimensiona.
    - cover=True: recorta manteniendo proporción para cubrir el tamaño.
    - darken=0.65: oscurece para usar como fondo con texto encima.
    Retorna None si Pillow no está instalado o si el archivo no existe.
    """
    if Image is None or ImageTk is None:
        return None
    path = Path(path)
    if not path.exists():
        return None
    try:
        img = Image.open(path).convert('RGBA')
        if size:
            w, h = size
            if cover:
                iw, ih = img.size
                scale = max(w / iw, h / ih)
                nw, nh = int(iw * scale), int(ih * scale)
                img = img.resize((nw, nh), Image.LANCZOS)
                left = max(0, (nw - w) // 2)
                top = max(0, (nh - h) // 2)
                img = img.crop((left, top, left + w, top + h))
            else:
                img.thumbnail(size, Image.LANCZOS)
        if darken is not None and ImageEnhance is not None:
            img = ImageEnhance.Brightness(img).enhance(darken)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None
