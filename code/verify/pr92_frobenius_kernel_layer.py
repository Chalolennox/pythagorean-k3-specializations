#!/usr/bin/env python3
"""Frobenius matrices in the congruence layers of the 2-adic image of J: y^2 = x^3-2x^2+2x.

For a prime p with J[2^k] in J(F_p) (p = 1 mod 8) write Frob = 1 + 2^k A on J[2^(k+1)].  The class of A mod 2
is the endomorphism of J[2] given by t -> Frob(B_t) - B_t, where B_t in J[2^(k+1)] satisfies 2^k B_t = t.
B_t is built by k halving steps from t in F_{p^2} (x-coordinates only), and Frob(B_t) - B_t in J[2] is
read off by comparing conj(x(B_t)) with x(B_t + t'), t' in J[2].
Checks per prime: A(T) = A(T2)+A(T3); trace(A) = (p-1)/2^k mod 2 (det Frob = p).
The additive span of the A's (over primes) is the image of G(2^k) in M_2(F_2); if it has dimension 4 then
G(2^k) = 1 + 2^k M_2(Z_2) (squaring 1+2^k A mod 2^(k+2) gives 1+2^(k+1) A for k >= 2, plus closedness).

Usage: pr92_frobenius_kernel_layer.py K primes_file [--max N] [--out file]
primes_file: pr92_p_divisibility_scan.tsv.gz (columns p, m_p, d_p); primes with m_p >= K are used.
"""
import sys, gzip, random, collections

