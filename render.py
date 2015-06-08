#!/usr/bin/env python

import sys
from math import *
from random import *
import numpy

from pyx import canvas, path, deco, trafo, style, text, color, deformer

text.set(mode="latex") 
text.set(docopt="12pt")
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

shade = rgb(0.75, 0.55, 0)
grey = rgb(0.75, 0.75, 0.75)

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



if 0:
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
    
    text.set(docopt="12pt")


#############################################################################
#
#

def anyon(x, y, r=0.07):
    c.fill(path.circle(x, y, r), [white])
    c.stroke(path.circle(x, y, r), [red, style.linewidth.thick])

from qupy.ldpc.solve import parse
from qupy.braid.tree import Tree

l = 8
w, h = 0.8, 0.8
m = 0.05


if 1:
    seed(2)
    data = numpy.zeros((l, l), dtype=numpy.int32)
    
    for count in range(10):
      if random()<0.5:
        i = randint(0, l-2)
        j = randint(0, l-1)
        data[i, j] += 1
        data[i+1, j] += 1
      else:
        # horizontal
        i = randint(0, l-1)
        j = randint(0, l-2)
        data[i, j] += 1
        data[i, j+1] += 1
    
    for i in range(l):
      for j in range(l):
        if data[i,j]>1:
          if random()<0.5:
            data[i,j]=0
          else:
            data[i,j]=1

else:
    data = parse("""
........
........
...1....
...1....
..1.....
........
.11.....
........
""")

#print data

data = data[1:, :7]
l = 7

sites = [(i, j) for i in range(l) for j in range(l)]
nbd = dict(((i, j), []) for (i, j) in sites)
for i in range(l):
  for j in range(l):
    items = nbd[i, j]
    if (i+1, j) in nbd:
        items.append((i+1, j))
    if (i-1, j) in nbd:
        items.append((i-1, j))
    if (i, j+1) in nbd:
        items.append((i, j+1))
    if (i, j-1) in nbd:
        items.append((i, j-1))


def join1(clusters):
    # join clusters using "T_1" separation
    j = 0
    while j < len(clusters):
        cj = clusters[j]
        for k in range(j+1, len(clusters)):
            ck = clusters[k]
            assert len(ck) == 1 
            for c in cj.sites:
                if ck.root in nbd[c]:
                    cj.add(c, ck.root) # c <-- ck.root
                    clusters.pop(k)
                    break
            else:
                continue
            break
            # meow :-)
        else:
            j += 1 

def grow(clusters):
    width = 1 # ?
    for cluster in clusters:
        cluster.grow(nbd, width)

def join(clusters):
    j = 0
    while j < len(clusters):
        delta = len(clusters) - j
        cj = clusters[j]
        for k in range(j+1, len(clusters)):
            ck = clusters[k]
            if cj.intersects(ck):
                clusters[j] = cj.join(ck)
                clusters.pop(k)
                break
        else:
            j += 1
        assert len(clusters)-j < delta

def coord(i, j):
    return (j+0.5)*w-m, (i+0.5)*h-m


def draw(dx=0., dy=0.):

    r = 4.*m
    data1 = data.copy()
    lines = []
    for tree in trees:
      for p0 in tree.sites:
        x0, y0 = coord(*p0)
        c.fill(path.circle(x0+dx, y0+dy, r), [grey])
        p1 = tree.parent[p0]
        #print p0, p1
        if p1 is None:
            continue # root
        lines.append((p0, p1))

        x1, y1 = coord(*p1)
        #data1[p0] = 0
        #c.stroke(path.line(x0+dx, y0+dy, x1+dx, y1+dy),
        #    [style.linewidth.Thick, deco.earrow(size=0.3)])

        if x0==x1:
            c.fill(path.rect(x0-r+dx, y0+dy, 2*r, y1-y0), [grey])
        else:
            c.fill(path.rect(x0+dx, y0-r+dy, x1-x0, 2*r), [grey])
        c.fill(path.circle(x0+dx, y0+dy, r), [grey])
        c.fill(path.circle(x1+dx, y1+dy, r), [grey])
        #c.stroke(path.line(x0+dx, y0+dy, x1+dx, y1+dy),
        #    [style.linewidth.THICK, style.linecap.round, grey])

    for (p0, p1) in lines:
        x0, y0 = coord(*p0)
        x1, y1 = coord(*p1)
        data1[p0] = 0
        c.stroke(path.line(x0+dx, y0+dy, x1+dx, y1+dy),
            [style.linewidth.Thick, deco.earrow(size=0.3)])

    for i, j in sites:
        c.stroke(path.rect(j*w+dx, i*h+dy, w-2*m, h-2*m))
        if data[i,j]:
            x, y = coord(i, j)
            anyon(x+dx, y+dy, 0.1*w)

    data[:] = data1


