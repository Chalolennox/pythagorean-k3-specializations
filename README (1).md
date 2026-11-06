# Scripts as run

These scripts are the working scripts behind individual claims of the paper. They were written in different sessions, mostly to check one statement each, and are **not cleaned up**: several load each other with `exec(open(...))`, several have no command-line interface, and some print more than they need to. They are kept because a claim without its script is harder to check.

**How to run.** Work from this directory (`cd code/scripts_as_run`), with Python 3, `sympy`, `numpy` and `scipy` installed (see `../../requirements.txt`). A few scripts write small files (pickles, jsonl) into the current directory; delete them afterwards. `scan.py` needs the compiled counter: `gcc -O2 -o fibrecount ../fibrecount.c` and it writes `scan_new.jsonl`.

**What the status column means.** It records only that the script was started in a clean copy of this directory on 6 November 2026 and what it printed last. *runs* means exit status 0 within 30 seconds; it does not mean the output was re-read against the paper, except for the scripts reproduced by `code/validate.py` and `code/verify_factorizations.py`. *long-running* means no error in the first 30 seconds.

| Script | Claim or paragraph | Status | Last line printed or error |
| --- | --- | --- | --- |
| Tproof2.py | F.21 classes of t'_n and local constancy of the local factors | runs | real factor, t<1: [-1, 1] |
| Tproof3.py | F.21 local constancy on rational points | runs |    t=8 mod 9 [1] |
| analyze.py | F.44 first version of the analysis (superseded by code/lfunc.py) | runs |   p=19  eps=-1  e5=0  #eigenvalues of form p*zeta = 2  (rho(F_p-bar)=14)  Lambda_p=484/361 |
| analyze_scan.py | F.46 classification of the scan | runs (from this directory) | reads ../../data/*.jsonl |
| bg1112.py | F.38 the n = 11, 12 numbers, trial division and ECM | long-running | no error in the first 30 s |
| c4prime_delta.py | F.37 delta along the C4' orbit | long-running | no error in the first 30 s |
| c4prime_verify.py | F.37 verification of those factorizations | runs |      factors: {'186041463417...(18 digits)': 1, '674934850740...(69 digits)': 1} |
| cases.py | F.28 search for squareful t | runs | (3969, 4, 1, 17, {3: 4, 7: 2}) |
| classify_all.py | F.45 classification with all candidate L-functions | runs (from this directory) | reads ../../data/*.jsonl |
| coprime.py | F.25 gcd(F_n,G_n)=1, resultant and common roots | runs | brute force n=1..150: gcd(/F_n/,/G_n/)=1 for all n: True [] |
| covers.py | F.30 growth and point counts of the covers | runs | C1 (c=1) w^2=(1+t^2)(-3t^2-16t+5)  # {t: H(t)<=B} for B=[10, 30, 100, 300, 1000, 3000] : [ |
| doubling_indep.py | F.36 independence of h and its doubling pullback | runs | disc(Num) primes: skipped |
| eps.py | exact definition of epsilon; helpers jac, triple, pieces (used by many scripts) | runs | f(t) matches the table column in 16/16 members; eps = f*(ab/F'') equals W*lambda in 16/16  |
| eps_pred.py | F.45 sign of the functional equation | runs | c=13/9: [(11, -1), (19, 1), (37, 1), (41, -1)] |
| evenodd.py | F.42 even/odd divisibility ratio | runs | R(infinity,10000) = 1.67364670646 |
| evenodd2.py | F.42 extension to p <= 40000 (needs evenodd_rows.pkl written by evenodd.py) | runs | fraction of primes with even ord(P): 0.577 |
| g3.py | F.20 valuations of F_n and G_n at 2 and 3 | runs | a_n is a perfect square (so x(nP+T)=2d/a has denominator a square): True |
| hilb.py | Hilbert symbols of the reciprocity formula (used by split23.py) | runs | [] |
| multi_t.py | F.28 / F.40 analytic checks at further t (needs t4.py) | runs | summary: 6 of 6 agree |
| nagao.py | F.43 Nagao-type rank estimates for the covers | runs | c=4                              running estimate of the Q(t)-rank of the twist (primes up |
| nagao_m.py | F.43 twists by a constant m | runs | m scanned: [-30, -29, -26, -23, -22, -21, -19, -17, -15, -14, -13, -11, -10, -7, -6, -5, - |
| netrel.py | F.34 elliptic-net relation | runs | disc_u(N) is not identically 0 modulo h(alpha) (so N is squarefree for each root alpha of  |
| onebit.py | F.31 the one-bit table (W = eps*delta) | runs | T     9    91    4  -1  3  +1  +1   +1   +1   +1   fact_ok=True  W==eps*delta:True  eps==p |
| poisson_parity.py | F.40-type Poisson parity model | runs |    N=50: refined 48.94   fair 49.0 |
| quot.py | F.26 the quotient sextic R(U) | runs | 5. Galois group of h: 24 True ; of R: 24 True |
| quot2.py | F.26 exceptional primes; F_n G_n = R_h(p_n,q_n) | runs | n<=40: F_n G_n = R_h(A^2+2B^4, A B^2): 40 ; gcd(p_n,q_n)=1: 40 ; x'(nP'')=x(nP)+2/x(nP)-2  |
| rootnum.py | F.28 analytic root number from the functional equation (library) | runs | 389a y=1.5 y^2 g(y)/g(1/y) = 1.0 |
| scan.py | F.46 scan of rational c (writes scan.jsonl; needs the compiled counter, here named count) | long-running | no error in the first 30 s |
| split23.py | 2-adic and 3-adic factors of epsilon | runs | Psi_2*Psi_3*Psi_inf equals eps_n computed from Jacobi symbols for n=2..59: 58 / 58 |
| splitcheck.py | F.28 Delta identity and the split condition | runs | primes p>=5 dividing F in 618 cases: p / c4 in 0; (-c6/p) != (ab/p) in 0 |
| sqclass.py | F.29 / F.36 squareclass independence of h*h_T | runs | h*hT*x(x^2-2x+2) squarefree-part degree:  15 ; gcd with derivative degree: 0 |
| t4.py | F.28 analytic check at t = +-4 (needs rootnum.py, eps.py) | runs | conductors consistent with a functional equation of sign +-1: [(5243616, {2: 5, 3: 4, 7: 1 |
| val.py | F.22 valuation laws; doubling raises the formal-group depth | runs | n=4: lambda=1, chi4(N)*(-1)^Omega1=1 |

Older versions of the Picard-number analysis (`analyze.py`, `classify_all.py`) explore all candidate L-functions without using the sign rule; the version used for the conclusions of F.44–F.46 is `../lfunc.py`.
