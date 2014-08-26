#!/usr/bin/env python

import sys
import os
import Image
import numpy


def write(c):
    sys.stdout.write(c)
    sys.stdout.flush()


def flat(im):

    a = numpy.array(im)
    shape = a.shape
    m, n, _ = shape
    
    for i in range(m):
      for j in range(n):
    
        v = a[i, j]
    
        vs = v.sum()
        va = vs / 3
        vd = ((v-va)**2/3.).sum()**0.5
    
        if va > 200:
    
            a[i, j] = [255, 255, 255]
            #write('.')
    
        elif va>50 and vd>20:
            a[i, j] = [0, 0, 0] # switch colour to black
    
        elif 1:
    
            continue
    
        elif va < 50:
    
            a[i, j] = [0, 0, 0]
    
        elif vd > 20.:
    
            a[i, j] = [255, 0, 0]
    
        else:
            a[i, j] = [0, 0, 0]
    
            #print "%.1f"%va,
            #print "%.0f"%vd,
    
            #vm = 1.*max(v)
            #r = 255. / vm
            #a[i, j] = r*v
    
      write('.')
    write('\n')

    im = Image.fromarray(a)

    return im


def pick(im):

    a = numpy.array(im)
    shape = a.shape
    m, n, _ = shape
    
    for i in range(m):
      for j in range(n):
    
        v = a[i, j]
    
        vs = v.sum()
        va = vs / 3
        vd = ((v-va)**2/3.).sum()**0.5
    
        if va > 200:
            a[i, j] = [255, 255, 255]
    
        elif va>50 and vd>20:
            a[i, j] = [0, 0, 0] # switch colour to black
    
        else:
            a[i, j] = [255, 255, 255] # whiteout
    
      write('.')
    write('\n')

    im = Image.fromarray(a)

    return im


def null(im):
    return None


def eps_setcolor(name, r, g, b):
    s = open(name).read()
    s = s.replace('0 setgray', '%.2f %.2f %.2f setrgbcolor' % (r, g, b))
    open(name, 'w').write(s)


def eps_split(name):

    f = open(name)

    header = []
    body = []
    footer = []

    lno = 0
    while lno < 8:

        lno += 1
        line = f.readline()
        header.append(line)
    header = ''.join(header)

    line = f.readline()
    while not line.startswith("%%EOF"):
        body.append(line)
        line = f.readline()

    body = ''.join(body)

    footer = line

    return header, body, footer


def eps_cat(name1, name2, output):

    h1, b1, foot = eps_split(name1)
    h2, b2, foot = eps_split(name2)

    f = open(output, 'w')
    f.write(h1)
    f.write(b1)
    f.write(b2)
    f.write(foot)

    f.close()


funcname = sys.argv[1]

if funcname == 'cat':

    args = sys.argv[2:]
    eps_cat(*args)

elif funcname == 'trace':

    name = sys.argv[2]
    stem = '.'.join(name.split('.')[:-1])
    
    name_png = "%s.png" % (stem,)
    name_pnm = "%s.pnm" % (stem,)
    name_eps = "%s.eps" % (stem,)
    
    cmd = 'pngtopnm %s > %s' % (name_png, name_pnm)
    print cmd
    os.system(cmd)
    
    cmd = 'potrace -e -q -c %s' % (name_pnm)
    print cmd
    os.system(cmd)
    
    r, g, b = 1., 0.5, 0.5

else:
    func = eval(funcname)
    
    name = sys.argv[2]
    stem = '.'.join(name.split('.')[:-1])
    
    im = None
    im = Image.open(name)
    im = func(im)
    
    name_png = "%s-%s.png" % (stem, funcname)
    name_pnm = "%s-%s.pnm" % (stem, funcname)
    name_eps = "%s-%s.eps" % (stem, funcname)
    
    if im is not None:
        print "\nsaving", name_png
        im.save(name_png)
    
    cmd = 'pngtopnm %s > %s' % (name_png, name_pnm)
    print cmd
    os.system(cmd)
    
    cmd = 'potrace -e -q -c %s' % (name_pnm)
    print cmd
    os.system(cmd)
    
    r, g, b = 1., 0.5, 0.5