c = canvas.canvas()

#print nbd
trees = [Tree(site) for site in sites if data[site]]
join1(trees)

c.text(-0.7, 0., "(a)")
draw(0., 0.)

grow(trees)
join(trees)

x = l*w+1.2*w
c.text(x-0.7, 0., "(b)")
draw(x, 0.)


#c.writePDFfile("pic-decode.pdf")
c.writeEPSfile("pic-decode.eps")


#############################################################################
#
#


#sys.exit(0)
#text.set(docopt="10pt")

dashed = []
dotted = [style.linestyle.dashed]

c = canvas.canvas()
old_c = None
def push():
    global c, old_c
    assert old_c is None
    old_c = c
    c = canvas.canvas()
    
def pop(extra=[]):
    global c, old_c
    old_c.insert(c, extra)
    c = old_c
    old_c = None


# --------------------------------------------------------------------

w, h = 1.0, 1.0
m = 0.1

#x0, y0 = 0.6, h + 10*m
x0, y0 = 0., 0.

push()
#c.text(x0-0.8, y0, "(a)")

c.stroke(path.rect(x0, y0, w, h), dashed)
c.stroke(path.rect(x0+w+m, y0, w, h), dotted)

grarrow = [green, style.linewidth.THick, deco.earrow(size=0.2)]

y = y0+0.3*h
c.stroke(path.line(x0+0.5*w, y, x0+1.5*w+m, y), grarrow)
anyon(x0+0.8*w, y)
anyon(x0+m+1.2*w, y)
    
y = y0+0.7*h
c.stroke(path.line(x0+1.5*w+m, y, x0+0.5*w, y), grarrow)
anyon(x0+0.8*w, y)
anyon(x0+m+1.2*w, y)

pop([trafo.rotate(-90), trafo.translate(0.8, 2.5*h)])
c.text(0., 0.5*h, "(a)")

# --------------------------------------------------------------------

#x0, y0 = 0.6, 0.
    
#c.text(x0-0.8, y0, "(b)")
push()

c.stroke(path.rect(x0, y0, w, h), dashed)
c.stroke(path.rect(x0+w+m, y0, w, h), dotted)


p = path.path(
    path.moveto(x0+0.5*w, y0-0.3*h), 
    path.lineto(x0+0.5*w, y0+0.3*h), 
    path.lineto(x0+1.5*w+m, y0+0.3*h),
    path.lineto(x0+1.5*w+m, y0+0.7*h), 
    path.lineto(x0+0.5*w, y0+0.7*h),
    path.lineto(x0+0.5*w, y0+1.3*h),
)
c.stroke(p, [deformer.smoothed(0.3)]+grarrow)

y = y0+0.3*h
anyon(x0+0.8*w, y)
anyon(x0+m+1.2*w, y)
    
y = y0+0.7*h
anyon(x0+0.8*w, y)
anyon(x0+m+1.2*w, y)

pop([trafo.rotate(-90), trafo.translate(2.*w+0.8, 2.5*h)])
c.text(2.*w, 0.5*h, "(b)")


# --------------------------------------------------------------------

push()
w1, h1 = w, h
w, h = 2., 2.
#w, h = 1.5, 1.5

N = 20

def dopath(ps, extra=[], fill=False, closepath=True):
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    if fill:
        c.fill(p, [deformer.smoothed(0.3)]+extra+[color.rgb.white])
    c.stroke(p, [deformer.smoothed(0.3)]+extra)

#x0, y0 = 2.8*w + 0*m, -6*m

dx = 0.8*w
dy = 12*m

r = 0.5*h
ys = [0.2*h, 0.7*h, 1.2*h, 1.7*h]


def braid(x0, y0, x1, y1):
    p = path.line(x0, y0, x1, y1)
    c.stroke(p, [color.rgb.white, style.linewidth.THICk])
    c.stroke(p, [red])

def braid(x0, y0, x1, y1):
    x, y = x0, y0
    dx = (x1-x0)/N
    dy = (y1-y0)/N
    ps = [(x, y)]
    for i in range(N):
        theta = i*2*pi/(N)
        x += dx*(cos(theta)+2) / (2.)
        y += dy
        ps.append((x, y))
    dopath(ps, [color.rgb.white, style.linewidth.THICk], closepath=False)
    dopath(ps, [red], closepath=False)



