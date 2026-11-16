<!-- Provenance: working note NOTE_coprimality_direct_proof.md (direct proof of parity, v2(psi_n) = v2(n) and gcd(psi_n, psi_{n+1}) = 1; section (a) of F.55)
     Reviewed source text, word for word, as of 16 November 2026 (delivery 2026-11-16d). Derived with a language model (Claude); not read by any human. -->

# Direct proof of  W_n = n (mod 2),  v2(W_n)=v2(n),  gcd(W_n,W_{n+1})=1   (explicit version, 16 Nov 2026)

Status: **my derivation; no human has checked it.** Written out line by line after an independent reviewer asked for the exact minimal-counterexample chain and the exact parity induction. Intermediate implications are tested in `verify_coprimality_direct.py`.

## 0. Conventions and the classical facts used
C: y^2 = x^3-2x^2+2x, P=(1,1) of infinite order (so kP != +-P for k>=2, and W_k != 0 for k != 0). W_n = psi_n(P); W_0..W_4 = 0,1,2,3,-20; W_{-n} = -W_n. A_n = W_{n-1}W_{n+1}, B_n = W_n^2 (integers), t_n = A_n/B_n, x_n = x(nP), y_n = y(nP).
* (F1) x_n = 1 - t_n (n>=1), because x(P)=1 and x(nP) = x(P) - psi_{n-1}psi_{n+1}/psi_n^2.
* (F2) W_{2n} = psi_2(nP) W_n^4 = 2 y_n W_n^4, i.e. y_n = W_{2n}/(2B_n^2).
* (F3) W_{2m+1} = W_{m+2}W_m^3 - W_{m-1}W_{m+1}^3 (m>=2), and Ward: A_nB_m - A_mB_n = W_{n+m}W_{n-m}.
* (F4) curve equation y^2 = x^3-2x^2+2x; chord formula x(Q+P) = lambda^2 + 1 - x(Q), lambda = (y(Q)-1)/(x(Q)-1) (since a2=-2, x(P)=1).
(F1)-(F4) are standard division-polynomial identities; all hold exactly for the tested range (script check 1). They are the only external facts.


### 0a. P has infinite order (Lutz-Nagell; suggested by the independent reviewer)
C has integer coefficients (y^2 = x^3 + a2 x^2 + a4 x + a6 with a2=-2, a4=2, a6=0). By the Lutz-Nagell theorem every torsion point of such a curve has integer coordinates. Doubling: lambda = (3x^2-4x+2)/(2y) = 1/2 at P=(1,1), x(2P) = lambda^2+2-2 = 1/4, y(2P) = lambda(1-1/4)-1 = -5/8. (Check: (-5/8)^2 = 25/64 = (1/4)^3 - 2(1/4)^2 + 2(1/4).) Since 2P is not integral it is not torsion, so P is not torsion. Hence kP != +-P for k>=2 and W_k != 0 for k != 0 (W_k = 0 iff kP = O).

## 1. Duplication in (A,B)
By (F1) and (F4): y_n^2 = (1-t_n)(1+t_n^2). With (F2): B_{2n} = W_{2n}^2 = 4 y_n^2 B_n^4 = 4B_n^4 (1-t_n)(1+t_n^2) = 4 B_n (B_n-A_n)(A_n^2+B_n^2).   (5b)
This is an identity between integers; it does not use parity, valuations or coprimality.

## 2. Parity: W_n = n (mod 2) for all n>=0  (strong induction, no circularity)
Base n=0..4: 0,1,2,3,-20. Let N>=5 and assume the claim for all k<N.
* N=2m+1 (m>=2): in (F3), the indices m-1,m,m+1,m+2 are all <N, so their parities are known. If m is even, W_m,W_{m+2} are even and W_{m-1},W_{m+1} odd: W_{m+2}W_m^3 is even and W_{m-1}W_{m+1}^3 is odd, so W_N is odd. If m is odd, W_{m+2}W_m^3 is odd and W_{m-1}W_{m+1}^3 is even, so W_N is odd.
* N=2m (m>=3): by (5b), 4 | B_{2m}, so W_{2m}^2 is divisible by 4 and W_N is even.
No coprimality or valuation statement is used.

## 3. v2(W_n)=v2(n)
n odd: B_n odd (parity), A_n = W_{n-1}W_{n+1} even (n+-1 even). Then B_n-A_n and A_n^2+B_n^2 are odd, so by (5b) v2(B_{2n}) = 2.
n even: B_n even, A_n odd (n+-1 odd). Again B_n-A_n and A_n^2+B_n^2 are odd, so v2(B_{2n}) = 2+v2(B_n).
For n=2^r o (o odd): v2(B_o)=0 and r applications give v2(B_n)=2r; so v2(W_n)=r=v2(n). (Only (5b) and parity are used.)

