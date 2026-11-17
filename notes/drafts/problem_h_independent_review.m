// Provenance: uploaded to the chat by the repository owner on 17 November 2026 as problem_h_independent_review.m (Magma V2.30 script of the dossier problem_h_independent_review.md in this directory).
// Reviewed in notes/REVIEW_2026-11-17_problem_h_dossier.md. The text below the line of slashes is unmodified.

///////////////////////////////////////////////////////////////////////////
// PROBLEM H -- INDEPENDENT REVIEW DOSSIER (Magma V2.30)
//
// Two distinct claims are examined:
//  (A) disjoint qualifying-prime sets at consecutive orbit indices;
//  (B) Chebotarev density of primes with NO qualifying roots.
//
// IMPORTANT STATUS: The resultant identity in (A) is exact and is
// independently reproducible below. The final consecutive-SET assertion
// additionally needs the exceptional-prime checks described below.
// The rational density 20867/24576 in (B) is a COMPUTATIONAL CANDIDATE,
// NOT yet a fully certified theorem: arithmetic identification of the
// degree-24 permutation action and Galois certification remain open.
// The existence of a rational Chebotarev density is unconditional.
//
// Curve C: y^2 = x^3 - 2*x^2 + 2*x, P=(1,1), T=(0,0).
// t(Q)=1-x(Q). Qualifying sets refer to the nP branch unless stated.
///////////////////////////////////////////////////////////////////////////

QQ := Rationals();
ZZ := Integers();
Z<t> := PolynomialRing(QQ);
ZU<u> := PolynomialRing(Z);
H := t^6 - 30*t^4 - 24*t^2 - 1;
Hu := u^6 - 30*u^4 - 24*u^2 - 1;

///////////////////////////////////////////////////////////////////////////
// PART A. CONSECUTIVE QUALIFYING PRIME SETS
//
// Write t=t(Q), u=t(Q+P). The addition law on C yields
//    Phi(t,u)=(t^2*u-t+2)^2-4*(1-t)*(1+t^2)=0.
// (The polynomial equation is a necessary relation; possible exceptional
// denominators must be handled separately in applications.)
//
// A prime p>=5 which divides the sextic at BOTH consecutive orbit
// parameters, with both parameters finite and p-integral, must make
// H(t)=H(u)=Phi(t,u)=0 mod p, subject to denominator exceptions.
// Thus it divides the integer resultant below. This is a necessary
// condition for common BAD primes, not sufficient for qualifying primes.
//
// The claimed exact factorization is:
//  2^18 * 3^30 * 7 * 103 * 113^3 * 13085561^2.
// Hence possible common primes >=5 are 7,103,113,13085561.
//
// Previous computations report that 7,103,113 do not yield a qualifying
// consecutive pair and 13085561 is nonqualifying. Those finite checks
// should be independently reproduced, including the finite/projective
// denominator cases, before claiming Q_n cap Q_(n+1) = empty for ALL n.
///////////////////////////////////////////////////////////////////////////

print "========== PART A: CONSECUTIVE RESULTANT ==========";
Phi := (t^2*u - t + 2)^2 - 4*(1-t)*(1+t^2);
R := Resultant(Phi, Hu);
D := Resultant(H, R);
Expected := ZZ!2^18 * ZZ!3^30 * ZZ!7 * ZZ!103 * ZZ!113^3 * ZZ!13085561^2;
assert Abs(ZZ!D) eq Expected;
assert Degree(GCD(H,R)) eq 0;
print "Exact resultant factorization:", Factorization(Abs(ZZ!D));
print "GCD over Q has degree", Degree(GCD(H,R));
print "Exceptional candidate primes >=5:", [7,103,113,13085561];

// Check whether an exceptional prime has a common AFFINE geometric pair.
// These are necessary-condition checks, not a replacement for orbit
// membership or for all exceptional reduction configurations.
for p in [7,103,113,13085561] do
    F := GF(p);
    FZ<a> := PolynomialRing(F);
    FH := a^6 - 30*a^4 - 24*a^2 - 1;
    FR := FZ!R;
    Common := GCD(FH,FR);
    printf "p=%o; gcd degree=%o; gcd=%o\n", p, Degree(Common), Common;
end for;

///////////////////////////////////////////////////////////////////////////
// PART B. DENSITY OF EMPTY QUALIFYING-ROOT SETS
//
// For p>=5, away from finitely many exceptions, a qualifying root a in Fp
// is a root of H satisfying:
//   q(a)=2*a*(1-a^2)/(1+a^2)^2 is a NONZERO square;
//   r(a)=(1-a)*(1+a^2) is a NONZERO square;
//   if (2/p)=+1, x(a)=1-a is additionally a square.
// Define Q_p as the set of such a. We count p with Q_p=empty.
//
// Define degree-24 and degree-48 resolvents Rm and Rp. In a splitting
// field, roots are respectively
//   +/-sqrt(q(a)) +/-sqrt(r(a)),
//   +/-sqrt(q(a)) +/-sqrt(r(a)) +/-sqrt(x(a))
// for the six roots a of H (with generic sign choices).
//
// Chebotarev: each root/existence condition is a Frobenius fixed-point
// condition in a finite Galois extension L/Q. Consequently the density
// exists and is rational (outside a finite exceptional set).
//
// PREVIOUS MAGMA COMPUTATIONS, TO BE INDEPENDENTLY CERTIFIED:
//  |Gal(L/Q)| = 24576.
//  |{g: g has no fixed point on degree-24 action}| = 19709.
//  |{g: g has no fixed point on degree-48 action}| = 22035.
//  sqrt(2) is contained in L.
//  In chi_2=+1 coset: 11013 elements have no fixed point in degree 48.
//  In chi_2=-1 coset: 9854 elements have no fixed point in degree 24.
//  Candidate empty density: (11013+9854)/24576 = 20867/24576.
//
// CRITICAL GAP: the 9854 count was inferred using one of two invariant
// pairings matching the degree-24 total fixed-point-free count. Equality
// of those totals alone DOES NOT arithmetically identify the Rm action.
// Also the computed Galois group still needs a certified Galois proof.
// Therefore the numerical density is NOT labelled a proved theorem here.
///////////////////////////////////////////////////////////////////////////

