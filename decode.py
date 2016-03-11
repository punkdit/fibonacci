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


def anyon(x, y, r=0.07):
    c.fill(path.circle(x, y, r), [white])
    c.stroke(path.circle(x, y, r), [red, style.linewidth.thick])


N = 20

def dopath(ps, extra=[], fill=False, closepath=True):
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    if fill:
        c.fill(p, [deformer.smoothed(0.3)]+extra+[color.rgb.white])
    c.stroke(p, [deformer.smoothed(0.3)]+extra)

def ellipse(x0, y0, rx, ry, extra=[], fill=False):
    ps = []
    for i in range(N):
        theta = 2*pi*i / (N-1)
        ps.append((x0+rx*sin(theta), y0+ry*cos(theta)))
    dopath(ps, extra, fill)


#############################################################################
#
#

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

from qupy.ldpc.solve import parse
from qupy.braid.tree import Tree

l = 8
w, h = 0.8, 0.8
m = 0.05


if 1:
    seed(2)
    syndrome = numpy.zeros((l, l), dtype=numpy.int32)
    
    for count in range(10):
      if random()<0.5:
        i = randint(0, l-2)
        j = randint(0, l-1)
        syndrome[i, j] += 1
        syndrome[i+1, j] += 1
      else:
        # horizontal
        i = randint(0, l-1)
        j = randint(0, l-2)
        syndrome[i, j] += 1
        syndrome[i, j+1] += 1
    
    for i in range(l):
      for j in range(l):
        if syndrome[i,j]>1:
          if random()<0.5:
            syndrome[i,j]=0
          else:
            syndrome[i,j]=1

else:
    syndrome = parse("""
........
........
...1....
...1....
..1.....
........
.11.....
........
""")

#print syndrome

syndrome = syndrome[1:, :7]
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


def draw(dx=0., dy=0., use_arrows=True):

    r = 4.*m
    syndrome1 = syndrome.copy()
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
        #syndrome1[p0] = 0
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

    if use_arrows:
      for (p0, p1) in lines:
        x0, y0 = coord(*p0)
        x1, y1 = coord(*p1)
        syndrome1[p0] = 0
        c.stroke(path.line(x0+dx, y0+dy, x1+dx, y1+dy),
            [style.linewidth.Thick, deco.earrow(size=0.3)])

    for i, j in sites:
        c.stroke(path.rect(j*w+dx, i*h+dy, w-2*m, h-2*m))
        if syndrome[i,j]:
            x, y = coord(i, j)
            anyon(x+dx, y+dy, 0.1*w)

    syndrome[:] = syndrome1



trees = [Tree(site) for site in sites if syndrome[site]] # <----------

c = canvas.canvas()
draw(0., 0.)
c.writePDFfile("pic-decode-0.pdf")

join1(trees) # <----------

c = canvas.canvas()
draw(0., 0.)
c.writePDFfile("pic-decode-1.pdf")

print syndrome
syndrome[6, 0] = 0
syndrome[2, 2] = 0
print [len(t) for t in trees]

c = canvas.canvas()
draw(0., 0., False)
c.writePDFfile("pic-decode-2.pdf")

trees.pop()
trees.pop(3)

grow(trees) # <----------
join(trees) # <----------

c = canvas.canvas()
draw(0., 0.)
c.writePDFfile("pic-decode-3.pdf")


code = \
"""
def decode():
    syndrome = get_syndrome()
    
    # build a cluster for each charge
    clusters = [Cluster(charge) for charge in syndrome]

    # join any neighbouring clusters
    join(clusters, 1)
    
    while clusters:
    
        # find total charge on each cluster
        for cluster in clusters:
            fuse_cluster(cluster)
    
        # discard vacuum clusters
        clusters = [cluster for cluster in clusters if non_vacuum(cluster)]
    
        # grow each cluster by 1 unit
        for cluster in clusters:
            grow_cluster(cluster, 1)
    
        # join any intersecting clusters
        join(clusters, 0)

    # success !
    return True
""".split('\n')
code = code[1:-1]

for i, line in enumerate(code):
    print "%2d:  %s"%(i+1, line)



