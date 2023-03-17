from typing import Tuple


def color_from_rgb(rgb: Tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'