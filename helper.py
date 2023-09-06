import scipy.sparse as sp
import matplotlib.pylab as plt
from ngsolve import *
from netgen.csg import *
from netgen.meshing import MeshingStep
from ngsolve.webgui import Draw

def ShowPattern(A,precision=-1,binarize=False):
    rows_all,cols_all,vals_all = A.COO()
    for i,(r,c,v) in enumerate(zip(rows_all,cols_all,vals_all)):
        vals_all[i] = abs(vals_all[i])
        if binarize and vals_all[i] > precision:
            vals_all[i] = 1.0
    minval = 0
    maxval = max(vals_all)
    A_all = sp.csr_matrix((vals_all,(rows_all,cols_all)),shape=(A.height,A.width))
    plt.figure(figsize=(6,6*A.width/A.width))
    plt.imshow(A_all.todense(),interpolation='none',cmap='jet',vmin=minval,vmax=maxval)
    plt.show()

def generate_sphere_mesh(maxh, order_g = 1, center=Pnt(0,0,0), r = 1.0):
    geo          = CSGeometry()
    sphere       = Sphere(center, r)
    geo.Add(sphere)
    mesh = Mesh(geo.GenerateMesh(maxh=maxh, optsteps2d=3, perfstepsend=MeshingStep.MESHSURFACE))
    mesh.Curve(order_g)
    return mesh

# TODO: Other possibilities to generate
def generate_torus_mesh(maxh, order_g = 1, center=Pnt(0,0,0), R = 1.0, r = 0.4):
    spline = SplineCurve2d()
    R = 1
    r = 0.4
    eps = r*1e-8

    # define the control points
    pnts = [ (0,R-r), (-r+eps,R-r+eps), (-r,R),
            (-r+eps,R+r-eps), (0,R+r), (r-eps,R+r-eps), (r,R), (r-eps,R-r+eps) ]
    # define the splines using the control points
    segs = [ (0,1,2), (2,3,4), (4,5,6), (6,7,0) ]

    # add the points and segments to the spline
    for pnt in pnts:
        spline.AddPoint (*pnt)

    for seg in segs:
        spline.AddSegment (*seg)

    rev = Revolution(Pnt(0,0,-1), Pnt(0,0,1), spline)
    geo = CSGeometry()
    geo.Add(rev.col([1,0,0]))

    mesh = geo.GenerateMesh(maxh=maxh, optsteps2d=3, perfstepsend=MeshingStep.MESHSURFACE)
    mesh = Mesh(mesh)
    mesh.Curve(order_g)	
    return mesh 