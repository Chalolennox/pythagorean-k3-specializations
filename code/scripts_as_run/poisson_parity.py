import numpy as np, math
from scipy.optimize import minimize
# factored members: (orbit, n, digits of N, omega, W observed)
data=[('nP',2,5,2,-1),('nP',3,10,2,-1),('nP',4,18,2,-1),('nP',5,29,3,-1),('nP',6,41,4,1),('nP',7,55,4,1),('nP',8,73,4,-1),('nP',9,91,5,1),('nP',12,163,7,-1),
      ('T',2,3,1,1),('T',3,10,3,-1),('T',4,16,2,-1),('T',5,27,2,-1),('T',6,39,3,-1),('T',7,56,5,1),('T',8,71,4,-1),('T',9,91,4,1),('T',10,113,5,1),('T',11,135,6,-1)]
eps=lambda orb,n: (1 if n%6 in (0,1,5) else -1) if orb=='nP' else (1 if n%3==0 else -1)
n_=np.array([d[1] for d in data]);dig=np.array([d[2] for d in data]);om=np.array([d[3] for d in data])
L=np.log(dig*math.log(10))                      # ln ln N
# Poisson regression  mu = exp(b0 + b1*lnlnN)   (and, for comparison, mu = c*lnlnN)
def nll(b):
    mu=np.exp(b[0]+b[1]*L); return -np.sum(om*np.log(mu)-mu-np.array([math.lgamma(o+1) for o in om]))
r=minimize(nll,[0.0,1.0]);b0,b1=r.x
mu=np.exp(b0+b1*L)
print("fit: mu = exp(%.3f + %.3f ln ln N);  mean omega %.2f, variance of omega %.2f (Poisson would be equal)"%(b0,b1,om.mean(),om.var()))
print("  fitted mu vs observed omega:",[(int(n),round(float(m),1),int(o)) for n,m,o in zip(n_,mu,om)][:8],"...")
# model for a_n = (-1)^omega (all exponents 1): P(a=+1) = (1+exp(-2 mu))/2
pa=(1+np.exp(-2*mu))/2
epsv=np.array([eps(d[0],d[1]) for d in data])
pW=np.where(epsv==1,pa,1-pa)                       # P(W=+1)
Wobs=np.array([d[4] for d in data]); aobs=Wobs*epsv
print("\nbias of the parity: P(a=+1)-1/2 for n=2..12:",{int(n):round(float(p-0.5),4) for n,p in zip(n_,pa)})
print("P(W=+1) per member:",[round(float(p),3) for p in pW])
# exact Poisson-binomial distribution of the number of positive W
def pb(ps):
    dist=np.array([1.0])
    for p in ps: dist=np.convolve(dist,[1-p,p])
    return dist
dist=pb(pW);dist_fair=pb(np.full(len(pW),0.5));k=int((Wobs==1).sum())
print("\nobserved positives:",k,"of",len(data))
print("  Poisson-parity model: expected %.2f, P(X<=%d)=%.3f, P(X>=%d)=%.3f"%(pW.sum(),k,dist[:k+1].sum(),k,dist[k:].sum()))
print("  fair-coin model     : expected %.2f, P(X<=%d)=%.3f, P(X>=%d)=%.3f"%(9.5,k,dist_fair[:k+1].sum(),k,dist_fair[k:].sum()))
# log-likelihood of the observed parity sequence a_n
ll_p=np.sum(np.where(aobs==1,np.log(pa),np.log(1-pa)));ll_f=len(data)*math.log(0.5)
print("\nlog-likelihood of observed (-1)^omega signs: Poisson-parity %.3f, fair coin %.3f (difference %.3f; %d of %d have a=+1)"%(ll_p,ll_f,ll_p-ll_f,int((aobs==1).sum()),len(data)))
# extrapolation of mu and of the bias, and expected number of rank>=2 members up to N
def mu_of(n):
    digits=0.0
    # digits of N_n ~ 1.13 n^2 (measured: 163 at n=12)
    digits=1.13*n*n
    return math.exp(b0+b1*math.log(digits*math.log(10)))
print("\nextrapolated mean number of prime factors and parity bias:")
for n in (2,5,12,20,30,50,100):
    m=mu_of(n);print("   n=%3d: mu=%.2f  bias P(a=+1)-1/2 = %.2e"%(n,m,(math.exp(-2*m))/2))
print("\nexpected number of members with W=+1 (rank>=2) for n=2..N, both orbits, refined model vs fair coin:")
for N in (12,20,30,50):
    tot=0.0
    for orb in ('nP','T'):
        for n in range(2,N+1):
            m=mu_of(n);p=(1+math.exp(-2*m))/2
            tot+= p if eps(orb,n)==1 else 1-p
    print("   N=%2d: refined %.2f   fair %.1f"%(N,tot,(N-1)))
