// Standalone replay of owner certificate, 27 Nov 2026.
// Filtering is unnecessary for replay: successful vector (1,0,0,0).
// No absolute field conversions. This compact replay is not independently run.
Q := Rationals();
R<X> := PolynomialRing(Q);
function AdjoinRoot(K,d)
    d := K!d;
    if d eq 0 then return K,K!0,1; end if;
    ok,r := IsSquare(d);
    if ok then
        assert r^2 eq d;
        return K,r,1;
    end if;
    RK<Z> := PolynomialRing(K);
    L<r> := ext<K | Z^2-d>;
    assert r^2 eq L!d;
    return L,r,2;
end function;
function HalvePoint(K,px,py,ii)
    K1,r1,d1 := AdjoinRoot(K,px);
    px := K1!px; py := K1!py; ii := K1!ii;
    K2,r2,d2 := AdjoinRoot(K1,px-1-ii);
    px := K2!px; py := K2!py; ii := K2!ii; r1 := K2!r1;
    if r1*r2 ne 0 then
        K3 := K2; r3 := -py/(r1*r2); d3 := 1;
    else
        K3,r3,d3 := AdjoinRoot(K2,px-1+ii);
    end if;
    px := K3!px; py := K3!py; ii := K3!ii;
    r1 := K3!r1; r2 := K3!r2; r3 := K3!r3;
    assert r1^2 eq px;
    assert r2^2 eq px-1-ii;
    assert r3^2 eq px-1+ii;
    assert r1*r2*r3 eq -py;
    w := r1*r2+r1*r3+r2*r3;
    hx := px+w; hy := -py-(r1+r2+r3)*w;
    E := EllipticCurve([K3!0,-2,0,2,0]);
    assert 2*(E![hx,hy,1]) eq E![px,py,1];
    return K3,hx,hy,ii,d1*d2*d3;
end function;
K<ii> := NumberField(X^2+1);
aX := K!0; aY := K!0; bX := 1+ii; bY := K!0;
level := 2; fieldDegree := 2;
while level lt 16 do
    print "Lifting torsion level:",level;
    L,newAX,newAY,newI,dA := HalvePoint(K,aX,aY,ii);
    print "First generator: PASS";
    M,newBX,newBY,finalI,dB := HalvePoint(L,L!bX,L!bY,newI);
    print "Second generator: PASS";
    aX := M!newAX; aY := M!newAY; bX := newBX; bY := newBY;
    K := M; ii := finalI;
    fieldDegree *:= dA*dB; level *:= 2;
    E := EllipticCurve([K!0,-2,0,2,0]);
    A := E![aX,aY,1]; B := E![bX,bY,1];
    assert (level div 2)*A eq E![0,0,1];
    assert (level div 2)*B eq E![1+ii,0,1];
    assert level*A eq E!0; assert level*B eq E!0;
    print "Full torsion level:",level;
    print "Absolute degree:",fieldDegree;
end while;
assert fieldDegree eq 512;
print "T_16 CONSTRUCTION: PASS";
z16 := WeilPairing(A,B,16);
assert z16^8 eq -1;
ok,z32 := IsSquare(z16);
assert ok; assert z32^2 eq z16; assert z32^16 eq -1;
print "Primitive 32nd root: VERIFIED";
ok,a := IsSquare(K!2);
assert ok;
rx := 2-a; ry := 2-2*a;
P := E![1,1,1];
assert 2*(E![rx,ry,1]) eq P;
L,sx,sy,newI,dS := HalvePoint(K,rx,ry,ii);
assert dS eq 1;
S := E![sx,sy,1]; assert 4*S eq P;
print "Quarter point: VERIFIED";
u := [aX,aX-1-ii,bX,bX-1-ii];
target := sx/z32;
assert target ne 0; assert &and[t ne 0 : t in u];
// Try certified vector first; fallback covers choices of radicals.
candidates := [[1,0,0,0]] cat [v : v in [[e1,e2,e3,e4] : e1,e2,e3,e4 in [0,1]] | v ne [1,0,0,0]];
proved := false;
for v in candidates do
    print "Testing candidate:",v;
    prod := &*[u[j]^v[j] : j in [1..4]];
    ok,w := IsSquare(target/prod);
    if ok then
        assert w^2*prod*z32 eq sx;
        print "EXACT SQUARE-CLASS CERTIFICATE: PASS";
        print "Exponent vector:",v;
        proved := true;
        break;
    end if;
end for;
assert proved;
print "POSITIVE CONTAINMENT IN T_64: PROVED";
