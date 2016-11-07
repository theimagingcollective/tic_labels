import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import nibabel as nib


def randrange(n, vmin, vmax):
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
data=[]
nPts=[]
boxEdge=200
pts=np.zeros([boxEdge,boxEdge,boxEdge])
com=np.array([0,0,0])
#generate coordinates of points
for c, m, center,edgeLen in [('r', 'o', [50,100,100], 30), ('b', '^',[60,110,110],15)]:

    nPts.append(edgeLen**3)
    xr = range(center[0]-int(edgeLen/2),center[0]+int(edgeLen/2+0.5))
    yr = range(center[1]-int(edgeLen/2),center[1]+int(edgeLen/2+0.5))
    zr = range(center[2]-int(edgeLen/2),center[2]+int(edgeLen/2+0.5))
    xs,ys,zs=np.meshgrid(xr,yr,zr)
    ax.scatter(xs, ys, zs, c=c, marker=m)
    for i in xr:
        for j in yr:
            for k in zr:
                if not pts[i,j,k]:
                    com+=[i,j,k]
                    pts[i,j,k]=1



ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
#plt.title('%d and %d points in each regions. But they overlaps.'%(nPts[0],nPts[1]))
plt.show()

totalPts=int(np.sum(pts[pts>0]))
print ('There should be %d points'%totalPts)
print ('com should be',np.round(com/totalPts))
niiImg = nib.Nifti1Image(pts, affine=np.eye(4))
nib.save(niiImg, '3Dcubes.nii.gz')