class F2:  # F_{p^2} = F_p[w]/(w^2 - n)
    def __init__(self, p):
        self.p = p
        n = 2
        while pow(n, (p - 1) // 2, p) != p - 1: n += 1
        self.n = n
        q = p * p - 1; s = 0
        while q % 2 == 0: q //= 2; s += 1
        self.q, self.s = q, s
        self.z = None
    def mul(self, a, b):
        p = self.p
        return ((a[0] * b[0] + self.n * a[1] * b[1]) % p, (a[0] * b[1] + a[1] * b[0]) % p)
    def add(self, a, b): p = self.p; return ((a[0] + b[0]) % p, (a[1] + b[1]) % p)
    def sub(self, a, b): p = self.p; return ((a[0] - b[0]) % p, (a[1] - b[1]) % p)
    def pw(self, a, e):
        r = (1, 0)
        while e:
            if e & 1: r = self.mul(r, a)
            a = self.mul(a, a); e >>= 1
        return r
    def inv(self, a):
        p = self.p
        nm = (a[0] * a[0] - self.n * a[1] * a[1]) % p
        ni = pow(nm, -1, p)
        return (a[0] * ni % p, (-a[1]) * ni % p)
    def is_sq(self, a):
        if a == (0, 0): return True
        nm = (a[0] * a[0] - self.n * a[1] * a[1]) % self.p
        return pow(nm, (self.p - 1) // 2, self.p) == 1
    def sqrt(self, a):
        if a == (0, 0): return a
        if self.z is None:
            r = random.Random(1)
            while True:
                z = (r.randrange(self.p), r.randrange(1, self.p))
                if not self.is_sq(z): break
            self.z = z
        M = self.s; c = self.pw(self.z, self.q); t = self.pw(a, self.q); R = self.pw(a, (self.q + 1) // 2)
        while t != (1, 0):
            t2 = t; k = 0
            while t2 != (1, 0): t2 = self.mul(t2, t2); k += 1
            assert k < M
            b = c
            for _ in range(M - k - 1): b = self.mul(b, b)
            M = k; c = self.mul(b, b); t = self.mul(t, c); R = self.mul(R, b)
        assert self.mul(R, R) == a
        return R

def halve(F, x0, es):
    u = [F.sub(x0, e) for e in es]
    if not all(F.is_sq(a) for a in u): return None
    s1, s2, s3 = (F.sqrt(a) for a in u)
    neg = lambda a: ((-a[0]) % F.p, (-a[1]) % F.p)
    x = F.add(x0, F.add(F.mul(s1, s2), F.add(F.mul(s1, s3), F.mul(s2, s3))))
    return x

def frob_layer_matrix(p, k):
    """returns (code(A T2), code(A T3), code(A T)) with codes O=0,T2=1,T3=2,T=3, or raises"""
    F = F2(p)
    z = pow(2, 1, p)
    nr = 2
    while pow(nr, (p - 1) // 4, p) in (1, p - 1) or pow(nr, (p - 1) // 4, p) ** 2 % p != p - 1:
        nr += 1
    i = pow(nr, (p - 1) // 4, p)
    assert i * i % p == p - 1
    e1, e2, e3 = (0, 0), ((1 + i) % p, 0), ((1 - i) % p, 0)
    es = (e1, e2, e3)
    def translate(x, e, ea, eb):
        # x(B + (e,0)) = e + (e-ea)(e-eb)/(x-e)
        c = F.mul(F.sub(e, ea), F.sub(e, eb))
        return F.add(e, F.mul(c, F.inv(F.sub(x, e))))
    def code_of(x):
        xc = (x[0], (-x[1]) % p)
        cand = {0: x, 3: translate(x, e1, e2, e3), 1: translate(x, e2, e1, e3), 2: translate(x, e3, e1, e2)}
        hit = [c for c, v in cand.items() if v == xc]
        assert len(hit) == 1, (p, hit)
        return hit[0]
    out = {}
    for name, e in (("T2", e2), ("T3", e3), ("T", e1)):
        x = e
        for _ in range(k):
            x = halve(F, x, es)
            assert x is not None
        out[name] = code_of(x)
    return out["T2"], out["T3"], out["T"]

def vec(a, b): return a | (b << 2)           # 4-bit vector in F_2^4
def trace_bit(a, b): return (a & 1) ^ ((b >> 1) & 1)

def rank(vs):
    basis = []
    for v in vs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)

def span_size(vs):
    S = {0}
    for v in vs: S |= {s ^ v for s in S}
    return len(S)

if __name__ == "__main__":
    K = int(sys.argv[1]); fn = sys.argv[2]
    mx = None; out = None
    a = sys.argv[3:]
    while a:
        if a[0] == "--max": mx = int(a[1]); a = a[2:]
        elif a[0] == "--out": out = a[1]; a = a[2:]
        else: raise SystemExit("bad arg")
    ps = []
    for line in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        if line.startswith("#"): continue
        p, m, d = map(int, line.split())
        if m >= K: ps.append((p, m, d))
        if mx and len(ps) >= mx: break
    res = []; bad = 0
    for p, m, d in ps:
        aT2, aT3, aT = frob_layer_matrix(p, K)
        ok_lin = (aT2 ^ aT3) == aT
        tr = trace_bit(aT2, aT3)
        ok_tr = tr == (((p - 1) >> K) & 1)
        zero_ok = ((aT2 | aT3) == 0) == (m >= K + 1)
        if not (ok_lin and ok_tr and zero_ok):
            bad += 1; print("CHECK FAILED", p, m, aT2, aT3, aT, ok_lin, ok_tr, zero_ok)
        res.append((p, m, aT2, aT3, vec(aT2, aT3), tr))
    print("level k=%d: %d primes with J[2^%d] rational (smallest %d, largest %d); failed internal checks: %d" % (K, len(res), K, res[0][0], res[-1][0], bad))
    vs = [r[4] for r in res]
    print("dimension of the F_2-span of the matrices A mod 2 in M_2(F_2): %d (span has %d elements)" % (rank(vs), span_size(set(vs))))
    cnt = collections.Counter(vs)
    print("distinct matrices seen: %d of 16;  counts by (trace,vector):" % len(cnt))
    for tr in (0, 1):
        sub = {v: c for v, c in cnt.items() if trace_bit(v & 3, v >> 2) == tr}
        n = sum(sub.values())
        print("  trace %d: %d primes, %d distinct of 8, counts %s" % (tr, n, len(sub), sorted(sub.values(), reverse=True)))
    # chi-square vs uniform over the 8 matrices of each trace class
    chi = 0.0; df = 0
    for tr in (0, 1):
        vals = [v for v in range(16) if trace_bit(v & 3, v >> 2) == tr]
        n = sum(cnt.get(v, 0) for v in vals)
        if n == 0: continue
        exp = n / 8.0
        chi += sum((cnt.get(v, 0) - exp) ** 2 / exp for v in vals); df += 7
    print("chi-square against uniform on the 8 matrices of each trace class: %.1f on %d d.o.f." % (chi, df))
    # first four independent examples
    basis = []; ex = []
    for r in res:
        v = r[4]; w = v
        for b in basis: w = min(w, w ^ b)
        if w:
            basis.append(w); ex.append(r)
        if len(basis) == 4: break
    print("independent examples (p, m_p, A(T2), A(T3)):", [(r[0], r[1], r[2], r[3]) for r in ex])
    if out:
        with open(out, "w") as f:
            f.write("# p\tm_p\tcodeA(T2)\tcodeA(T3)  (codes O=0,T2=1,T3=2,T=3), level k=%d\n" % K)
            for r in res: f.write("%d\t%d\t%d\t%d\n" % (r[0], r[1], r[2], r[3]))
