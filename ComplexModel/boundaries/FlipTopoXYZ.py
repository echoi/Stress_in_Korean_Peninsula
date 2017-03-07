#!/bin/env python

fi = open("Topo_flipped.xyz","r")
fo = open("Topo.xyz","w")

nx = 51
ny = 41

lines = fi.readlines()
for j in range(ny):
    for i in range(nx):
        n = i + nx*(ny-j-1)
        x,y,z = lines[n].split()
        print >> fo, "%s %.1f %s" % (x,float(y)-36.0,z)

fi.close()
fo.close()
