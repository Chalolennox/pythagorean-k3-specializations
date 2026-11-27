clear;
p := 125329;
assert IsPrime(p) and p mod 8 eq 1;
F := GF(p);
R<x> := PolynomialRing(F);
h := (1-x)^6-30*(1-x)^4-24*(1-x)^2-1;
assert IsSquarefree(h);
xx := Sort([Integers()!r[1] : r in Roots(h)]);
assert xx eq [10263,37280,45627,79704,88051,115068];
ok,ii := IsSquare(F!(-1)); assert ok;
bits := [];
for a in xx do
 u := F!a;
 Y := u*(u^2-2*u+2);
 assert Y ne 0 and IsSquare(Y);
 assert IsSquare(u);
 assert u-1-ii ne 0;
 Append(~bits, IsSquare(u-1-ii) select 0 else 1);
end for;
print "Roots:",xx;
print "Second descent bits:",bits;
assert bits eq [1,0,0,0,0,1];
for j in [1..6] do
 assert (xx[j]+xx[7-j]) mod p eq 2;
end for;
print "Unit-vector witness: PASS";
