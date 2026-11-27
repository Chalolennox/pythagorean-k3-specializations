clear;
Qx<x> := PolynomialRing(Rationals());
h := (1-x)^6-30*(1-x)^4-24*(1-x)^2-1;
function SplitPoints(p,h)
 F := GF(p); R<X> := PolynomialRing(F);
 hp := R!h;
 if not IsSquarefree(hp) then return false, []; end if;
 rt := Roots(hp);
 if #rt ne 6 then return false, []; end if;
 E := EllipticCurve([F!0,F!(-2),F!0,F!2,F!0]);
 pts := [];
 for r in rt do
  a := r[1]; Y := a^3-2*a^2+2*a;
  if Y eq 0 then return false, []; end if;
  ok,b := IsSquare(Y);
  if not ok then return false, []; end if;
  Append(~pts,E![a,b,1]);
 end for;
 return true,pts;
end function;
print "KUMMER SATURATION AT 3 AND 23";
ok,pts := SplitPoints(2621,h); assert ok;
E := Parent(pts[1]); N := #E;
assert N eq 2680 and N mod 3 ne 0 and N mod 23 ne 0;
print "Torsion certificate:",2621,N;
for row in [<3,113819,113730,true>,<3,49253,49536,false>,<23,229469,229080,true>,<23,229469,229080,false>] do
 l,p,N0,isP := Explode(row);
 ok,pts := SplitPoints(p,h); assert ok;
 E := Parent(pts[1]); N := #E;
 assert N eq N0 and N mod l eq 0;
 if isP then pts := [E![1,1,1]]; end if;
 found := false;
 for U in pts do
  V := (N div l)*U;
  if V ne E!0 then
   print "PASS:",l,p,N,isP,U,V;
   found := true; break;
  end if;
 end for;
 assert found;
end for;
print "3-SATURATION: PASS";
print "23-SATURATION: PASS";
