// fibrecount.c : N_k = sum over t in P^1(F_q) of a_t,  q = p^k,  a_t = -sum_x chi(x^3 + a4(t) x + a6(t)).
// Model of the twist K3 surface (minimal at every place):
//   Y^2 = X^3 + 4(1-t^2)(1+t^2)N(t)^2 X - 16 t (1+t^2)^2 N(t)^3,   N(t) = n2 t^2 + n1 t + n0.
// Usage: ./fibrecount p k n2 n1 n0     (n_i integers mod p; p >= 5 prime; k <= 5)
// Fields: log/antilog tables from a primitive polynomial, Zech logarithms for addition.
// Fibres over F_q whose t has Frobenius orbit of full size k >= 4 are counted by baby-step giant-step.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
int p, k; ll q, Q1;
int *expt, *logt, *Z;

static int mulx(int code, int *poly) {            // multiply by x modulo x^k = -poly(x); digits in base p
    int d[8], c = code;
    for (int i = 0; i < k; i++) { d[i] = c % p; c /= p; }
    int top = d[k-1];
    for (int i = k-1; i > 0; i--) d[i] = d[i-1];
    d[0] = 0;
    for (int i = 0; i < k; i++) d[i] = ((d[i] - top*poly[i]) % p + p) % p;
    int r = 0;
    for (int i = k-1; i >= 0; i--) r = r*p + d[i];
    return r;
}
static int addcode(int a, int b) {
    int r = 0, m = 1;
    for (int i = 0; i < k; i++) { r += (((a % p) + (b % p)) % p) * m; a /= p; b /= p; m *= p; }
    return r;
}
static void build(void) {
    q = 1; for (int i = 0; i < k; i++) q *= p;
    Q1 = q - 1;
    expt = malloc(sizeof(int)*q); logt = malloc(sizeof(int)*q); Z = malloc(sizeof(int)*q);
    int poly[8];
    for (ll cand = 0; cand < q; cand++) {          // first primitive polynomial x^k + ... + poly[0]
        ll c = cand;
        for (int i = 0; i < k; i++) { poly[i] = c % p; c /= p; }
        if (poly[0] == 0 && k > 1) continue;
        int cur = 1, ok = 1;
        memset(logt, -1, sizeof(int)*q);
        for (ll i = 0; i < Q1; i++) {
            if (logt[cur] != -1) { ok = 0; break; }
            expt[i] = cur; logt[cur] = i; cur = mulx(cur, poly);
        }
        if (ok && cur == 1) break;
    }
    for (ll n = 0; n < Q1; n++) { int s = addcode(1, expt[n]); Z[n] = (s == 0) ? -1 : logt[s]; }
}
// arithmetic on logarithms; -1 stands for 0
static inline ll ladd(ll a, ll b) { if (a < 0) return b; if (b < 0) return a; ll d = b - a; if (d < 0) d += Q1; int z = Z[d]; if (z < 0) return -1; ll r = a + z; if (r >= Q1) r -= Q1; return r; }
static inline ll lmul(ll a, ll b) { if (a < 0 || b < 0) return -1; ll r = a + b; if (r >= Q1) r -= Q1; return r; }
static inline ll lneg(ll a) { if (a < 0) return -1; ll r = a + Q1/2; if (r >= Q1) r -= Q1; return r; }
static inline ll lsub(ll a, ll b) { return ladd(a, lneg(b)); }
static inline ll linv(ll a) { return (Q1 - a) % Q1; }
static ll lconst(int v) { v %= p; if (v < 0) v += p; return v == 0 ? -1 : logt[v]; }
static ll lpow(ll a, int e) { return a < 0 ? -1 : (a*e) % Q1; }

