// Scan of the orbits of P and P+T on y^2 = x^3 - 2x^2 + 2x modulo every prime 5 <= p <= LIMIT (second argument: lower bound): reports, for each gap 1..12, the (prime, branch) pairs
// with two qualifying indices at that gap (notes/REVIEW_2026-11-17_gap_k_classification.md; output in data/gap_coincidences_p300000.txt; not in CI). gcc -O2 -o scan_gaps scan_gaps.c
// brute-force scan: for every prime 5 <= p <= LIMIT, walk the orbits of P and P+T, mark qualifying indices,
// report gap-one, gap-two and gap-three coincidences (cyclic mod the order of P).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define KMAX 12
typedef long long ll; typedef unsigned long long ull;
static ll P_;
static ll inv(ll a, ll p){ ll t=0,nt=1,r=p,nr=((a%p)+p)%p; while(nr){ ll q=r/nr, x; x=t-q*nt; t=nt; nt=x; x=r-q*nr; r=nr; nr=x;} if(t<0)t+=p; return t; }
static ll pw(ll b, ll e, ll p){ ll r=1; b%=p; while(e){ if(e&1) r=(__int128)r*b%p; b=(__int128)b*b%p; e>>=1;} return r; }
static int leg(ll a, ll p){ a%=p; if(a<0)a+=p; if(!a) return 0; return pw(a,(p-1)/2,p)==1?1:-1; }
static int qualifies(ll x, ll p){
  ll t=((1-x)%p+p)%p;
  ll t2=t*t%p, t4=t2*t2%p, t6=t4*t2%p;
  ll f=((t6-30*t4%p-24*t2%p-1)%p+2*p)%p; if(f) return 0;
  ll d=(1+t2)%p; if(!d) return 0;
  ll d2=d*d%p;
  ll q=(2*t%p)*(((1-t2)%p+p)%p)%p*inv(d2,p)%p;
  ll r=(((1-t)%p+p)%p)*d%p;
  if(leg(q,p)!=1||leg(r,p)!=1) return 0;
  if(leg(2,p)==1 && leg(1-t,p)!=1) return 0;
  return 1;
}
int main(int argc,char**argv){
  ll LIM=atoll(argv[1]); ll LO=argc>2?atoll(argv[2]):5;
  char *comp=calloc(LIM+1,1); for(ll i=2;i*i<=LIM;i++) if(!comp[i]) for(ll j=i*i;j<=LIM;j+=i) comp[j]=1;
  ll nprimes=0; ll hits[40]={0}; char *mark=malloc(LIM*2+2000);
  for(ll p=LO;p<=LIM;p++){ if(comp[p]) continue; nprimes++;
    for(int eps=0;eps<2;eps++){
      // walk orbit: index n -> nP + eps T
      ll m=0; int inf=0; ll x=0,y=0; // current point
      // start point
      if(eps){ x=0;y=0; inf=0; } else { inf=1; }
      memset(mark,0,2*p+1000);
      ll sx=x, sy=y; int sinf=inf;
      for(;;){
        if(!inf && qualifies(x,p)) mark[m]=1;
        m++;
        // add P=(1,1)
        if(inf){ x=1; y=1; inf=0; }
        else {
          ll lam;
          if(x==1){ if((y+1)%p==0){ inf=1; } else { lam=((3*x%p*x-4*x+2)%p+p)%p*inv(2*y%p,p)%p; goto have; } }
          else { lam=((1-y)%p+p)%p*inv(((1-x)%p+p)%p,p)%p; // (y2-y1)/(x2-x1) with P2=(1,1): (1-y)/(1-x)
          have: { ll x3=((lam*lam+2-x-1)%p+p)%p; ll y3=((lam*((x-x3)%p+p)%p-y)%p+p)%p; x=x3; y=y3; } }
        }
        if(inf==sinf && (inf || (x==sx&&y==sy))) break;
      }
      for(int g=1;g<=KMAX;g++){ int found=0;
        for(ll n=0;n<m;n++) if(mark[n] && mark[(n+g)%m]){ found=1; printf("gap %d: p=%lld branch %d n=%lld order %lld trivial %d\n",g,p,eps,n,m,(int)(g%m==0)); break; }
        hits[g]+=found; }
    }
  }
  printf("primes scanned: %lld (%lld..%lld)\n",nprimes,LO,LIM); for(int g=1;g<=KMAX;g++) printf("gap %d: %lld (prime,branch) pairs\n",g,hits[g]);
  return 0;
}