x1, y1 = x0+dx, y0+dy
perm = [2, 0, 1, 3]
for i in [0, 1, 2, 3]:
    braid(x0, y0+ys[i], x1, y1+ys[perm[i]])

#c.text(x0-1.5, 0, "(c)")


y2 = y0+0.95*h
ps = []
for i in range(N):
    theta = 2*pi*i / (N-1)
    ps.append((x0+0.4*r*sin(theta), y2+0.9*r*cos(theta)))

dopath(ps, dotted, fill=True)

ps = []
for i in range(N):
    theta = pi + pi*i / (N-1)
    ps.append((x0+0.5*h*sin(theta), y2+0.9*h*cos(theta)))

y1 = ys[-1]+y0
r1 = ps[-1][1]-y1
for i in range(N):
    theta = pi*i / (N-1)
    ps.append((x0+r1*sin(theta), y1+r1*cos(theta)))

r2 = ps[-1][1]-y2
for i in range(N):
    theta = pi - pi*i / (N-1)
    ps.append((x0-0.5*r2*sin(theta), y2-r2*cos(theta)))

y1 = ys[0]+y0
#r1 = ps[-1][1]-y1
for i in range(N):
    theta = pi*i / (N-1)
    ps.append((x0+r1*sin(theta), y1+r1*cos(theta)))

dopath(ps, dashed, fill=True)

c.stroke(path.line(x0, y0, x0, y0+2*h), grarrow)
for y in ys:
    anyon(x0, y0+y)


# --------------------------------------------------------------------

#c.text(x0+1.2, 0.3*dy, "(d)")

x0 += dx
y0 += dy

c.stroke(path.line(x0, y0, x0, y0+2*h), grarrow)

for y in ys:
    anyon(x0, y0+y)

y2 = y0+0.45*h
ps = []
for i in range(N):
    theta = 2*pi*i / (N-1)
    ps.append((x0+0.4*r*sin(theta), y2+0.8*r*cos(theta)))

dopath(ps, dotted)

y2 = y0+1.45*h
ps = []
for i in range(N):
    theta = 2*pi*i / (N-1)
    ps.append((x0+0.4*r*sin(theta), y2+0.8*r*cos(theta)))

dopath(ps, dashed)

#pop([trafo.rotate(-90)])
pop([trafo.rotate(-90), trafo.translate(2.*w+1.0, 2*h1)])
c.text(4.3*w1, 2*h1, "(c)")
c.text(5.4*w1, 0.5*h1, "(d)")

c.writePDFfile("pic-syndrome.pdf")
c.writeEPSfile("pic-syndrome.eps")

sys.exit(0)

#############################################################################
#
#

def ellipse(x0, y0, rx, ry, extra=[]):
    ps = []
    for i in range(N):
        theta = 2*pi*i / (N-1)
        ps.append((x0+rx*sin(theta), y0+ry*cos(theta)))
    dopath(ps, extra)


def bump(t):
    assert 0.<=t<=1.
    if t<=0.5:
        t1 = 0.5*(2*t)**4
    else:
        t1 = 1.-bump(1.-t)
    assert 0.<=t1<=1., (t, t1)
    return t1

#for i in range(N):
#    t = 1.*i/(N-1)
#    print t, bump(t)


w = 1.3

c = canvas.canvas()

x = 0.
y = 0.
r = 0.5

ps = []
ps.append((x-1.2*r, y))
ps.append((x-1.*r, y))

N = 40
for i in range(N):
    t = 1.*i/(N-1) # 0.0 -> 1.0
    theta = pi*bump(t)
    r1 = (1.-t)*r + t*(0.4*r)
    ps.append((x-r1*cos(theta), y+r1*sin(theta)))

for i in range(N):
    t = 1.*i/(N-1) # 0.0 -> 1.0
    theta = pi*bump(t) + pi
    r1 = t*r + (1.-t)*(0.4*r)
    ps.append((x+r1*cos(theta), y+r1*sin(theta)))

#print ps

ps.append((x+1.*r, y))
ps.append((x+1.2*r, y))
ps.append((x+1.5*r, y))

dopath(ps, grarrow, closepath=False)

#c.stroke(path.line(x-1.2*r, y, x+1.5*r, y), grarrow)
ellipse(x, y, r, r)

