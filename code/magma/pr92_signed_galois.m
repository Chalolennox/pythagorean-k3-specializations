// Archived equivalent of the owner-executed script (26 Nov 2026).
// Comments and formatting shortened; mathematical checks unchanged.
// Owner output: notes/data/pr92_signed_galois_output.txt.
Q := Rationals();
Qx<x> := PolynomialRing(Q);
H := x^6 - 30*x^4 - 24*x^2 - 1;
h := Evaluate(H, 1-x);
Y := x^3 - 2*x^2 + 2*x;
print "SIGNED GALOIS REPRESENTATION";
print "h(x) =", h;
print "Y(x) =", Y;
assert Degree(h) eq 6;
assert IsIrreducible(h);
assert GCD(h,Y) eq 1;
print "Irreducibility of h: PASS";
print "Discriminant of h:", Factorization(Integers()!Discriminant(h));
Qz<z> := PolynomialRing(Q);
Qzx<X> := PolynomialRing(Qz);
hh := &+[ Qzx!Coefficient(h,i)*X^i : i in [0..Degree(h)] ];
YY := X^3 - 2*X^2 + 2*X;
R := Resultant(hh,z^2-YY);
R := R/LeadingCoefficient(R);
print "STEP 1: RESULTANT";
print "R(z) =",R;
print "Degree =",Degree(R);
print "Squarefree =",IsSquarefree(R);
print "Irreducible =",IsIrreducible(R);
assert Degree(R) eq 12;
assert IsSquarefree(R);
assert IsIrreducible(R);
assert Evaluate(R,-z) eq R;
S := Resultant(hh,z-YY);
S := S/LeadingCoefficient(S);
print "STEP 2: Y-COORDINATE SEPARATION";
print "Polynomial of Y-values =",S;
print "Degree =",Degree(S);
print "Squarefree =",IsSquarefree(S);
assert Degree(S) eq 6;
assert IsSquarefree(S);
assert Evaluate(S,z^2) eq R;
print "Y-coordinate separation: PASS";
print "STEP 3: GALOIS GROUP";
start := Cputime();
G := GaloisGroup(R);
print "Galois computation time:",Cputime(start);
print "Group order =",#G;
print "Permutation degree =",Degree(G);
print "Transitive =",IsTransitive(G);
print "Generators:",Generators(G);
assert Degree(G) eq 12;
assert IsTransitive(G);
print "STEP 4: OPPOSITE-ROOT PAIRING";
gens := Setseq(Generators(G));
pairings := [];
for j in [2..12] do
    image := [0 : i in [1..12]];
    image[1] := j;
    queue := [1];
    pos := 1;
    valid := true;
    while pos le #queue and valid do
        a := queue[pos];
        pos +:= 1;
        for g in gens do
            b := a^g;
            c := image[a]^g;
            if image[b] eq 0 then
                image[b] := c;
                Append(~queue,b);
            elif image[b] ne c then
                valid := false;
                break;
            end if;
        end for;
    end while;
    if valid and #queue eq 12 then
        if #Seqset(image) eq 12 then
            involution := &and[image[image[i]] eq i : i in [1..12]];
            fixedfree := &and[image[i] ne i : i in [1..12]];
            if involution and fixedfree then
                Append(~pairings,image);
            end if;
        end if;
    end if;
end for;
print "Number of invariant opposite pairings:",#pairings;
assert #pairings ge 1;
if #pairings ne 1 then
    print "WARNING: Opposite pairing is not unique.";
    print pairings;
else
    opp := pairings[1];
    pairs := [{i,opp[i]} : i in [1..12] | i lt opp[i]];
    assert #pairs eq 6;
    print "Unique invariant pairing: PASS";
    print "Six geometric pairs:",pairs;
    reps := [Minimum(B) : B in pairs];
    print "Chosen representatives:",reps;
    print "STEP 5: EXACT CHARACTER COMPUTATION";
    function SignedTrace(g,reps,opp)
        tr := 0;
        for i in reps do
            j := i^g;
            if j eq i then
                tr +:= 1;
            elif j eq opp[i] then
                tr -:= 1;
            end if;
        end for;
        return tr;
    end function;
    sumchi := Integers()!0;
    sumchi2 := Integers()!0;
    count := 0;
    hist := AssociativeArray(Integers());
    for k in [-6..6] do
        hist[k] := 0;
    end for;
    start := Cputime();
    for g in G do
        chi := SignedTrace(g,reps,opp);
        sumchi +:= chi;
        sumchi2 +:= chi^2;
        hist[chi] +:= 1;
        count +:= 1;
        if count mod 10000 eq 0 then
            print "Processed",count,"of",#G;
        end if;
    end for;
    assert count eq #G;
    meanchi := (Q!sumchi)/(Q!#G);
    inner := (Q!sumchi2)/(Q!#G);
    print "Character computation time:",Cputime(start);
    print "Character distribution:";
    for k in [-6..6] do
        if hist[k] ne 0 then
            print "Trace =",k,"Multiplicity =",hist[k];
        end if;
    end for;
    print "EXACT RESULTS";
    print "Group order =",#G;
    print "Representation dimension = 6";
    print "Sum of characters =",sumchi;
    print "Sum of squared characters =",sumchi2;
    print "<chi,1> =",meanchi;
    print "<chi,chi> =",inner;
    print "No trivial constituent =",meanchi eq 0;
    print "Absolutely irreducible =",inner eq 1;
    if meanchi eq 0 and inner eq 1 then
        print "SIGNED REPRESENTATION: PASS";
        print "V_D is absolutely irreducible.";
        print "V_D has no trivial constituent.";
        print "Using the established non-torsion results:";
        print "P,U_1,...,U_6 are independent modulo torsion.";
        print "Rank J(K) >= 7.";
        print "MORDELL-WEIL INDEPENDENCE: PASS";
        print "Subject to the non-torsion proof.";
    else
        print "Irreducibility criterion not satisfied.";
    end if;
    print "This does not establish C = 1.";
    print "Problem H remains open.";
end if;
print "COMPUTATION FINISHED";