## 4. gcd(W_n,W_{n+1})=1 for all n>=0
**p=2:** by Section 2 consecutive terms have different parity.
**Odd p.** The pairs (W_0,W_1)=(0,1), (1,2), (2,3), (3,-20) are coprime. Suppose the claim is false and let N>=4 be the *smallest* index such that some odd prime p divides both W_N and W_{N+1}. Minimality means: (M) for every k<N, p does not divide both W_k and W_{k+1}.

**4.1 Choice of m.** Put m=floor(N/2), so N=2m or N=2m+1, and m>=2. In both cases 2m+1 in {N,N+1}, and one of 2m, 2m+2 is the other element of {N,N+1}. Hence
 (i) p | W_{2m+1}, and (ii) p | W_{2m} or p | W_{2m+2}.
The pairs used below are (m-1,m), (m,m+1), (m+1,m+2); their first indices m-1, m, m+1 are <N because m+1 <= 2m-1 < N (m>=2). So (M) applies to all three.

**4.2 W_m and W_{m+1} are p-units.** Suppose p | W_m. By (F3) and (i): W_{m-1}W_{m+1}^3 = W_{m+2}W_m^3 - W_{2m+1} is divisible by p, so p | W_{m-1} (contradicting (M) for (m-1,m)) or p | W_{m+1} (contradicting (M) for (m,m+1)). Suppose p | W_{m+1}. By (F3) and (i): W_{m+2}W_m^3 is divisible by p, so p | W_{m+2} (contradicts (M) for (m+1,m+2)) or p | W_m (contradicts (M) for (m,m+1)). So B_m, B_{m+1} are units in Z_(p); hence t_m, t_{m+1}, x_m, x_{m+1}, y_m, y_{m+1} (y_k = W_{2k}/(2B_k^2), p odd) are all in Z_(p), and the reductions mod p make sense.

**4.3 t_m = t_{m+1} (mod p).** Ward with (n,m)->(m+1,m): A_{m+1}B_m - A_mB_{m+1} = W_{2m+1}W_1 = W_{2m+1}. Dividing by the units B_mB_{m+1}: t_{m+1}-t_m = W_{2m+1}/(B_mB_{m+1}) = 0 mod p by (i). Call the common residue s in F_p.

**4.4 y_m = 0 (mod p), and f(s)=0.** If p | W_{2m}: y_m = W_{2m}/(2B_m^2) = 0 mod p. If p | W_{2m+2}: y_{m+1} = 0 mod p; by (F4), y_k^2 = (1-t_k)(1+t_k^2) for k=m,m+1, and t_m = t_{m+1} mod p, so y_m^2 = y_{m+1}^2 = 0 mod p, hence y_m = 0 mod p. In both cases (1-s)(1+s^2) = y_m^2 = 0 mod p. Call f(s)=(1-s)(1+s^2). In particular s != 0 (f(0)=1), so t_m is a unit.

**4.5 g(s)=0.** Since m>=2, mP != +-P, so (m+1)P = mP + P is a chord addition over Q and (F4) gives x_{m+1} = lambda^2 + 1 - x_m with lambda = (y_m-1)/(x_m-1) = (1-y_m)/t_m (x_m-1 = -t_m by (F1)). Here t_m is a unit and y_m is integral, so lambda in Z_(p), and mod p: lambda = 1/s (y_m=0). Also x_m = x_{m+1} = 1-s mod p. Thus 1-s = 1/s^2 + 1-(1-s) = 1/s^2 + s, i.e. s^2 - 2s^3 = 1, i.e. g(s)=2s^3-s^2+1 = 0 in F_p.

**4.6 Contradiction.** f(s)=g(s)=0 in F_p forces p | Res(f,g). Over Q, Res(f,g) = -16 (computed symbolically by the reviewer; also g(1)g(i)g(-i) = 2(2-2i)(2+2i) = 16 up to sign). So p | 16, impossible for odd p. Hence no minimal counterexample exists, and gcd(W_n,W_{n+1}) = 1 for all n. QED

## 5. Consequences
gcd(A_n,B_n) = gcd(W_{n-1}W_{n+1}, W_n^2) = 1 (n>=1). So t_n = A_n/B_n is in lowest terms with B_n>0: U_n=A_n, V_n=B_n, and the paper's N_n = Phi(U_n,V_n) = Phi(A_n,B_n). Together with Section 3 these are exactly the inputs (V) and coprimality used in NOTE_odd_case_proof.md.

## 6. Where each hypothesis enters (for the audit)
* Minimality (M): used only in 4.2 (three pairs). Without it nothing guarantees B_m, B_{m+1} are units.
* Parity (Section 2): used for p=2 and in Section 3. Its proof uses only (F3) for odd N and (5b) for even N.
* (F2) enters (5b) and 4.4; (F1) enters 4.3-4.5; (F4) enters 4.4-4.5; Ward enters 4.3.
* The infinite order of P (Section 0a) enters 4.5 (m P != +-P) and the nonvanishing of W_k.
