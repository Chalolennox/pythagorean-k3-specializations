clear;
print "============================================";
print "GEOMETRIC SIDON CERTIFICATE";
print "============================================";
p := 2621;
assert IsPrime(p);
K := GF(p);
R<x> := PolynomialRing(K);
E := EllipticCurve([K!0, K!(-2), K!0, K!2, K!0]);
h := x^6 - 6*x^5 - 15*x^4 + 100*x^3
     - 189*x^2 + 162*x - 54;
Y := x^3 - 2*x^2 + 2*x;
assert GCD(h, Derivative(h)) eq R!1;
assert GCD(h, Y) eq R!1;
print "Prime:", p;
print "Curve:", E;
print "Factorization:", Factorization(h);
D := [];
for r in Roots(h) do
    a := r[1];
    for s in Roots(x^2 - Evaluate(Y, a)) do
        Append(~D, E![a, s[1], K!1]);
    end for;
end for;
assert #D eq 12;
assert #Seqset(D) eq 12;
print "Number of points:", #D;
for Q in D do
    print Q;
end for;
O := E!0;
Sums := [];
Pairs := [];
ZeroCount := 0;
Collisions := 0;
print "--------------------------------------------";
print "Checking unordered pair sums";
print "--------------------------------------------";
for i in [1..#D] do
    for j in [i..#D] do
        S := D[i] + D[j];
        if S eq O then
            ZeroCount +:= 1;
            continue;
        end if;
        k := Index(Sums, S);
        if k ne 0 then
            Collisions +:= 1;
            print "COLLISION";
            print "Previous pair:", Pairs[k];
            print "Current pair:", <i,j>;
            print "Common sum:", S;
        end if;
        Append(~Sums, S);
        Append(~Pairs, <i,j>);
    end for;
end for;
XCoords := { S[1] : S in Sums };
TwoTorsionCount := #[ S : S in Sums | 2*S eq O ];
print "--------------------------------------------";
print "RESULTS";
print "--------------------------------------------";
print "Total unordered pairs:", 78;
print "Zero sums:", ZeroCount;
print "Nonzero sums:", #Sums;
print "Distinct nonzero sums:", #Seqset(Sums);
print "Distinct x-coordinates:", #XCoords;
print "Nonzero 2-torsion sums:", TwoTorsionCount;
print "Nontrivial collisions:", Collisions;
assert ZeroCount eq 6;
assert #Sums eq 72;
assert #Seqset(Sums) eq 72;
assert #XCoords eq 36;
assert TwoTorsionCount eq 0;
assert Collisions eq 0;
print "============================================";
print "GEOMETRIC SIDON CERTIFICATE: PASS";
print "============================================";
