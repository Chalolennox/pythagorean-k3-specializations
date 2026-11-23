////////////////////////////////////////////////////////////////////////
// PROBLEM H: OPTIMIZED TWO-BRANCH ADDITION FORMULA
// Magma V2.30-1, standalone; NOT independently executed.
//
// Find roots of H modulo p before constructing any orbit.
// For split roots, solve Q = nP or Q = nP+T using BSGS.
// One baby-step table is shared by both branches.
//
// Print exact finite-N sign-flip counts after EVERY prime cutoff.
// The full global root number is NOT computed.
////////////////////////////////////////////////////////////////////////
ZZ := Integers();
QQ := Rationals();
RR := RealField(25);

MAX_N := 100000;
BOUNDS := [1000,5000,20000,100000];
DO_REGRESSION := true;
REGRESSION_PRIMES := [83,149,197,307];

print "==============================================";
print "PROBLEM H: OPTIMIZED ADDITION FORMULA";
print "N =", MAX_N, "bounds =", BOUNDS;
print "==============================================";

function SplitTargets(p)
    F := GF(p);
    R<t> := PolynomialRing(F);
    H := t^6-30*t^4-24*t^2-1;
    if Degree(GCD(H,Derivative(H))) gt 0 then
        return false, [], F;
    end if;
    xs := [];
    for pair in Roots(H) do
        a := pair[1];
        g := F!2*a*(F!1-a^2);
        if g ne F!0 and IsSquare(g) then
            Append(~xs,F!1-a);
        end if;
    end for;
    return true,xs,F;
end function;

function BabyTable(P,m)
    k := ZZ!Ceiling(Sqrt(RR!m));
    baby := AssociativeArray();
    Q := Parent(P)!0;
    for j in [0..k-1] do
        baby[Sprint(Q)] := j;
        Q +:= P;
    end for;
    return baby,k,-k*P;
end function;

function BSGS(Q,P,m,baby,k,giantStep)
    V := Q;
    for i in [0..k] do
        key := Sprint(V);
        if IsDefined(baby,key) then
            n := (i*k+baby[key]) mod m;
            if n*P eq Q then
                return true,n;
            end if;
        end if;
        V +:= giantStep;
    end for;
    return false,ZZ!0;
end function;

// Returns event positions for both branches, modulo ord(P).
// For branch 2, nP+T=Q is equivalent to nP=Q+T.
function BothEvents(p)
    valid,xs,F := SplitTargets(p);
    if not valid or #xs eq 0 then
        return valid,ZZ!1,[],[];
    end if;

    E := EllipticCurve([F!0,F!(-2),F!0,F!2,F!0]);
    P := E![F!1,F!1,F!1];
    T := E![F!0,F!0,F!1];
    m := ZZ!Order(P);
    baby,k,giantStep := BabyTable(P,m);
    S1 := []; S2 := [];

    for x in xs do
        rhs := x^3-2*x^2+2*x;
        if not IsSquare(rhs) then continue; end if;
        y := Sqrt(rhs);
        ys := [y];
        if y ne F!0 then Append(~ys,-y); end if;

        for yy in ys do
            Q := E![x,yy,F!1];
            ok1,n1 := BSGS(Q,P,m,baby,k,giantStep);
            if ok1 and n1 notin S1 then Append(~S1,n1); end if;
            ok2,n2 := BSGS(Q+T,P,m,baby,k,giantStep);
            if ok2 and n2 notin S2 then Append(~S2,n2); end if;
        end for;
    end for;

    return true,m,S1,S2;
end function;

// Small-prime validation against direct orbit scanning.
// This is a runtime test, not a claim that the script was pretested.
procedure CheckSmallPrime(p)
    valid,m,A,B := BothEvents(p);
    if not valid then
        print "Regression skipped (exceptional prime):",p;
        return;
    end if;
    F := GF(p);
    E := EllipticCurve([F!0,F!(-2),F!0,F!2,F!0]);
    P := E![F!1,F!1,F!1];
    T := E![F!0,F!0,F!1];
    Q := E!0;
    directA := []; directB := [];
    for n in [0..m-1] do
        for branch in [1,2] do
            V := Q;
            if branch eq 2 then V +:= T; end if;
            if not IsId(V) then
                t := F!1-V[1];
                h := t^6-30*t^4-24*t^2-1;
                g := F!2*t*(F!1-t^2);
                if h eq F!0 and g ne F!0 and IsSquare(g) then
                    if branch eq 1 then
                        Append(~directA,n);
                    else
                        Append(~directB,n);
                    end if;
                end if;
            end if;
        end for;
        Q +:= P;
    end for;
    assert Seqset(A) eq Seqset(directA);
    assert Seqset(B) eq Seqset(directB);
    print "Regression PASS p =",p,"period =",m,
          "branch counts =",#A,#B;
