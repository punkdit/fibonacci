#!/usr/bin/env python

import sys, os

from random import random, seed
from math import *

EPSILON = 1e-8

def _bump(x):

    assert 0.<=x<=1.
    if x<EPSILON:
        return 0.

    A = exp(-1)
    x = 1.-x
    y = exp(-1./(1-x**2))
    y /= A
    assert 0.<=y<=1.+EPSILON
    return y

def bump(x):

    y = 0.5 * (_bump(x) + 1.-_bump(1.-x))

    return y


def bump0(x):
    if abs(x) < 1-EPSILON:
        y = exp(-1./(1-x**2))
    else:
        y = 0.
    return y

for i in range(11):
    v = i/10.
    bump(v)


def c2p(x, y):

    r = sqrt(x**2+y**2)

    if abs(x) > EPSILON:
        theta = atan(y/x)
    elif x<=0:
        if y>=0:
            theta = -pi/2
        else:
            theta = pi/2
    elif y>=0:
        theta = pi/2
    else:
        theta = -pi/2

    if x <= 0:
        if y>=0:
            #print "+pi",
            theta += pi
        else:
            #print "-pi",
            theta -= pi
            
    return r, theta


def p2c(r, theta):

    x = r*cos(theta)
    y = r*sin(theta)

    return x, y


def rnd(r=1.):
    x = (random() * 2 - 1.) * r
    return x

def str(a, b):
    s = "%.2f,%.2f"%(a, b)
    s = s.rjust(11)
    return s

def twist(x, y, phi=0., r1=1., r2=2., x0=0., y0=0.):

    x -= x0
    y -= y0
    r, theta = c2p(x, y)

    assert r2-r1>EPSILON

    if r <= r1:
        theta += phi
    elif r <= r2:
        theta += phi*bump((r2-r)/(r2-r1))

    x, y = p2c(r, theta)

    x += x0
    y += y0
    return x, y


seed(0)

for i in range(10):
    x, y = rnd(), rnd()
    r, theta = c2p(x, y)
    x1, y1 = p2c(r, theta)
    assert abs(x1-x) + abs(y1-y) < EPSILON

    x1, y1 = twist(x, y)
    assert abs(x1-x) + abs(y1-y) < EPSILON

    x1, y1 = twist(x, y, pi/4, 0.2, 0.8)
    assert abs(x1-x) + abs(y1-y) < 1.


#for x in range(-10, 10):
#    x = float(x)
#    x1, y1 = twist(x, 0, pi/8, 2, 8)
#    #print x, 0., x1, y1


for i in range(10):
    x, y = rnd(1e-10), rnd()
    r, theta = c2p(x, y)
    x1, y1 = p2c(r, theta)
    assert abs(x1-x) + abs(y1-y) < EPSILON


import numpy
from PIL import Image

def twist_im(im, x0, y0, phi, r0, r1):
    
    src = numpy.array(im)
    print "source:", src.shape, src.dtype

    w, h = src.shape[:2]

    ijs = []
    for i in range(w):
        for j in range(h):
            ijs.append((i, j))

    if src.shape[2]==4:
        for i, j in ijs:
            if src[i, j, 3] == 0:
                src[i, j] = (255, 255, 255, 255)
        src = src[:, :, :3]

    assert src.shape == (w, h, 3)
    target = numpy.empty((w, h, 3), dtype=src.dtype)

    target[:] = 0

    for i, j in ijs:

        x, y = 2.*j/w - 1., 2.*i/h - 1.
        x -= x0
        y -= y0
        #y *= 2
        x, y = twist(x, y, phi, r0, r1)
        #y /= 2
        x += x0
        y += y0
        j1, i1 = (x+1.)*w/2., (y+1.)*h/2.
        #print (i, j), (x, y), (i1, j1),
        i1, j1 = int(round(i1)), int(round(j1))
        #print (i1, j1)

        target[i, j] = src[i1, j1][:4]

    im = Image.fromarray(target)

    return im


def main(name):
    
    image = Image.open(name)
    
    #a = numpy.fromstring(s, dtype=numpy.uint8)
    src = numpy.array(image)
    print src.shape, src.dtype

    w, h = src.shape[:2]

    ijs = []
    for i in range(w):
        for j in range(h):
            ijs.append((i, j))

    for i, j in ijs:
        if src[i, j, 3] == 0:
            src[i, j] = (255, 255, 255, 255)
    src = src[:, :, :3]

    assert src.shape == (w, h, 3)
    target = numpy.empty((w, h, 3), dtype=src.dtype)

    N = 240
    for frame in range(N):

        phi = pi*frame/(N-1)
        target[:] = 0

        for i, j in ijs:

            x, y = 2.*i/w - 1., 2.*j/h - 1.
            x, y = twist(x, y, phi, 0.2, 0.8)
            i1, j1 = (x+1.)*w/2., (y+1.)*h/2.
            #print (i, j), (x, y), (i1, j1),
            i1, j1 = int(round(i1)), int(round(j1))
            #print (i1, j1)

            target[i, j] = src[i1, j1][:4]

        image = Image.fromarray(target)
        stem = 'frames/%.4d'%frame
        image.save(stem+".png", "PNG")
        print phi, stem

        #break


