# Odd saturation through 10,000 (2026-11-27)

Owner-executed Magma V2.30-1 results; AI-authored record, independent human review pending. Extends KUMMER_ODD_SATURATION.md. No global saturation or Problem H claim.

Let J: y²=x³−2x²+2x, P=(1,1), and U=(x,z), where x is a root of h=X^6−6X^5−15X^4+100X^3−189X²+162X−54. The degree-12 point field F=Q(z) is defined by f=X^12−66X^10−29922X^8+73214X^6−62559X^4+22032X²−3456. Recover x by the linear gcd of h and X³−2X²+2X−z² over F. Owner reports torsion order 2 and height 0.744894832461137944106490376.

For odd l, divisibility modulo torsion descends from K to F by trace and Bezout since [K:F]=128. Independent sign flips isolate each U coordinate in the saturation kernel; transitivity reduces to U. For P, trace to Q excludes l>=5 provided P is primitive in J(Q)/torsion (as in the preceding work); l=3 was previously certified.

At a prime p>3 not dividing disc(f), a simple root z mod p gives a degree-one place. A linear gcd as above recovers the reduction U. If l divides N=#J(F_p) and [N/l]U is nonzero, U cannot be l-divisible modulo torsion over F, since its torsion has order 2.

## Owner execution

Initial known primes: 3,5,7,11,13,23 (3,23 from earlier certificates; 5,7,11,13 from reported direct division tests). Compact scan through p=2,000,000 produced 1,218 new certificates, all replayed successfully, leaving four primes. Targeted scan produced these final integer certificates in format [l,p,N,xU,yU,xV,yV], V=[N/l]U:

    [8431,2123831,2124612,1566839,703827,1895189,199072]
    [6841,2136527,2134392,1706561,635147,1458897,1616987]
    [5167,2302987,2304482,1823048,98124,2285848,162389]
    [8627,2487581,2484576,2113923,169161,672642,955731]

Targeted scan: 33299 reduction primes, 10685 with degree-one roots, replay PASS, remaining [], CPU 3.070s, seed 2499199044. Combined coverage: 1228/1228 odd primes <=10000. Compact scan did not export the full witness table; rerun to regenerate it. See companion replay script for final four.

## Height route (not completed)

Sage reports degree 12, signature (2,5), discriminant −256, numerical height 0.744894832461138. Two bad places above 2 have Kodaira types I7* and I4*, minimal discriminant valuations 20 each, conductor exponents 9 and 12, Tamagawa numbers 2 and 4, component exponents both 2. The finite component multiplier is 2. Sage test_mu run stopped in the supplied output at N=2, with target 1/250000; no lower-bound certificate obtained. Verify all hypotheses including archimedean conditions before using this method.

The next possible prime is 10007. A rigorous positive lower height bound c and certified upper bound H for U with H < 10007² c would exclude all remaining primes. Numerical threshold is approximately 7.43853e-9; this is not itself a certified bound. Global odd saturation remains open.
