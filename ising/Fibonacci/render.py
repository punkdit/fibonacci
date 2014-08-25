#!/usr/bin/env python

import sys

from pyx import canvas, path, deco, trafo, style, text, color

text.set(mode="latex") 
text.set(docopt="12pt")
#text.preamble(r"\usepackage{amsmath}")
#text.preamble(r"\

st_dashed = [style.linestyle.dashed]
st_dotted = [style.linestyle.dotted]

def arrow(x0, y0, x1, y1, extra=[]):
    c.stroke(path.line(x0, y0, x1, y1),
        extra+[deco.earrow(size=0.1)])

#c.stroke(
#    path.curve(0, 0, 0, 4, 2, 4, 3, 3),
#    [style.linewidth.THICK, style.linestyle.dashed, color.rgb.blue,
#    deco.earrow([deco.stroked([color.rgb.red, style.linejoin.round]),
#                       deco.filled([color.rgb.green])], size=1)])

def line(x0, y0, x1, y1, extra=[]):
    c.stroke(path.line(x0, y0, x1, y1), extra)

def varrow(x, y0, y1, extra=[], label=None):
    arrow(x, y0, x, y1, extra)
    if label:
        c.text(x-0.1, (y0+y1)/2., label, [text.halign.boxright])


def harrow(x0, x1, y, extra=[], label=None):
    arrow(x0, y, x1, y, extra)
    if label:
        c.text((x0+x1)/2., y+0.1, label,
            [text.valign.bottom, text.halign.boxcenter])



# -------------------------------------------------

c = canvas.canvas()

c.text(0.0, 1.8, "$L_2$", [])
c.text(1.8, 1.8, "$D_n$", [])
harrow(0.6, 1.8, 2.0, label="$g$")

c.text(0.9, 0.0, "$L_n$", [])

arrow(0.2, 1.7, 1.0, 0.5)
#c.text(0.2, 0.8, "$\subset$", [])
c.text(0.2, 0.8, "$i$", [])

arrow(1.2, 0.5, 1.9, 1.7)
c.text(1.6, 0.8, "$\phi f$", [])

c.writeEPSfile("halftwist-factor.eps")

# -------------------------------------------------




