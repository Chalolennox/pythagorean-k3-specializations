# Active-period transpose obstruction

Fix the sixteen owner Magma residue rows in code/verify/pr92_transpose_obstruction.py. For n=72k define e_p=d_p/gcd(d_p,n), and the active period lattice as the intersection of kernels of (i,j) -> 2^i 3^j mod e_p over primes with nonempty qualifying support.

Theorem (relative to the input residue data): no two nontrivial active period lattices for seeds divisible by 72 are coordinate transposes of each other.

Proof certificate. Every e_p divides d_p/gcd(d_p,72). If a qualifying residue v is accessible, g=d_p/e_p divides v and gcd(v/g,e_p)=1, since orbit elements divided by g are units. Enumerate all divisors satisfying this necessary condition, allowing inactive primes and ignoring cross-prime compatibility. The e=1 lattice is Z^2 and may be omitted. Thus every actual active lattice belongs to the enumerated superset.

Represent a lattice by (r,a,b), basis (r,0),(-a,b), 0<=a<r. Here r=ord_e(2), b is the least positive integer with 3^b in <2>, and 3^b=2^a. For two lattices (r,a,b),(s,c,d), set g=gcd(r,s), l=lcm(b,d), h=a*l/b-c*l/d. Their intersection has vertical period t=l*g/gcd(h,g), horizontal period R=lcm(r,s), and shear given by CRT of a*t/b mod r and c*t/d mod s. For the transpose, set q=gcd(r,a). Its horizontal period is br/q, vertical period q, and shear b times an inverse of a/q modulo r/q, reduced modulo br/q. This follows by solving r*k-a*j=q and exchanging coordinates. Modulus one is allowed.

Starting from Z^2, take intersections with each prime's candidate lattices or omit that prime. The executed exact JavaScript enumeration produced 98304 distinct canonical lattices, verified transpose involution for every entry, and found no nontrivial transposed pair. The standalone Python certificate implements the same finite enumeration and asserts the counts and unique trivial match; Python version not yet executed in this turn.

Scope: this excludes coordinate-swap isomorphisms between the specified active period quotients, not arbitrary isomorphisms, XOR stabilizer quotients, enlarged symmetric covers, other prime sets, or all rational arithmetic labels. The reference de Bruijn group still acts combinatorially. The result is a negative certificate for a specific arithmetic lifting mechanism, not an impossibility theorem for every arithmetic realization of the order-32 group. Input residue data are not independently recertified here. Human review pending.