def main_pov():

    header = """
camera{location <10., -10., 15.0> up <0,0,1> right <0,1,0> look_at <%f, %f, %f>}
//camera{location <0., 15., 7.5> up <0,0,1> right <1,0,0> direction <0,-1,0>}
light_source{<20., 5., 8.> <1, 1, 1>}
light_source{<210, 10, 0> <1, 1, 1>}
light_source{<-210, -10, 0> <1, 1, 1>}
    """

    sweep = """
sphere_sweep {
    cubic_spline
    6,
    <-4, -5, 0>, 1 <-5, -5, 0>, 1 <-5,  5, 0>, 1.  < 5, -5, 0>, 1.  < 5,  5, 0>, 1 < 4,  5, 0>, 1
    tolerance 0.5
 texture{ pigment{ color<0.5, 1., 1., 0, 0.> } finish{     phong 0.7 }} 
 }
    """

    (x0, y0), (x1, y1) = (-1., 0), (+1., 0)
    sweeps = [[(x0, y0)], [(x1, y1)]]
    sweeps = [[], []]

    SLICES = 100

    for i in range(SLICES/2):
        sweeps[0].append((x0, y0))
        sweeps[1].append((x1, y1))

    for i in range(2*SLICES):
        v = 1.*i/(2*SLICES-1)
        #phi = 2*pi*v
        phi = 2*pi*bump(v)

        x, y = twist(x0, y0, phi, 1.5, 2.)
        sweeps[0].append((x, y))

        x, y = twist(x1, y1, phi, 1.5, 2.)
        sweeps[1].append((x, y))

        #print phi, x, y

    for i in range(SLICES/2):
        sweeps[0].append((x0, y0))
        sweeps[1].append((x1, y1))

    dz = 5. / SLICES
    radius = 0.1

    look_at = (
        sum([1.*x for (x, y) in sweeps[0]])/len(sweeps[0]),
        sum([1.*y for (x, y) in sweeps[0]])/len(sweeps[0]),
        dz*len(sweeps[0])/2)

    look_at = (0, 0, dz*len(sweeps[0])/2)

    #FRAMES = 240
    FRAMES = SLICES

    commands = []

    for frame in range(FRAMES):
        stem = 'frames/%.4d'%frame
        f = open(stem+'.pov', 'w')
        print >>f, header % look_at
    
        #z = 0.
        n = 2 + 1.*frame*len(sweeps[0]) / FRAMES

        for sweep_i in [0, 1]:

            color = "texture{ pigment{ color<0.5, 1., 1., 0, 0.> } finish{ phong 0.7 }} "
            sweep = sweeps[sweep_i]
            sweep = sweep[:int(n)]
            assert len(sweep)>=2

            s = ' '.join("<%f, %f, %f>, %f" % (x, y, i*dz, radius) for i, (x, y) in enumerate(sweep))

            if len(sweep)>=4:
                # need 4 points for cubic_spline
                print >>f, "sphere_sweep { cubic_spline %d, %s tolerance 0.1 %s }" % (
                    len(sweep), s, color)

            color = "texture{ pigment{ color<1.0, 0.5, 1., 0, 0.> } finish{ phong 0.7 }} "
            (x, y) = sweep[-2]
            i = len(sweep)-2
            print >>f, "sphere{ <%f, %f, %f>, %s %s }" % (
                x, y, i*dz, 2*radius, color)

        color = "texture{ pigment{ color<1.0, 0.0, 0.5, 0, 0.5> } finish{ phong 0.7 }} "
        v = 2.0
        x, y = 0., 0.
        print >>f, "polygon{ 5 <%f, %f, %f>, <%f, %f, %f>, <%f, %f, %f>, <%f, %f, %f>, <%f, %f, %f> %s }" % (
            x-v, y-v, i*dz,
            x+v, y-v, i*dz,
            x+v, y+v, i*dz,
            x-v, y+v, i*dz,
            x-v, y-v, i*dz,
            color)

        f.close()

        #WIDTH, HEIGHT = 200, 200
        #cmd = "povray +A %s.pov -W%d -H%d +O%s.png" % (stem, WIDTH, HEIGHT, stem)
        #os.system(cmd)

        WIDTH, HEIGHT = 600, 600
        stem = '%.4d'%frame
        cmd = "povray +A %s.pov -W%d -H%d" % (stem, WIDTH, HEIGHT)
        print cmd
        commands.append(cmd)
        #break

    #print >>f, sweep

    commands.append("wait")

    commands.append("ffmpeg -y -r 5 -i %4d.png -b 4096k -r 5 animation.avi")

    f = open('frames/build.sh', 'w')
    print >>f, "#!/bin/sh"
    for i, cmd in enumerate(commands):
        if (i+1)%20:
            cmd += '&'
        print >>f, cmd
    f.close()
    #os.chmod('frames/build.sh', 777)

    system('chmod +x frames/build.sh')
    system('tar zcf frames.tgz frames')
    system('scp frames.tgz cartman:braid')

    system('ssh cartman "cd braid; rm -r frames; tar zxf frames.tgz; cd frames; nohup ./build.sh&"')


def system(cmd):
    print cmd
    r = os.system(cmd)
    assert r==0, r
    return r

if __name__ == "__main__":

    #name = sys.argv[1]
    #main(name)

    main_pov()