anyon(x-0.4*r, 0)
c.text(x-0.3*r, 0.2*r, "$\scriptstyle a$", southwest)
anyon(x+0.4*r, 0)
c.text(x+0.3*r, -0.2*r, "$\scriptstyle b$", northeast)

c.text(x+r, y-r, "$\scriptstyle c$", southwest)

#R_{\mathbb{I}}^{\tau\tau} = \e^{\frac{-4\pi i}{5}} 
#R_\tau^{\tau\tau}= \e^{\frac{3\pi i}{5}} 
#F_{\tau}^{\tau\tau\tau} = \begin{pmatrix}\varphi^{-1}&\varphi^{-\frac{1}{2}}\\\varphi^{-\frac{1}{2}}&-\varphi^{-1}\end{pmatrix} \,,

x += w
#c.text(x, y, r"$= \mathrm{e}^{\frac{-4\pi i}{5}} $", center)
c.text(x, y, r"$= R_c^{ab} $", center)

x += w
c.stroke(path.line(x-1.2*r, y, x+1.5*r, y), grarrow)
ellipse(x, y, r, r)

anyon(x-0.4*r, 0)
c.text(x-0.3*r, 0.3*r, "$\scriptstyle a$", south)
anyon(x+0.4*r, 0)
c.text(x+0.3*r, -0.3*r, "$\scriptstyle b$", north)

c.text(x+r, y-r, "$\scriptstyle c$", southwest)

c.writePDFfile("pic-rmove.pdf")


#############################################################################
#
#

w = 1.0

c = canvas.canvas()

x = 0.
y = 0.
r = 0.5

c.text(x-1.6*r, y, r"$\alpha$", center)
ellipse(x, y+0.1*r, r, 0.7*r)

anyon(x-0.4*r, 0)
c.text(x-0.4*r, 0.3*r, r"$\scriptstyle \tau$", south)
anyon(x+0.4*r, 0)
c.text(x+0.4*r, 0.3*r, r"$\scriptstyle \tau$", south)

c.text(x+r, y-0.5*r, r"$\scriptstyle \mathbb{I}$", southwest)

x += w
c.text(x, y, r"$+\ \beta$", center)

x += w
#c.stroke(path.line(x-1.2*r, y, x+1.5*r, y), grarrow)
ellipse(x, y+0.1*r, r, 0.7*r)

anyon(x-0.4*r, 0)
c.text(x-0.4*r, 0.3*r, r"$\scriptstyle \tau$", south)
anyon(x+0.4*r, 0)
c.text(x+0.4*r, 0.3*r, r"$\scriptstyle \tau$", south)

c.text(x+r, y-0.5*r, r"$\scriptstyle \tau$", southwest)

c.writePDFfile("pic-fibonacci.pdf")


#############################################################################
#
#


w = 2.2

c = canvas.canvas()

x = 0.
y = 0.
r = 0.5


c.stroke(path.line(x-2.0*r, y, x+2.2*r, y), grarrow)
anyon(x-r, y)
c.text(x-r, y+0.25*r, "$\scriptstyle a$", south)
anyon(x, y)
c.text(x, y+0.25*r, "$\scriptstyle b$", south)
anyon(x+r, y)
c.text(x+r, y+0.25*r, "$\scriptstyle c$", south)

ellipse(x-0.5*r, y+0.1*r, 0.9*r, 0.7*r)
c.text(x+0.5*r, y-0.4*r, "$\scriptstyle i$", center)
ellipse(x, y+0.1*r, 1.6*r, 1.0*r)
c.text(x+1.4*r, y-0.9*r, "$\scriptstyle d$", southwest)

x += w

c.text(x+0.1*r, y, "$ = \sum_j[F^{abc}_d]_{ij}$", center)

x += w

c.stroke(path.line(x-2.0*r, y, x+2.2*r, y), grarrow)
anyon(x-r, y)
c.text(x-r, y+0.25*r, "$\scriptstyle a$", south)
anyon(x, y)
c.text(x, y+0.25*r, "$\scriptstyle b$", south)
anyon(x+r, y)
c.text(x+r, y+0.25*r, "$\scriptstyle c$", south)

ellipse(x+0.5*r, y+0.1*r, 0.9*r, 0.7*r)
c.text(x-0.5*r, y-0.4*r, "$\scriptstyle j$", center)
ellipse(x, y+0.1*r, 1.6*r, 1.0*r)
c.text(x-1.4*r, y-0.9*r, "$\scriptstyle d$", southeast)

c.writePDFfile("pic-fmove.pdf")


#############################################################################
#
#

