// Owner certificates recorded 2026-11-27; consolidated replay not yet run.
for p in [8956097,2738753] do
    print "Prime:",p;
    assert IsPrime(p) and p mod 128 eq 65;
    F := GF(p);
    E := EllipticCurve([F!0,-2,0,2,0]);
    T := E![0,0,1]; O := E!0;
    if p eq 8956097 then
        A := E![8023164,4886572,1];
        B := E![3491812,6904152,1];
        assert #E eq 8953856;
    else
        A := E![2419569,1057284,1];
        B := E![2701647,1471702,1];
        assert #E eq 2736128;
    end if;
    assert 32*A eq T and 2*T eq O and T ne O;
    assert 64*B eq O and 32*B ne O and 32*B ne T;
    print "Full T64: PASS";
    if p eq 8956097 then
        U := E![3305919,2881857,1];
        assert 2*U eq A and 64*U eq T;
        print "Trace=1, first column zero: PASS";
    else
        K := GF(p^2);
        EK := EllipticCurve([K!0,-2,0,2,0]);
        AK := EK![K!A[1],K!A[2],1];
        halves := DivisionPoints(AK,2);
        assert #halves eq 4;
        for U in halves do
            assert 2*U eq AK;
            FU := EK![U[1]^p,U[2]^p,U[3]^p];
            D := FU-U;
            assert D eq EK![1532999,0,1];
            assert D ne EK!0 and D ne EK![0,0,1];
            assert 2*D eq EK!0;
        end for;
        print "c=1: PASS";
    end if;
end for;
print "All three invariant hyperplanes excluded.";
print "FULL CONGRUENCE KERNEL: PASS";
