// Reconstructed clean certificate from the conversation of 24 Nov 2026.
// User confirmed execution on 24 Nov 2026; reported CPU 0.070 s.
// Output: notes/data/eligible_triple_geometry_20261124.txt.
Z:=Integers();
function h(x)
 return x^6-6*x^5-15*x^4+100*x^3-189*x^2+162*x-54;
end function;
function Y(x)
 return x^3-2*x^2+2*x;
end function;
function g(t)
 return 2*t*(1-t^2);
end function;
function dp(x)
 a:=(x^2-2)^2; b:=4*Y(x);
 return a^6-6*a^5*b-15*a^4*b^2+100*a^3*b^3-189*a^2*b^4+162*a*b^5-54*b^6;
end function;
function pts(K,eligible)
 E:=EllipticCurve([K!0,K!(-2),K!0,K!2,K!0]);
 assert Discriminant(E) ne 0;
 R<x>:=PolynomialRing(K); S:=[];
 for r in Roots(h(x)) do
  a:=r[1]; c:=g(1-a);
  if not eligible or (c ne 0 and IsSquare(c)) then
   for s in Roots(x^2-Y(a)) do Append(~S,E![a,s[1],1]); end for;
  end if;
 end for;
 return E,S;
end function;
function triples(S)
 return [<a,b,a+b>: a,b in S | a+b in S];
end function;
start:=Cputime();
print "Geometry";
E,D:=pts(GF(5^6),false);
assert #D eq 12;
assert #triples(D) eq 0;
print "Geometry PASS";
Ru<u>:=PolynomialRing(Z); Rx<x>:=PolynomialRing(Ru); Rz<z>:=PolynomialRing(Rx);
xx:=Rz!x; uu:=Rz!(Rx!u);
q,r:=Quotrem(h(z)-h(xx),z-xx); assert r eq 0;
B:=(uu-2+xx+z)*(xx-z)^2-Y(xx)-Y(z);
F,r:=Quotrem(B^2-4*Y(xx)*Y(z),(xx-z)^2); assert r eq 0;
print "Resultants";
A:=Abs(Z!Resultant(h(u),Resultant(h(x),Resultant(q,F) mod h(x))));
R<s>:=PolynomialRing(Z);
C:=Abs(Z!Resultant(h(s),dp(s)));
N:=[A,C,Abs(Z!Discriminant(h(s))),Abs(Z!Resultant(h(s),Y(s)))];
pr:={};
for n in N do
 fac:=Factorization(n); print n,fac;
 assert &*[a[1]^a[2]:a in fac] eq n;
 for a in fac do
  assert IsPrime(a[1]);
  if a[1] ge 5 then Include(~pr,a[1]); end if;
 end for;
end for;
L:=Sort(Setseq(pr));
assert L eq [7,19,23,31,71,83,229,797,5087,7351,12113,363773,609613,9624457993,1386618529213,49635479695149757];
Suv:=[];
for p in L do
 E,D:=pts(GF(p),false); E,S:=pts(GF(p),true);
 T:=triples(S); print p,#D,#S,#triples(D),#T,T;
 if #T gt 0 then Append(~Suv,p); end if;
end for;
assert Suv eq [229,609613,1386618529213];
print "Geometry and candidate classification PASS",Cputime(start);
