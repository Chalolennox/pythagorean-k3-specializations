// Scan primes p <= LIMIT.  f(t) = t^6 - 30 t^4 - 24 t^2 - 1 = g(t^2), g(s) = s^3 - 30 s^2 - 24 s - 1.
// For primes where f splits completely mod p (g has 3 roots in F_p, all quadratic residues) print the data for the index-four question.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static u64 P;
static inline u64 mm(u64 a,u64 b){ return (u64)((u128)a*b % P); }
static u64 pw(u64 a,u64 e){ u64 r=1; a%=P; while(e){ if(e&1) r=mm(r,a); a=mm(a,a); e>>=1;} return r; }
typedef struct { u64 c[3]; } poly;               // c0 + c1 s + c2 s^2  mod (s^3 = 30 s^2 + 24 s + 1)
static poly pmul(poly a, poly b){
  u64 t[5]={0,0,0,0,0};
  for(int i=0;i<3;i++) for(int j=0;j<3;j++) t[i+j]=(t[i+j]+mm(a.c[i],b.c[j]))%P;
  // s^4 = 924 s^2 + 721 s + 30 ; s^3 = 30 s^2 + 24 s + 1
  u64 r2=(t[2]+mm(t[3],30)+mm(t[4],924))%P, r1=(t[1]+mm(t[3],24)+mm(t[4],721))%P, r0=(t[0]+t[3]+mm(t[4],30))%P;
  poly r={{r0,r1,r2}}; return r; }
static poly ppow(poly a,u64 e){ poly r={{1,0,0}}; while(e){ if(e&1) r=pmul(r,a); a=pmul(a,a); e>>=1;} return r; }
static u64 sqrtmod(u64 a){          // Tonelli-Shanks, returns 0 if nonresidue
  a%=P; if(a==0) return 0; if(pw(a,(P-1)/2)!=1) return 0;
  u64 q=P-1; int s=0; while(q%2==0){ q/=2; s++; }
  u64 z=2; while(pw(z,(P-1)/2)==1) z++;
  u64 c=pw(z,q), r=pw(a,(q+1)/2), t=pw(a,q); int m=s;
  while(t!=1){ int i=0; u64 tt=t; while(tt!=1){ tt=mm(tt,tt); i++; } u64 b=c; for(int j=0;j<m-i-1;j++) b=mm(b,b);
    r=mm(r,b); c=mm(b,b); t=mm(t,c); m=i; }
  return r; }
static u64 inv(u64 a){ return pw(a,P-2); }
// roots of g mod P if it splits completely; returns 1 and fills r[3]
static int cubic_roots(u64 r[3]){
  poly s={{0,1,0}}; poly sp=ppow(s,P);
  if(!(sp.c[0]==0 && sp.c[1]==1 && sp.c[2]==0)) return 0;                 // not completely split
  for(u64 a=0;a<200;a++){
    poly b={{a,1,0}}; poly w=ppow(b,(P-1)/2);                           // (s+a)^((P-1)/2) mod g ; roots of g where s+a is a QR give w=1, else -1
    // evaluate which roots: instead of gcd, find a root by trying to split via values: we need the roots themselves -> use gcd(g, w-1)
    u64 w0=(w.c[0]+P-1)%P, w1=w.c[1], w2=w.c[2];
    // gcd of g and (w2 s^2 + w1 s + w0) over F_P
    u64 A[4]={P-1,P-24%P,P-30%P,1};                                      // g = s^3 - 30 s^2 - 24 s - 1  (coeffs c0..c3)
    A[0]=P-1; A[1]=(P-24)%P; A[2]=(P-30)%P; A[3]=1;
    u64 B[3]={w0,w1,w2}; int db=2; while(db>=0 && B[db]==0) db--;
    if(db<0) continue;                                                    // w == 1 : all roots QR, no split
    // polynomial gcd (Euclid)
    u64 X[4]; memcpy(X,A,sizeof A); int dx=3; u64 Y[4]={B[0],B[1],B[2],0}; int dy=db;
    while(dy>=0){
      // X mod Y
      while(dx>=dy && dx>=0){ u64 f=mm(X[dx],inv(Y[dy])); for(int i=0;i<=dy;i++) X[dx-dy+i]=(X[dx-dy+i]+P-mm(f,Y[i]))%P; dx--; while(dx>=0 && X[dx]==0) dx--; }
      u64 T[4]; memcpy(T,X,sizeof T); memcpy(X,Y,sizeof T); memcpy(Y,T,sizeof T); int td=dx; dx=dy; dy=td; }
    int dg=dx;                                                            // gcd = X (degree dg)
    if(dg==1){ u64 rt=mm((P-X[0])%P,inv(X[1])); r[0]=rt; 
      // quotient g/(s-rt) = s^2 + b s + c
      u64 b2=(rt+P-30)%P, c2=(mm(rt,b2)+P-24)%P;
      u64 disc=(mm(b2,b2)+P-4*c2%P)%P; u64 sq=sqrtmod(disc); if(!sq && disc) continue;
      u64 i2=inv(2); r[1]=mm((P-b2+sq)%P,i2); r[2]=mm((P-b2+P-sq)%P,i2); return 1; }
    if(dg==2){ u64 il=inv(X[2]); u64 b2=mm(X[1],il), c2=mm(X[0],il); u64 disc=(mm(b2,b2)+P-4*c2%P)%P; u64 sq=sqrtmod(disc); if(!sq && disc) continue;
      u64 i2=inv(2); r[0]=mm((P-b2+sq)%P,i2); r[1]=mm((P-b2+P-sq)%P,i2); r[2]=(30+2*P-r[0]-r[1])%P; return 1; }
  }
  return 0; }
