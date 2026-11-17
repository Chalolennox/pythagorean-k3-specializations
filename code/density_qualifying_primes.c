/* Density of the primes with a qualifying root (F.57): for each prime 5 <= p < LIM, find the roots of f(a) = a^6 - 30a^4 - 24a^2 - 1 in F_p and test the qualifying conditions.
 * Build: gcc -O2 -o dens density_qualifying_primes.c     Run: ./dens 100000000   (about 3 minutes; not part of CI).  Prints the empty fraction overall and by p mod 8.
 * Reproduces the counts 2260 / 348 for p <= 20000 and, for p < 10^8, 0.84905 (overall), 0.89632 (p = +-1 mod 8), 0.80178 (p = +-3 mod 8). */
// For each prime 5<=p<LIM: roots of H(a)=a^6-30a^4-24a^2-1 in F_p; qualifying root (dossier definition):
//   q=2a(1-a^2)/(1+a^2)^2, r=(1-a)(1+a^2) nonzero squares, and 1-a a square if (2/p)=+1.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64; typedef long long i64;
static u64 p;
#define MAXD 8
typedef struct { int d; u64 c[MAXD+1]; } poly;   // d=-1 zero poly
static u64 mulm(u64 a,u64 b){ return a*b%p; }
static u64 powm(u64 a,u64 e){ u64 r=1; a%=p; while(e){ if(e&1) r=r*a%p; a=a*a%p; e>>=1;} return r; }
static u64 invm(u64 a){ return powm(a,p-2); }
static void norm(poly*f){ while(f->d>=0 && f->c[f->d]==0) f->d--; }
static poly pmodp(poly a, poly b){ // a mod b
  norm(&a); norm(&b); u64 il=invm(b.c[b.d]);
  while(a.d>=b.d && a.d>=0){ u64 f=a.c[a.d]*il%p; int s=a.d-b.d; for(int i=0;i<=b.d;i++){ a.c[i+s]=(a.c[i+s]+p-f*b.c[i]%p)%p; } norm(&a); }
  return a; }
static poly pgcd(poly a, poly b){ norm(&a); norm(&b); while(b.d>=0){ poly r=pmodp(a,b); a=b; b=r; } if(a.d>=0){ u64 il=invm(a.c[a.d]); for(int i=0;i<=a.d;i++) a.c[i]=a.c[i]*il%p; } return a; }
static poly pmulmod(poly a, poly b, poly m){ poly r; r.d=a.d+b.d; memset(r.c,0,sizeof r.c);
  // use temp big array
  u64 t[2*MAXD+2]; memset(t,0,sizeof t);
  for(int i=0;i<=a.d;i++) for(int j=0;j<=b.d;j++) t[i+j]=(t[i+j]+a.c[i]*b.c[j])%p;
  poly x; x.d=a.d+b.d; if(x.d>2*MAXD) x.d=2*MAXD; memset(x.c,0,sizeof x.c);
  // reduce by m (make monic first)
  u64 il=invm(m.c[m.d]);
  for(int k=a.d+b.d;k>=m.d;k--){ u64 f=t[k]*il%p; if(f){ for(int i=0;i<=m.d;i++) t[k-m.d+i]=(t[k-m.d+i]+p-f*m.c[i]%p)%p; } }
  poly out; out.d=m.d-1; memset(out.c,0,sizeof out.c); for(int i=0;i<m.d;i++) out.c[i]=t[i]; norm(&out); return out; }
static poly ppowmod(poly base, u64 e, poly m){ poly r; r.d=0; memset(r.c,0,sizeof r.c); r.c[0]=1; while(e){ if(e&1) r=pmulmod(r,base,m); base=pmulmod(base,base,m); e>>=1; } return r; }
static int roots_of(poly g, u64 *out, int cnt){ // g monic squarefree, splits completely over F_p
  if(g.d==0) return cnt; if(g.d==1){ out[cnt++]=(p-g.c[0])%p; return cnt; }
  for(;;){ u64 s=(u64)rand()%p; poly x; x.d=1; memset(x.c,0,sizeof x.c); x.c[0]=s; x.c[1]=1;
    poly w=ppowmod(x,(p-1)/2,g); if(w.d<0){ w.d=0; w.c[0]=0; } w.c[0]=(w.c[0]+p-1)%p; norm(&w);
    poly h=pgcd(g,w); if(h.d>0 && h.d<g.d){ // split
      // quotient g/h
      poly q; q.d=g.d-h.d; memset(q.c,0,sizeof q.c); poly r=g; u64 il=invm(h.c[h.d]);
      for(int k=g.d;k>=h.d;k--){ u64 f=r.c[k]*il%p; q.c[k-h.d]=f; for(int i=0;i<=h.d;i++) r.c[k-h.d+i]=(r.c[k-h.d+i]+p-f*h.c[i]%p)%p; }
      norm(&q); u64 ilq=invm(q.c[q.d]); for(int i=0;i<=q.d;i++) q.c[i]=q.c[i]*ilq%p;
      cnt=roots_of(h,out,cnt); cnt=roots_of(q,out,cnt); return cnt; } } }