end procedure;

if DO_REGRESSION then
    print "Running BSGS/direct-orbit regression tests...";
    for p in REGRESSION_PRIMES do CheckSmallPrime(p); end for;
end if;

signs1 := [ZZ!1 : i in [1..MAX_N]];
signs2 := [ZZ!1 : i in [1..MAX_N]];
ind1 := QQ!1;
ind2 := QQ!1;
lower := 4;

for upper in BOUNDS do
    print "";
    print "==============================================";
    print "INTERVAL",lower+1,"TO",upper;
    print "==============================================";

    flips1 := [false : i in [1..MAX_N]];
    flips2 := [false : i in [1..MAX_N]];
    active1 := 0; active2 := 0;
    occurrences1 := 0; occurrences2 := 0;
    exceptional := 0; checked := 0;
    intervalInd1 := QQ!1; intervalInd2 := QQ!1;

    for p in PrimesUpTo(upper) do
        if p le lower or p lt 5 then continue; end if;
        checked +:= 1;
        valid,m,S1,S2 := BothEvents(p);
        if not valid then
            exceptional +:= 1;
            continue;
        end if;
        if #S1 gt 0 then
            active1 +:= 1;
            intervalInd1 *:= 1-QQ!(2*#S1)/QQ!m;
            for r in S1 do
                first := r;
                if first eq 0 then first := m; end if;
                if first le MAX_N then
                    for n in [first..MAX_N by m] do
                        flips1[n] := not flips1[n];
                        occurrences1 +:= 1;
                    end for;
                end if;
            end for;
        end if;
        if #S2 gt 0 then
            active2 +:= 1;
            intervalInd2 *:= 1-QQ!(2*#S2)/QQ!m;
            for r in S2 do
                first := r;
                if first eq 0 then first := m; end if;
                if first le MAX_N then
                    for n in [first..MAX_N by m] do
                        flips2[n] := not flips2[n];
                        occurrences2 +:= 1;
                    end for;
                end if;
            end for;
        end if;
    end for;

    ind1 *:= intervalInd1;
    ind2 *:= intervalInd2;
    print "Primes checked:",checked,
          "exceptional:",exceptional;
    print "Active split primes nP:",active1,
          "nP+T:",active2;

    for branch in [1,2] do
        if branch eq 1 then
            oldSigns := signs1;
            blockFlips := flips1;
            occurrences := occurrences1;
            model := ind1;
            label := "nP";
        else
            oldSigns := signs2;
            blockFlips := flips2;
            occurrences := occurrences2;
            model := ind2;
            label := "nP+T";
        end if;

        oldSum := ZZ!0;
        newSum := ZZ!0;
        A := ZZ!0;
        D := ZZ!0;
        flipCount := ZZ!0;
        newSigns := oldSigns;

        for n in [1..MAX_N] do
            s := oldSigns[n];
            oldSum +:= s;
            if blockFlips[n] then
                flipCount +:= 1;
                if s eq 1 then A +:= 1; else D +:= 1; end if;
                s := -s;
                newSigns[n] := s;
            end if;
            newSum +:= s;
        end for;

        assert newSum-oldSum eq 2*(D-A);
        assert flipCount eq A+D;
        assert flipCount le occurrences;

        oldMean := QQ!oldSum/MAX_N;
        newMean := QQ!newSum/MAX_N;
        delta := newMean-oldMean;
        flipProb := QQ!flipCount/MAX_N;
        covariance := QQ!(D-A)/MAX_N-oldMean*flipProb;
        // E[sigma_B * flip] = (A-D)/N
        // covariance = E[sigma_B * flip]-E[sigma_B]*E[flip].
        covariance := QQ!(A-D)/MAX_N-oldMean*flipProb;
        assert delta eq -2*(oldMean*flipProb+covariance);

        ratio := QQ!0;
        if flipCount gt 0 then ratio := QQ!Abs(D-A)/flipCount; end if;

        print "";
        print "BRANCH",label;
        print "old mean =",RR!oldMean;
        print "+ -> - =",A,"- -> + =",D;
        print "flip fraction =",RR!flipProb;
        print "cancellation ratio =",RR!ratio;
        print "covariance(old sign, flip) =",RR!covariance;
        print "independent contribution =",RR!(-2*oldMean*flipProb);
        print "covariance contribution =",RR!(-2*covariance);
        print "exact delta =",RR!delta;
        print "new mean =",RR!newMean;
        print "independent-prime model =",RR!model;
        print "actual minus model =",RR!(newMean-model);
        print "split-event occurrences =",occurrences;
        print "addition formula PASS";

        if branch eq 1 then signs1 := newSigns;
        else signs2 := newSigns;
        end if;
    end for;
    lower := upper;
    print "CUTOFF COMPLETE:",upper;
end for;
print "ALL CUTOFFS COMPLETE";
