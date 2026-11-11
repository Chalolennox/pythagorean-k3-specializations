// odd_order_density.c -- density of primes p for which alpha = (c, ck) has ODD order in E(F_p),  E : y^2 = x^3 + a x^2 + b x,  b = c k^2 - a c - c^2   (Liang-Rouse parametrisation).
// Our curve C : y^2 = x^3 - 2x^2 + 2x with P = (1,1) is [a,c,k] = [-2,1,1].   Build: gcc -O2 -o odd_order_density code/odd_order_density.c -lm
// Usage: ./odd_order_density a c k LIMIT     prints the fraction of primes q <= LIMIT (q not dividing 2 b (a^2-4b) c) with odd order, overall and by q mod 8 and mod 3.
// The order of alpha is found by baby-step giant-step in the Hasse interval.  Validated against Table 1 of Liang-Rouse (arXiv 1810.10583) at LIMIT = 10^7 (see notes/odd_order_density_check.md).
// For each prime 5 <= p <= LIM: order r_p of P = (1,1) in C(F_p), C : y^2 = x^3 - 2x^2 + 2x.  Count primes with r_p odd, overall and by classes of p.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
typedef int64_t i64; typedef uint64_t u64;
static i64 p; static i64 Aa,Bc,Cc,Kc;
typedef struct { i64 x, y; int inf; } pt;
static inline i64 md(i64 a){ a%=p; return a<0?a+p:a; }
static i64 inv(i64 a){ i64 t=0,nt=1,r=p,nr=md(a); while(nr){ i64 q=r/nr; i64 tmp=t-q*nt; t=nt; nt=tmp; tmp=r-q*nr; r=nr; nr=tmp; } return t<0?t+p:t; }
static pt add(pt A, pt B){
  if(A.inf) return B; if(B.inf) return A;
  i64 l;
  if(A.x==B.x){ if(md(A.y+B.y)==0){ pt O={0,0,1}; return O; }
    l = md(((3*A.x%p*A.x + 2*md(Aa)*A.x + md(Bc))%p) * inv(2*A.y)); }
  else l = md(md(B.y-A.y)*inv(B.x-A.x));
  i64 x3 = md(l*l%p - md(Aa) - A.x - B.x);
  pt R={x3, md(l*md(A.x-x3)%p - A.y), 0}; return R; }
static pt mul(u64 k, pt A){ pt R={0,0,1}; while(k){ if(k&1) R=add(R,A); A=add(A,A); k>>=1; } return R; }
static int isO(pt A){ return A.inf; }
// baby steps: store x -> j in a sorted array
typedef struct { i64 x; int j; int sgn; } bs;
static int cmp(const void*a,const void*b){ i64 d=((const bs*)a)->x-((const bs*)b)->x; return d<0?-1:d>0; }
static u64 order_of_P(){
  pt P={md(Cc),md(Cc*Kc),0}; i64 w=(i64)(2*sqrt((double)p))+2, L=p+1-w, H=p+1+w;
  int m=(int)sqrt((double)(H-L))+2; bs *B=malloc(sizeof(bs)*(m+1)); pt cur={0,0,1};
  for(int j=0;j<=m;j++){ B[j].x= cur.inf? -1 : cur.x; B[j].j=j; cur=add(cur,P); }
  qsort(B,m+1,sizeof(bs),cmp);
  pt G=mul(m,P), S=mul(L,P); u64 found=0;
  for(i64 i=0;i<=(H-L)/m+1 && !found;i++){
    i64 key = S.inf? -1 : S.x;
    // binary search for key in B
    int lo=0,hi=m; while(lo<hi){ int mid=(lo+hi)/2; if(B[mid].x<key) lo=mid+1; else hi=mid; }
    for(int t=lo;t<=m && B[t].x==key;t++){
      int j=B[t].j; pt Pj=mul(j,P);
      // S = L P + i m P  equals +-jP  ->  candidate N = L + i m -+ j
      u64 N1=(u64)(L+i*m - j), N2=(u64)(L+i*m + j);
      if(isO(mul(N1,P))) { found=N1; break; }
      if(isO(mul(N2,P))) { found=N2; break; }
      (void)Pj; }
    S=add(S,G); }
  free(B);
  if(!found){ // fallback (should not happen): brute force in the interval
    for(i64 N=L;N<=H;N++) if(isO(mul(N,P))){ found=N; break; } }
  // reduce to the exact order
  u64 r=found, n=found; for(u64 q=2;q*q<=n;q++) if(n%q==0){ while(n%q==0) n/=q; while(r%q==0 && isO(mul(r/q,P))) r/=q; }
  if(n>1){ u64 q=n; while(r%q==0 && isO(mul(r/q,P))) r/=q; }
  return r; }
int main(int argc,char**argv){
  Aa=atoll(argv[1]); i64 cc=atoll(argv[2]), kk=atoll(argv[3]); Cc=cc; Kc=kk; Bc=cc*kk*kk-Aa*cc-cc*cc; i64 disc=2*Bc*(Aa*Aa-4*Bc)*cc; if(disc<0) disc=-disc;
  i64 LIM=atoll(argv[4]); char*sv=calloc(LIM+1,1);
  for(i64 i=2;i*i<=LIM;i++) if(!sv[i]) for(i64 j=i*i;j<=LIM;j+=i) sv[j]=1;
  long tot=0, odd=0; long c8[8][2]; memset(c8,0,sizeof c8); long c3[3][2]; memset(c3,0,sizeof c3);
  long checkpoint=1000000;
  for(i64 q=3;q<=LIM;q++){ if(sv[q]) continue; if(disc%q==0) continue; p=q; u64 r=order_of_P(); int o=(r&1); tot++; odd+=o; c8[p%8][o]++; c3[p%3][o]++;
    if(q>=checkpoint){ printf("p <= %lld: %ld primes, odd order at %ld (%.5f)\n",(long long)q,tot,odd,(double)odd/tot); fflush(stdout); checkpoint*=10; if(checkpoint<=LIM && 0) ; } }
  printf("FINAL p <= %lld: %ld primes (p >= 5), odd order %ld = %.6f\n",(long long)LIM,tot,odd,(double)odd/tot);
  for(int a=1;a<8;a+=2) printf("  p = %d mod 8: %ld primes, odd-order fraction %.5f\n",a,c8[a][0]+c8[a][1],(double)c8[a][1]/(c8[a][0]+c8[a][1]));
  for(int a=1;a<3;a++) printf("  p = %d mod 3: %ld primes, odd-order fraction %.5f\n",a,c3[a][0]+c3[a][1],(double)c3[a][1]/(c3[a][0]+c3[a][1]));
  return 0; }