int main(int argc,char**argv){
  u64 LIM=strtoull(argv[1],0,10); u64 SEG=1<<24;
  // base primes
  u64 sq=1; while(sq*sq<=LIM) sq++; char*bs=calloc(sq+1,1); u64*bp=malloc(sizeof(u64)*(sq)); int nb=0;
  for(u64 i=2;i<=sq;i++){ if(!bs[i]){ bp[nb++]=i; for(u64 j=i*i;j<=sq;j+=i) bs[j]=1; } }
  char*seg=malloc(SEG);
  for(u64 lo=0;lo<=LIM;lo+=SEG){
    u64 hi=lo+SEG-1; if(hi>LIM) hi=LIM; memset(seg,0,SEG);
    for(int k=0;k<nb;k++){ u64 q=bp[k]; if(q*q>hi) break; u64 st=((lo+q-1)/q)*q; if(st<q*q) st=q*q; for(u64 j=st;j<=hi;j+=q) seg[j-lo]=1; }
    for(u64 n=lo;n<=hi;n++){ if(n<7||seg[n-lo]) continue; P=n;
      if(P%8!=1 && !getenv("ALLP")) continue;                              // T_p = 6 forces p = 1 mod 8; ALLP=1 disables the filter
      u64 r[3]; if(!cubic_roots(r)) continue;
      u64 tau[3]; int ok=1; for(int j=0;j<3;j++){ tau[j]=sqrtmod(r[j]); if(!tau[j]){ ok=0; break; } }
      if(!ok) continue;
      u64 I=sqrtmod(P-1);                                                  // sqrt(-1) when it exists
      int ta=0,tb=0,tc=0, chi[3]={0,0,0};
      for(int j=0;j<3;j++) for(int sg=0;sg<2;sg++){ u64 t=sg?(P-tau[j])%P:tau[j]; u64 x=(1+P-t)%P; u64 y2=mm(x,(mm(x,x)+P-2*x%P+2)%P);
        int onC=(y2==0)||pw(y2,(P-1)/2)==1; int xsq=(x!=0)&&pw(x,(P-1)/2)==1; ta+=onC; tb+=(onC&&xsq); { u64 t1=(1+P-mm(t,t))%P; u64 arg=mm(mm(2,t),t1); int c2=(arg!=0)&&pw(arg,(P-1)/2)==1; tc+=(onC&&c2&&y2!=0); }
        if(I && sg==0){ u64 v=(t+I)%P; chi[j]=(v==0)?0:(pw(v,(P-1)/2)==1?1:-1); } }
      printf("%llu %d %d %d %d %d %d\n",(unsigned long long)P,ta,tb,tc,chi[0],chi[1],chi[2]); }
  }
  return 0; }