print "========== PART B: RESOLVENTS ==========";
Fz := FieldOfFractions(Z);
TT<v> := PolynomialRing(Fz);
Fv := FieldOfFractions(TT);
vv := Fv!v;
zz := Fv!(Fz!t);
HH := v^6 - 30*v^4 - 24*v^2 - 1;
q := 2*vv*(1-vv^2)/(1+vv^2)^2;
r := (1-vv)*(1+vv^2);
x := 1-vv;

// Build polynomials in t with rational coefficients.
Rm := PrimitivePart(Numerator(Resultant(HH,
      Numerator((zz^2-q-r)^2-4*q*r))));
Epart := zz^4+6*zz^2*x+x^2-2*(q+r)*(zz^2+x)+(q-r)^2;
Opart := 4*zz*(zz^2+x-q-r);
Rp := PrimitivePart(Numerator(Resultant(HH,
      Numerator(Epart^2-x*Opart^2))));
assert Degree(Rm) eq 24;
assert Degree(Rp) eq 48;
assert IsIrreducible(Rm);
assert IsIrreducible(Rp);
print "Degree(Rm)=", Degree(Rm), "; degree(Rp)=", Degree(Rp);
print "Both resolvents irreducible: true";

// Optional expensive group verification. Set to true for independent run.
DO_GALOIS := false;
if DO_GALOIS then
    print "Computing Galois group of degree-48 resolvent...";
    G, roots, S := GaloisGroup(Rp);
    print "Computed group order:", #G;
    assert #G eq 24576;
    print "This is a group computation, not a formal GaloisProof.";
    print "Independent review still requires identifying the degree-24 action";
    print "and obtaining a certified Galois proof.";
end if;

// Exact arithmetic showing sqrt(2) lies in the radical splitting field:
// Put u_i=t_i^2 for one representative of each +/- pair of roots of H.
// The u_i are roots of U^3-30U^2-24U-1.
// For v_i=1+u_i, their product is 8 (evaluate the cubic at -1).
// Since r(t_i)/x(t_i)=1+t_i^2=1+u_i, the splitting field containing
// sqrt(r(t_i)) and sqrt(x(t_i)) contains sqrt(1+u_i).
// Their product is +/-sqrt(8)=+/-2sqrt(2), so sqrt(2) lies in L.
W<w> := PolynomialRing(QQ);
Cubic := w^3 - 30*w^2 - 24*w - 1;
assert -Evaluate(Cubic,-1) eq 8;
print "Radical identity: product_i (1+u_i) = 8; hence sqrt(2) in L.";

// Exact candidate fraction, deliberately not a certified Galois count.
Candidate := QQ!(11013+9854)/24576;
assert Candidate eq QQ!20867/24576;
print "Candidate empty density:", Candidate;
print "Candidate nonempty density:", 1-Candidate;
print "STATUS: CONDITIONAL on action identification and Galois certification.";

///////////////////////////////////////////////////////////////////////////
// PART C. INDEPENDENT FINITE-PRIME CHECK (SMALL BOUND)
// These frequencies are evidence, not a proof of the limiting density.
///////////////////////////////////////////////////////////////////////////

print "========== PART C: FINITE-PRIME CHECK ==========";
MAX_P := 20000;
Total := 0;
Nonempty := 0;
OrbitNonempty := 0;
for p in PrimesUpTo(MAX_P) do
    if p lt 5 then continue; end if;
    Total +:= 1;
    F := GF(p);
    PF<a> := PolynomialRing(F);
    Hp := a^6-30*a^4-24*a^2-1;
    E := EllipticCurve([F!0,F!(-2),F!0,F!2,F!0]);
    P := E![F!1,F!1,F!1];
    T2 := E![F!0,F!0,F!1];
    O := E!0;
    qualifyingX := {F|};
    for rt in Roots(Hp) do
        aa := rt[1];
        den := 1+aa^2;
        if den eq 0 then continue; end if;
        qq := 2*aa*(1-aa^2)/den^2;
        xx := 1-aa;
        rr := xx*den;
        if qq eq 0 or rr eq 0 then continue; end if;
        if not IsSquare(qq) or not IsSquare(rr) then continue; end if;
        if IsSquare(F!2) and not IsSquare(xx) then continue; end if;
        Include(~qualifyingX,xx);
    end for;
    if #qualifyingX eq 0 then continue; end if;
    Nonempty +:= 1;
    // Search reduced nP and nP+T, with exact periodic stopping.
    Q := O;
    hit := false;
    repeat
        if Q ne O and Q[1] in qualifyingX then hit := true; end if;
        QT := Q+T2;
        if QT ne O and QT[1] in qualifyingX then hit := true; end if;
        Q +:= P;
    until Q eq O or hit;
    if hit then OrbitNonempty +:= 1; end if;
end for;
print "Primes p>=5:", Total;
print "Primes with qualifying roots:", Nonempty;
print "Primes with qualifying roots in reduced orbit:", OrbitNonempty;
print "Excluded by orbit:", Nonempty-OrbitNonempty;
print "Expected prior run at bound 20000: 2260, 348, 263, 85";
print "Candidate density is NOT established by finite prime counts.";
print "========== REVIEW DOSSIER COMPLETE ==========";
