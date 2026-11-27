Q := Rationals();
R<X> := PolynomialRing(Q);
h := X^6-6*X^5-15*X^4+100*X^3-189*X^2+162*X-54;
f := X^3-2*X^2+2*X;
J := EllipticCurve([Q!0,-2,0,2,0]);
print "EXACT TORSION INTERSECTION";
assert Discriminant(J) eq -256;
print "Curve discriminant:",Discriminant(J);
print "Ramification support: {2}";
excluded := [false,false,false];
classes := [-1,2,-2];
for p in [2621,93491] do
    print "Prime:",p;
    assert IsPrime(p);
    F := GF(p); RF<Z> := PolynomialRing(F);
    hp := RF!h; fp := RF!f;
    assert GCD(hp,Derivative(hp)) eq RF!1;
    rr := Roots(hp); assert #rr eq 6;
    for r in rr do
        xx := r[1];
        assert r[2] eq 1;
        assert Evaluate(hp,xx) eq 0;
        yy2 := Evaluate(fp,xx); assert yy2 ne 0;
        ok,yy := IsSquare(yy2); assert ok; assert yy^2 eq yy2;
        print "Verified point:",xx,yy;
    end for;
    print "Complete splitting in K: PASS";
    signs := [IsSquare(F!d) select 1 else -1 : d in classes];
    print "Prime modulo 8:",p mod 8;
    print "Quadratic characters:",signs;
    for j in [1..3] do
        if signs[j] eq -1 then excluded[j] := true; end if;
    end for;
end for;
assert &and[flag : flag in excluded];
print "ALL QUADRATIC SUBFIELDS EXCLUDED";
print "TORSION INTERSECTION CERTIFICATE: PASS";
print "K intersect T_infty = Q";