static int leg(u64 a){ a%=p; if(!a) return 0; return powm(a,(p-1)/2)==1?1:-1; }
int main(int argc,char**argv){
  u64 LIM=strtoull(argv[1],0,10); srand(12345);
  char *sieve=calloc(LIM+1,1); 
  long tot[8]={0},ne[8]={0},nr[8]={0}; long rep=0;
  long tot20k=0, ne20k=0;
  for(u64 n=2;n<=LIM;n++){ if(sieve[n]) continue; for(u64 m=n*n;m<=LIM;m+=n) sieve[m]=1; if(n<5) continue;
    p=n; poly h; h.d=6; memset(h.c,0,sizeof h.c); h.c[6]=1; h.c[4]=p-30; h.c[2]=p-24; h.c[0]=p-1;
    poly x; x.d=1; memset(x.c,0,sizeof x.c); x.c[1]=1;
    poly xp=ppowmod(x,p,h); // x^p mod h
    poly d=xp; if(d.d<1){ for(int i=d.d+1;i<=1;i++) d.c[i]=0; d.d=1; } d.c[1]=(d.c[1]+p-1)%p; norm(&d);
    poly g; if(d.d<0) g=h; else g=pgcd(h,d);
    // repeated-root test
    poly hp; hp.d=5; memset(hp.c,0,sizeof hp.c); hp.c[5]=6; hp.c[3]=(4*(p-30))%p; hp.c[1]=(2*(p-24))%p; poly gg=pgcd(h,hp); if(gg.d>0) rep++;
    int cl=p%8; tot[cl]++; int nonempty=0; int nroots=0;
    if(g.d>0){ u64 rt[8]; int c=roots_of(g,rt,0); nroots=c; int two=(leg(2)==1);
      for(int i=0;i<c;i++){ u64 a=rt[i]; u64 den=(1+a*a)%p; if(den==0) continue; u64 qq=2*a%p*((1+p-a*a%p)%p)%p; u64 rr=((1+p-a)%p)*den%p;
        if(qq==0||rr==0) continue; if(leg(qq)!=1||leg(rr)!=1) continue; if(two && leg((1+p-a)%p)!=1) continue; nonempty=1; break; } }
    if(nonempty) ne[cl]++; if(nroots) nr[cl]++;
    if(p<=20000){ tot20k++; ne20k+=nonempty; }
  }
  long T=0,N=0; for(int c=1;c<8;c+=2){ T+=tot[c]; N+=ne[c]; }
  printf("LIM=%llu primes>=5: %ld nonempty: %ld (empty fraction %.5f)  [primes with repeated roots mod p: %ld]\n",LIM,T,N,1.0-(double)N/T,rep);
  printf("p<=20000: primes %ld nonempty %ld\n",tot20k,ne20k);
  long Tp=tot[1]+tot[7], Np=ne[1]+ne[7], Tm=tot[3]+tot[5], Nm=ne[3]+ne[5];
  printf("chi2=+1 (p=+-1 mod 8): %ld primes, empty fraction %.5f   (candidate 11013/12288 = %.5f)\n",Tp,1.0-(double)Np/Tp,11013.0/12288);
  printf("chi2=-1 (p=+-3 mod 8): %ld primes, empty fraction %.5f   (candidate  9854/12288 = %.5f)\n",Tm,1.0-(double)Nm/Tm,9854.0/12288);
  printf("overall candidate 20867/24576 = %.5f\n",20867.0/24576);
  for(int c=1;c<8;c+=2) printf(" class %d mod 8: primes %ld, empty %.5f\n",c,tot[c],1.0-(double)ne[c]/tot[c]);
  return 0; }
