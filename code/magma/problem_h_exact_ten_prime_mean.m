// Problem H: exact parity means for two ten-prime sets
// Magma V2.30-1; standalone. Uses generalized CRT inclusion-exclusion.
// See notes/problem_h_finite_prime_correlations.md.
ZZ := Integers(); QQ := Rationals(); RR := RealField(30);
A := [83,547,307,149,197,757,823,631,9391,2293];
B := [83,673,1009,557,617,397,823,491,1229,1289];
function Split(Q,F)
    if IsId(Q) then return false; end if;
    t := F!1-Q[1];
    if t^6-30*t^4-24*t^2-1 ne F!0 then return false; end if;
    g := F!2*t*(F!1-t^2);
    assert g ne F!0;
    return IsSquare(g);
end function;
function Events(p,branch)
    F := GF(p);
    E := EllipticCurve([F!0,F!(-2),F!0,F!2,F!0]);
    P := E![F!1,F!1,F!1]; T := E![F!0,F!0,F!1];
    m := ZZ!Order(P);
    Q := E!0;
    if branch eq 2 then Q := T; end if;
    S := [];
    for j in [0..m div 2] do
        if Split(Q,F) then
            Append(~S,j);
            if j ne 0 and 2*j ne m then Append(~S,m-j); end if;
        end if;
        Q := Q+P;
    end for;
    return m,S;
end function;
function CRT(r,m,s,k)
    d := GCD(m,k);
    if (s-r) mod d ne 0 then return false,ZZ!0,ZZ!1; end if;
    L := LCM(m,k); k1 := k div d;
    if k1 eq 1 then return true,r mod L,L; end if;
    u := (((s-r) div d)*InverseMod((m div d) mod k1,k1)) mod k1;
    return true,(r+m*u) mod L,L;
end function;
procedure Explore(i,r,m,c,periods,sets,~total,~nodes,~leaves)
    nodes +:= 1;
    if i gt #periods then
        total +:= QQ!c/QQ!m;
        leaves +:= 1;
        return;
    end if;
    Explore(i+1,r,m,c,periods,sets,~total,~nodes,~leaves);
    for s in sets[i] do
        ok,r1,m1 := CRT(r,m,s,periods[i]);
        if ok then
            Explore(i+1,r1,m1,-2*c,periods,sets,~total,~nodes,~leaves);
        end if;
    end for;
end procedure;
procedure Run(label,primes,branch,expected)
    print "============================================";
    print "Branch:",label;
    periods := []; sets := []; independent := QQ!1; L := ZZ!1;
    for p in primes do
        m,S := Events(p,branch);
        Append(~periods,m); Append(~sets,S);
        independent *:= 1-QQ!(2*#S)/QQ!m;
        L := LCM(L,m);
        print "p =",p,"period =",m,"events =",#S;
    end for;
    print "Joint period:",L;
    total := QQ!0; nodes := ZZ!0; leaves := ZZ!0;
    Explore(1,ZZ!0,ZZ!1,ZZ!1,periods,sets,~total,~nodes,~leaves);
    print "Independent mean:",RR!independent;
    print "Exact parity mean:",RR!total;
    print "Exact minus independent:",RR!(total-independent);
    print "Nodes:",nodes,"Leaves:",leaves;
    assert Abs(RR!total-expected) lt RR!10^(-20);
    print "Regression: PASS";
end procedure;
Run("nP",A,1,RR!583861991833028828656755278093 / RR!10^30);
Run("nP+T",B,2,RR!718215686108091026369471223623 / RR!10^30);
print "COMPLETE";