static ll legsum(ll A, ll B) {                     // sum over x of chi(x^3 + A x + B), A and B given as logs
    ll s = 0;
    if (B >= 0) s += (B % 2 == 0) ? 1 : -1;        // x = 0
    for (ll L = 0; L < Q1; L++) {
        ll f = ladd(ladd((3*L) % Q1, (A < 0) ? -1 : (A + L) % Q1), B);
        if (f >= 0) s += (f & 1) ? -1 : 1;
    }
    return s;
}
// ---- point counting on y^2 = x^3 + A x + B over F_q by baby-step giant-step ----
typedef struct { ll x, y; int inf; } Pt;
static ll LA, LB, L2, L3;
static Pt padd(Pt P, Pt Q) {
    if (P.inf) return Q;
    if (Q.inf) return P;
    ll lam;
    if (P.x == Q.x) {
        if (P.y == lneg(Q.y) || (P.y < 0 && Q.y < 0)) { Pt O = {0, 0, 1}; return O; }
        lam = lmul(ladd(lmul(L3, lmul(P.x, P.x)), LA), linv(lmul(L2, P.y)));
    } else lam = lmul(lsub(Q.y, P.y), linv(lsub(Q.x, P.x)));
    ll x3 = lsub(lsub(lmul(lam, lam), P.x), Q.x);
    Pt R = {x3, lsub(lmul(lam, lsub(P.x, x3)), P.y), 0};
    return R;
}
static Pt pmul(Pt P, ll n) {
    Pt R = {0, 0, 1};
    if (n < 0) { n = -n; if (!P.inf) P.y = lneg(P.y); }
    while (n) { if (n & 1) R = padd(R, P); P = padd(P, P); n >>= 1; }
    return R;
}
static unsigned long long rng = 88172645463325252ULL;
static unsigned long long rnd(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static int randpt(Pt *P) {
    for (int tries = 0; tries < 200; tries++) {
        ll L = rnd() % Q1;
        ll f = ladd(ladd((3*L) % Q1, (LA < 0) ? -1 : (LA + L) % Q1), LB);
        if (f >= 0 && f % 2 == 0) { P->x = L; P->y = f/2; P->inf = 0; return 1; }
    }
    return 0;
}
#define MAXC 600
static int candidates(Pt P, ll W, ll *cand) {      // all M in [q+1-W, q+1+W] with M*P = O
    ll m = 1; while (m*m < W) m++; m += 1;
    Pt baby[1024]; baby[0].inf = 1; baby[0].x = 0; baby[0].y = 0;
    Pt cur = P;
    for (ll j = 1; j < m; j++) { baby[j] = cur; cur = padd(cur, P); }
    Pt mP = cur, T = pmul(P, q + 1);
    if (!T.inf) T.y = lneg(T.y);                   // T = -(q+1)P
    ll amax = W/m + 2; int nc = 0;
    Pt S = padd(T, pmul(mP, amax));                // S_a = -(q+1)P - a mP, started at a = -amax
    Pt negm = mP; if (!negm.inf) negm.y = lneg(negm.y);
    for (ll a = -amax; a <= amax; a++) {
        for (ll b = 0; b < m; b++) {
            int eq = (S.inf && baby[b].inf) || (!S.inf && !baby[b].inf && S.x == baby[b].x && S.y == baby[b].y);
            if (eq) { ll kk = a*m + b; if (kk >= -W && kk <= W && nc < MAXC) cand[nc++] = q + 1 + kk; }
        }
        S = padd(S, negm);
    }
    return nc;
}
static ll count_points(ll A, ll B) {               // #E(F_q), or -1 on failure
    LA = A; LB = B;
    ll W = 2; while (W*W <= q) W++; W *= 2;
    ll cand[MAXC], cur[MAXC]; int nc = -1, informative = 0;
    for (int it = 0; it < 60; it++) {
        Pt P; if (!randpt(&P)) return -1;
        int n = candidates(P, W, cand);
        if (n >= MAXC - 1 || n > 24) continue;     // a point of small order says too little: skip it
        informative++;
        if (nc < 0) { nc = n; memcpy(cur, cand, sizeof(ll)*n); }
        else { int m2 = 0; for (int i = 0; i < nc; i++) for (int j = 0; j < n; j++) if (cur[i] == cand[j]) { cur[m2++] = cur[i]; break; } nc = m2; }
        if (nc == 0) return -1;
        if (nc == 1 && informative >= 4) return cur[0];
    }
    return -1;
}
int main(int argc, char **argv) {
    p = atoi(argv[1]); k = atoi(argv[2]);
    int n2 = atoi(argv[3]), n1 = atoi(argv[4]), n0 = atoi(argv[5]);
    build();
    L2 = lconst(2); L3 = lconst(3);
    ll cn2 = lconst(n2), cn1 = lconst(n1), cn0 = lconst(n0), total = 0;
    ll Ainf = lneg(lmul(lconst(4), lmul(cn2, cn2)));          // t = infinity: a4 = -4 n2^2, a6 = 0
    if (Ainf >= 0) total -= legsum(Ainf, -1);
    ll A0 = lmul(lconst(4), lmul(cn0, cn0));                  // t = 0: a4 = 4 N(0)^2, a6 = 0
    if (A0 >= 0) total -= legsum(A0, -1);
    char *seen = calloc(Q1, 1);
    for (ll m = 0; m < Q1; m++) {                             // t = g^m, one t per Frobenius orbit
        if (seen[m]) continue;
        int osz = 0; ll mm = m;
        do { seen[mm] = 1; osz++; mm = (mm*p) % Q1; } while (mm != m);
        ll t = m, t2 = lpow(t, 2);
        ll omt2 = ladd(0, lneg(t2)), opt2 = ladd(0, t2);
        ll N = ladd(ladd(lmul(cn2, t2), lmul(cn1, t)), cn0);
        ll A = lmul(lconst(4), lmul(lmul(omt2, opt2), lpow(N, 2)));
        ll B = lneg(lmul(lconst(16), lmul(lmul(t, lpow(opt2, 2)), lpow(N, 3))));
        if (A < 0 && B < 0) continue;                         // additive fibre, a_t = 0
        ll disc = ladd((A < 0) ? -1 : lmul(lconst(4), lpow(A, 3)), (B < 0) ? -1 : lmul(lconst(27), lpow(B, 2)));
        ll at;
        if (osz == k && k >= 4 && disc >= 0) {
            ll npts = count_points(A, B);
            at = (npts > 0) ? q + 1 - npts : -legsum(A, B);
        } else at = -legsum(A, B);
        total += osz * at;
    }
    printf("%d %d %lld", p, k, total); putchar(10);
    return 0;
}
