#!/usr/bin/env python

import sys
from math import *
from random import *
import numpy

from pyx import canvas, path, deco, trafo, style, text, color, deformer

text.set(mode="latex") 
text.set(docopt="10pt")
text.preamble(r"\usepackage{amsmath,amsfonts,amssymb}")

rgb = color.rgb
rgbfromhexstring = color.rgbfromhexstring

red, green, blue, yellow = (
    rgbfromhexstring("#d00000"),
    rgbfromhexstring("#006000"),
    rgb.blue, rgb(0.75, 0.75, 0)) 

black = rgb(0., 0., 0.) 
blue = rgb(0., 0., 0.8)
lred = rgb(1., 0.4, 0.4)
white = rgb(1., 1., 1.) 

#shade = rgb(0.75, 0.55, 0)

grey = rgb(0.75, 0.75, 0.75)
shade = grey
shade0 = rgb(0.75, 0.75, 0.75)
shade1 = rgb(0.80, 0.80, 0.80)
shade2 = rgb(0.85, 0.85, 0.85)

light_shade = rgb(0.85, 0.65, 0.1)
light_shade = rgb(0.9, 0.75, 0.4)


north = [text.halign.boxcenter, text.valign.top]
northeast = [text.halign.boxright, text.valign.top]
northwest = [text.halign.boxleft, text.valign.top]
south = [text.halign.boxcenter, text.valign.bottom]
southeast = [text.halign.boxright, text.valign.bottom]
southwest = [text.halign.boxleft, text.valign.bottom]
east = [text.halign.boxright, text.valign.middle]
west = [text.halign.boxleft, text.valign.middle]
center = [text.halign.boxcenter, text.valign.middle]


st_dashed = [style.linestyle.dashed]
st_dotted = [style.linestyle.dotted]

st_thick = [style.linewidth.thick]
st_Thick = [style.linewidth.Thick]


###############################################################################
#
#

c = canvas.canvas()


W = 3.4
H = 5.0

dy = 0.9

x, y = 0., 0.
r = 0.3

c.text(x, y, "Decoder", center)
c.text(x, y-0.2, "(classical)", north)

c.stroke(path.line(x, y+r, x, y+H)) #, [deco.earrow()])

y += dy
c.stroke(path.line(x+2*W-r, y, x+W+r, y), [deco.earrow()])
c.text(x+1.5*W, y+0.1, "noise", south)

y += 0.5*dy
c.stroke(path.line(x+r, y, x+W-r, y), [deco.earrow()])
c.text(x+0.5*W, y+0.1, "recovery", south)

y += dy
c.stroke(path.line(x+W-r, y, x+r, y), [deco.earrow()])
c.text(x+0.5*W, y+0.1, "syndrome", south)

y += 0.5*dy
c.stroke(path.line(x+0.5*W, y+0.2, x+0.5*W, y-0.2+dy), st_dotted)

y += dy

c.stroke(path.line(x+r, y, x+W-r, y), [deco.earrow()])
c.text(x+0.5*W, y+0.1, "recovery", south)

y += dy
c.stroke(path.line(x+W-r, y, x+r, y), [deco.earrow()])
c.text(x+0.5*W, y+0.1, "empty syndrome", south)



x += W
y = 0.

c.text(x, y, "System", center)
c.text(x, y-0.2, "(quantum)", north)

c.stroke(path.line(x, y+r, x, y+H)) #, [deco.earrow()])


c.writePDFfile("pic-process.pdf")

