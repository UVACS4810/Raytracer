import dataclasses


def bound(v: float, high: float, low: float) -> float:
    return max(low, min(high, v))

@dataclasses.dataclass
class RGB():
    """RGB is really sRGB. It is a gamma corrected version of RGB with values in range 0-255
    """
    r: float
    g: float
    b: float
    a: float = 255
    def __add__(self, other):
        return RGB(
            min((self.r + other.r), 255),
            min((self.g + other.g), 255),
            min((self.b + other.b), 255),
            min((self.a + other.a), 255),
        )
    def round(self):
        """Since the RGB values can be floats in range 0-255, this allows us to round to the nearest integer
        """
        self.r = round(self.r)
        self.g = round(self.g)
        self.b = round(self.b)
        self.a = round(self.a)

def gamma_correction(v: float) -> float:
    if v <= 0.0031308:
        return 12.92 * v
    return 1.055 * v ** (1/2.4) - 0.055

@dataclasses.dataclass
class RGBLinear():
    """Linear RGB allows for linear color interpolation. It do not work with gamma correction. Thus, before we display
    a pixel, we will convert it into `RGB`.

    Returns:
        [type]: [description]
    """
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 1.0

    def __add__(self, other):
        return RGBLinear(
            bound((self.r + other.r), 255, 0),
            bound((self.g + other.g), 255, 0),
            bound((self.b + other.b), 255, 0),
            bound((self.a + other.a), 255, 0),
        )
    def __mul__(self, other):
        return RGBLinear(
            bound((self.r * other.r), 255, 0),
            bound((self.g * other.g), 255, 0),
            bound((self.b * other.b), 255, 0),
            bound((self.a * other.a), 255, 0),
        )
    def as_rgb(self, rounded = False) -> RGB:
        r = bound(gamma_correction(self.r) * 255, 255, 0)
        g = bound(gamma_correction(self.g) * 255, 255, 0)
        b = bound(gamma_correction(self.b) * 255, 255, 0)
        a = bound(self.a * 255, 255, 0)
        if rounded:
            return RGB(round(r), round(g), round(b), round(a))
        else:
            return RGB(r, g, b, a)

def over_operator(ca: int, cb: int, aa: int, ab, a0: int) -> int:
    return round((ca * aa + cb*ab*(1-aa))/a0)

def add_pixel_colors(a: RGB, b: RGB) -> RGB:
    """Used to compute the new color of two pixels with alpha values. Uses the over
    operator to acomplish this

    Args:
        a (RGB): the over color
        b (RGB): the under color

    Returns:
        RGB: the new pixel color
    """
    aa = a.a/255
    ab = b.a/255
    a0 = aa + ab * (1-(aa))

    r = over_operator(a.r, b.r, aa, ab, a0)
    g = over_operator(a.g, b.g, aa, ab, a0)
    b = over_operator(a.b, b.b, aa, ab, a0)

    a0 = round(a0*255)
    return RGB(r, g, b, a0)

def convert_hex_to_rgb(hex: str) -> RGB:
    # we will get the "hex" value in the form "#rrggbb"
    # The first step will be to strip the "#" char.
    hex = hex.strip("#")
    # Next we will seperate the string into "rr" "gg" "bb"
    # Convert the values into integers
    rr = int(hex[0:2], base=16)
    gg = int(hex[2:4], base=16)
    bb = int(hex[4:6], base=16)
    aa = 255
    if len(hex) > 6:
        aa = int(hex[6:8], base=16)
    # store the values in an RGB class
    return RGB(rr, gg, bb, aa)