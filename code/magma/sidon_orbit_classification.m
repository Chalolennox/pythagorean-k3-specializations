// Reconstructed standalone verification script; owner ran equivalent split scripts.
clear;
C := [5,7,19,23,41,83,97,103,113,157,257,4583,55009,64811,70297,96001,103967,138679,248389,519521,609571,43185607,254717627,280937621,990716219,7170845597,30358338574451,45886915050671,1531941337378691479,344440033300531101843589,12171150351860362096713064958322911,1203273355205525581931059818759348924273956480384606123,5136714670616930401674408573902323936996380257286318245563];
assert #C eq 33;
function MaxDiff(D,E)
    Shifts := []; Counts := [];
    for A in D do
        for B in D do
            r := A-B;
            if r ne E!0 then
                j := Index(Shifts,r);
                if j eq 0 then
                    Append(~Shifts,r); Append(~Counts,1);
                else
                    Counts[j] +:= 1;
                end if;
            end if;
        end for;
    end for;
    assert &+([0] cat Counts) eq #D*(#D-1);
    return Maximum([0] cat Counts), [Shifts[j] : j in [1..#Shifts] | Counts[j] gt 2];
end function;
checked := 0;
for p in C do
    assert IsPrime(p);
    K := GF(p); R<x> := PolynomialRing(K);
    E := EllipticCurve([K!0,K!(-2),K!0,K!2,K!0]);
    h := x^6-6*x^5-15*x^4+100*x^3-189*x^2+162*x-54;
    D := []; S := [];
    for a in Roots(h) do
        xx := a[1]; yy := xx^3-2*xx^2+2*xx;
        t := 1-xx; g := 2*t*(1-t^2);
        for b in Roots(x^2-yy) do
            Q := E![xx,b[1],K!1];
            Append(~D,Q);
            if g ne 0 and IsSquare(g) then Append(~S,Q); end if;
        end for;
    end for;
    dm,db := MaxDiff(D,E); sm,sb := MaxDiff(S,E);
    print p,#D,#S,dm,sm,#db,#sb;
    assert dm le 4;
    if p eq 519521 then
        P := E![1,1,1]; T := E![0,0,1];
        assert sm eq 4 and sb eq [T];
        assert #E eq 519312 and Order(P) eq 698;
        assert 349*P eq T;
        Orbit := {n*P : n in [0..697]};
        assert #Orbit eq 698;
        assert #[Q : Q in S | Q in Orbit] eq 0;
    else
        assert sm le 2;
    end if;
    checked +:= 1;
end for;
assert checked eq 33;
print "ORBIT SIDON CLASSIFICATION PASS";
