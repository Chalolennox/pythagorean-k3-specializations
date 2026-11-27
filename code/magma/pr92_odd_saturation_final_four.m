// Reconstructed from owner-executed Magma certificates, 2026-11-27.
Z := Integers();
R<X> := PolynomialRing(Rationals());
h := X^6-6*X^5-15*X^4+100*X^3-189*X^2+162*X-54;
f := X^12-66*X^10-29922*X^8+73214*X^6-62559*X^4+22032*X^2-3456;
assert IsIrreducible(f);
F<z> := NumberField(f);
S<W> := PolynomialRing(F);
g := GCD(S!h,W^3-2*W^2+2*W-z^2);
assert Degree(g) eq 1;
u := -Coefficient(g,0)/Coefficient(g,1);
J := EllipticCurve([F!0,F!(-2),F!0,F!2,F!0]);
U := J![u,z,1];
T, mp := TorsionSubgroup(J);
assert #T eq 2;
C := [
[8431,2123831,2124612,1566839,703827,1895189,199072],
[6841,2136527,2134392,1706561,635147,1458897,1616987],
[5167,2302987,2304482,1823048,98124,2285848,162389],
[8627,2487581,2484576,2113923,169161,672642,955731]
];
D := Z!Discriminant(f);
for c in C do
 l := c[1]; p := c[2]; N := c[3];
 assert IsPrime(l) and IsPrime(p) and p gt 3;
 assert D mod p ne 0;
 k := GF(p);
 A<t> := PolynomialRing(k);
 E := EllipticCurve([k!0,k!(-2),k!0,k!2,k!0]);
 assert #E eq N and N mod l eq 0;
 x := k!c[4]; y := k!c[5];
 assert Evaluate(A!f,y) eq 0;
 gp := GCD(A!h,t^3-2*t^2+2*t-y^2);
 assert Degree(gp) eq 1 and Evaluate(gp,x) eq 0;
 V := (N div l)*E![x,y,1];
 assert V ne E!0 and l*V eq E!0;
 assert V eq E![k!c[6],k!c[7],1];
 print "PASS", l,p,N;
end for;
print "FINAL FOUR CERTIFICATES: PASS";
