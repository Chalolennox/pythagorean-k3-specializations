"""Reproduce DE_BRUIJN_WALSH_DISTRIBUTION.md.
Python 3.10+; dependency: sympy. Run python code/verify/pr92_walsh_distribution.py.
Input residues are from the owner Magma run, not independently certified here.
"""
from math import gcd,lcm
from fractions import Fraction as F
from sympy import n_order
rows=[(2131,1031,[388,643]),(5779,2903,[1286,1617]),(6907,1151,[6,1145]),(10321,2589,[639,874,1715,1950]),(12907,6465,[810,5655]),(13763,6959,[240,6719]),(18797,9404,[2600,6804]),(23747,11783,[3037,8746]),(40841,10247,[4507,5740]),(46933,23492,[1344,2872,20620,22148]),(47657,11927,[5069,6858]),(47701,23708,[714,9644,14064,22994]),(52883,26343,[11592,14751]),(54517,27256,[3244,5520,21736,24012]),(72883,36479,[9393,27086]),(77347,38711,[5713,32998])]
def crt(u,r,v,s):
 g=gcd(r,s)
 if (v-u)%g:return None
 return (u+r*((v-u)//g*pow(r//g,-1,s//g)%(s//g)))%lcm(r,s)
def intersect(A,B):
 r,a,b,x,y=A;s,c,d,u,v=B
 Y=crt(y,b,v,d)
 if Y is None:return None
 L=lcm(b,d);g=gcd(r,s)
 X=x-a*((Y-y)//b);U=u-c*((Y-v)//d)
 h=(a*(L//b)-c*(L//d));q=gcd(h,g)
 if (X-U)%q:return None
 k=((X-U)//q*pow(h//q,-1,g//q))%(g//q)
 Y+=L*k; Bnew=L*(g//q)
 X=crt(x-a*((Y-y)//b),r,u-c*((Y-v)//d),s)
 anew=crt(a*(Bnew//b),r,c*(Bnew//d),s)
 return lcm(r,s),anew,Bnew,X,Y

def local(n,d,z):
 g=gcd(n,d);e=d//g;r=int(n_order(2,e));powers={pow(2,i,e):i for i in range(r)};b=1
 while pow(3,b,e) not in powers:b+=1
 a=powers[pow(3,b,e)];targets={v//g*pow(n//g,-1,e)%e for v in z if v%g==0};hits=[]
 for j in range(b):
  for t in targets:
   u=t*pow(pow(3,j,e),-1,e)%e
   if u in powers:hits.append((powers[u],j))
 if not hits:return None
 assert len(hits)==1
 x,y=hits[0];out=[]
 for i,j in [(0,0),(1,0),(0,1),(1,1)]:
  Y=(y-j)%b;X=(x-i-a*((Y-(y-j))//b))%r;out.append((r,a,b,X,Y))
 return out

def calc(block,w):
 # accumulate integer coefficients by intersection coset, then sum densities
 D={(1,0,1,0,0):1}
 for p,cs in block:
  E=D.copy()
  for A,c in D.items():
   for i,B in enumerate(cs):
    if w & (8>>i):
     C=intersect(A,B)
     if C is not None:E[C]=E.get(C,0)-2*c
  D={A:c for A,c in E.items() if c}
 return sum((F(c,A[0]*A[2]) for A,c in D.items()),F(0))
for n in [72,360,2520]:
 data=[(p,local(n,d,z)) for p,d,z in rows];data=[(p,c) for p,c in data if c];blocks=[]
 while data:
  block=[data.pop()];changed=True
  while changed:
   changed=False
   for item in data[:]:
    if any(gcd(item[1][0][0]*item[1][0][2],c[0][0]*c[0][2])>1 for p,c in block):block.append(item);data.remove(item);changed=True
  blocks.append(block)
 W=[F(1)]*16
 for block in blocks:
  for w in range(1,16):W[w]*=calc(block,w)
  print(n,'block',[p for p,c in block],flush=True)
 M=[sum(((-1)**((w&k).bit_count())*W[w] for w in range(16)),F(0))/16 for k in range(16)]
 assert sum(M)==1 and min(M)>0
 print('RESULT',n,[float(x) for x in M], 'odd',float((1-W[8])/2),'corr',*[float(W[w]) for w in [12,10,15]],flush=True)
 print('EXACT MASSES',n,[str(x) for x in M],flush=True)
