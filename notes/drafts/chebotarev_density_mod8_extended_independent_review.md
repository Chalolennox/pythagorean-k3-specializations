# A Chebotarev density calculation for the curve \(y^2=x^3-2x^2+2x\)

**Extended independent-review draft — 11 November 2026**

**Status key:** The mod-8 density and the four-divisibility equivalence below are deductions from explicitly reported exact Magma group computations. The level-16 equivalence is disproved by an exact counterexample. Higher-level geometric density laws remain conjectural.


## Statement

Let
\[
C/\mathbb Q:\quad y^2=x^3-2x^2+2x,
\]
and let \(\pi(X)\) denote the number of primes \(p\leq X\). The proposed theorem is
\[
\boxed{\lim_{X\to\infty}\frac{\#\{p\le X:p\equiv7\pmod8,\ 8\mid\#C(\mathbb F_p)\}}{\pi(X)}=\frac18.}
\]
Equivalently, the conditional density within the primes \(p\equiv7\pmod8\) is \(1/2\).

The proof uses an **exact Magma group calculation** as a finite computational lemma. The mathematical argument below specifies what the computation must certify. The Magma outputs were supplied by the investigator; an independent reviewer should rerun the calculations, particularly the identification of the cyclotomic coset and the root-to-torsion implication.

## 1. The halving polynomial

Write \(T=(0,0)\in C(\mathbb Q)[2]\). The duplication formula is
\[
x(2R)=\frac{(x(R)^2-2)^2}{4x(R)(x(R)^2-2x(R)+2)}.
\]
Hence, for \(s^2=2\), the polynomial governing the \(x\)-coordinates of points \(R\) with \(x(2R)=s\) is
\[
H_s(X)=(X^2-2)^2-4sX(X^2-2X+2)
=X^4-4sX^3+(8s-4)X^2-8sX+4.
\]
The product of the two conjugate quartics is
\[
\begin{aligned}
f(X)&=H_{\sqrt2}(X)H_{-\sqrt2}(X)\\
&=X^8-40X^6+128X^5-232X^4+256X^3-160X^2+16.
\end{aligned}
\]
It is the unique irreducible degree-eight factor of the eighth division polynomial in the Magma computation.

For any odd prime \(p\equiv7\pmod8\), both \(2\) and \(-2\) are squares modulo \(p\), while \(-1\) is not. The nonzero rational 2-torsion points satisfy \(x^2-2x+2=0\), whose discriminant is \(-4\). Thus \(T\) is the **unique** nonidentity rational 2-torsion point, and the 2-Sylow subgroup of \(C(\mathbb F_p)\) is cyclic.

The halves of \(T\) have \(x=\pm s\), where \(s^2=2\). Their \(y\)-coordinate squares are
\[
F(s)=s^3-2s^2+2s=4(s-1),\qquad
F(-s)=-4(s+1).
\]
Their product is \(-16\). Since \(-1\) is nonsquare, **exactly one** of these values is a square in \(\mathbb F_p\). Hence one of the two points \(Q\) of order four, with \(2Q=T\), is rational (and so is \(-Q\)). In particular, \(4\mid\#C(\mathbb F_p)\).

## 2. Exact splitting-field data

Let \(L\) be the splitting field of \(f\) over \(\mathbb Q\), and let \(G=\operatorname{Gal}(L/\mathbb Q)\), acting on its eight roots.

The reported exact Magma computations give:

1. \(f\) is irreducible over \(\mathbb Q\), and \(|G|=32\).
2. Over \(K=\mathbb Q(\zeta_8)=\mathbb Q(i,\sqrt2)\), \(f\) splits into two irreducible quartics and its splitting-field Galois group over \(K\) has order eight. Consequently \([L\cap K:\mathbb Q]=32/8=4\), so \(K\subseteq L\).
3. Among the normal order-16 subgroups of \(G\), exactly one, denoted \(H_2\), has orbit sizes \([4,4]\). Since \(f\) factors over \(\mathbb Q(\sqrt2)\) into two irreducible quartics, \(H_2=\operatorname{Gal}(L/\mathbb Q(\sqrt2))\).

The last identification is exact: the subgroup fixing \(\sqrt2\) is normal of order 16 and its orbits are precisely the irreducible factor root sets. The uniqueness in item 3 identifies it.

## 3. Exact identification of the \(i\)-character

For \(s^2=2\), direct calculation gives
\[
\operatorname{disc}(H_s)=2^{20}(2s-3)=-\bigl(2^{10}(s-1)\bigr)^2.
\]
In particular, the discriminant square root of either quartic generates \(i\) over \(\mathbb Q(\sqrt2)\). Indeed, the square root of a separable polynomial's discriminant transforms under root permutations by their sign. Thus, for \(g\in H_2\),
\[
\operatorname{sgn}(g\text{ on the roots of }H_s)=\frac{g(i)}{i}.
\]
This is a genuine Galois character, not an inference from observed primes.

For an unramified prime \(p\equiv7\pmod8\), the Frobenius fixes \(\sqrt2\) and sends \(i\mapsto-i\). Its conjugacy class therefore lies in the explicitly defined subset
\[
\mathcal C_7=\{g\in H_2:\operatorname{sgn}(g\text{ on a quartic orbit})=-1\}.
\]
This subset is the inverse image of the element \(7\in(\mathbb Z/8\mathbb Z)^\times\) under restriction \(G\to\operatorname{Gal}(K/\mathbb Q)\). It has exactly eight elements.

## 4. Finite Galois-group enumeration

The reported Magma enumeration of all elements of \(\mathcal C_7\) gives:

| Cycle type on the eight roots of \(f\) | Number of elements |
|:--|--:|
| \(1^4 2^2\) | 4 |
| \(4^2\) | 4 |
| Other | 0 |

These are **exact integer counts** in a group of order 32, not estimates from prime samples.

An element of type \(1^4 2^2\) fixes four roots of \(f\); an element of type \(4^2\) fixes none. Thus exactly four of the eight elements of \(\mathcal C_7\) have a fixed root.

## 5. Why a fixed root is equivalent to rational 8-torsion in this residue class

We need to justify the passage from the polynomial \(f\), which records **\(x\)-coordinates**, to rational points. This cannot be assumed for arbitrary primes.

Fix \(p\equiv7\pmod8\), and let \(s\in\mathbb F_p\) be a square root of 2. As shown in Section 1, exactly one of the two points with \(x=\pm s\) is rational. Call that rational point \(Q\), of order four. Its \(x\)-coordinate is either \(s\) or \(-s\).

The Frobenius action on each four-element root set of \(H_s\) is an **odd** permutation, by the discriminant computation and the fact that \(p\equiv3\pmod4\). Since the full eight-root cycle types in \(\mathcal C_7\) are only \(1^4 2^2\) and \(4^2\), in the first case each quartic must have exactly two fixed roots: an odd permutation on four letters can have two fixed points (a transposition) or no fixed points (a four-cycle), and four fixed roots in total force the former in both quartics.

Therefore, if \(f\) has a root over \(\mathbb F_p\), the **particular quartic associated with the rational point \(Q\)** has a root \(x_0\in\mathbb F_p\). Choose a geometric point \(R\) above \(x_0\) with \(2R=Q\). Such a point exists by the duplication formula and the group law over an algebraic closure. Frobenius fixes \(x(R)\), hence sends \(R\) to \(R\) or \(-R\). But it fixes \(Q=2R\), whereas \(2(-R)=-Q\ne Q\), since \(Q\) has order four. Thus Frobenius fixes \(R\), and \(R\in C(\mathbb F_p)\) has order eight.

Conversely, if \(8\mid\#C(\mathbb F_p)\), Cauchy's theorem gives a rational point \(R\) of order eight; then \(2R\) has order four and \(x(2R)^2=2\), so \(x(R)\) is a root of \(f\) modulo \(p\).

We have proved, for all primes \(p\equiv7\pmod8\) of good reduction,
\[
\boxed{f\text{ has a root in }\mathbb F_p\quad\Longleftrightarrow\quad8\mid\#C(\mathbb F_p).}
\]

## 6. Chebotarev

The subset \(\mathcal C_7\subseteq G\) is stable under conjugation, because it is defined by the cyclotomic restriction. The property of having a fixed root is also conjugacy invariant.

By the Chebotarev density theorem, the set of unramified primes whose Frobenius belongs to the four fixed-root elements of \(\mathcal C_7\) has natural density
\[
\frac{4}{|G|}=\frac4{32}=\boxed{\frac18}.
\]
By Section 5 this is precisely the set of primes \(p\equiv7\pmod8\) for which \(8\mid\#C(\mathbb F_p)\), apart from finitely many ramified primes, which do not affect density. This proves the stated theorem, **conditional only on the reproducibility and correctness of the finite exact Magma computations in Sections 2 and 4**.

Since the primes \(p\equiv7\pmod8\) have density \(1/4\), the conditional density is \((1/8)/(1/4)=1/2\).

## 7. Independent-review checklist

The reviewer should independently check:

1. The duplication formula, the factorization \(f=H_sH_{-s}\), and the quartic discriminant identity.
2. Irreducibility of \(f\), the exact Galois group order 32, and the cyclotomic base-change group order 8.
3. Uniqueness of the normal order-16 subgroup with two four-element orbits, and its identification with the \(\sqrt2\)-kernel.
4. The identification of the sign character with the action on \(i\), not merely a numerical correlation.
5. The exact coset enumeration \((4,4,0)\).
6. The fixed-root-to-rational-point argument in Section 5, including the role of the *rational* order-four point.

**Scope:** This establishes one finite-level density. It does not establish the conjectured density \(1/6\) of primes \(p\equiv7\pmod8\) for which the reduction of \(P=(1,1)\) has odd order, nor the original rank-specialization question.


---

# Addendum A. A rational half of the distinguished point

Let \(P=(1,1)\in C(\mathbb Q)\), let \(K_0=\mathbb Q(s)\) with \(s^2=2\), and define
\[
Q=(2+s,2+2s)\in C(K_0).
\]
Substitution into the equation of \(C\) and the group law verify **exactly** that \(2Q=P\). The polynomial for the \(x\)-coordinates of halves of \(P\) is
\[
F_P(X)=(X^2-2)^2-4X(X^2-2X+2)
=(X^2-4X+2)(X^2+2).
\]
The reported Magma computation gives \(\operatorname{Gal}(F_P/\mathbb Q)\cong C_2\times C_2\) (order four). For each odd prime \(p\equiv7\pmod8\), \(s\in\mathbb F_p\), so the displayed point \(Q\) reduces to an \(\mathbb F_p\)-rational half of \(P\). Therefore
\[
\boxed{P\in2C(\mathbb F_p)\quad\text{for every prime }p\equiv7\pmod8.}
\]
This statement is unconditional and does not require Chebotarev.

# Addendum B. Exact equivalence between eight-torsion and four-divisibility of \(P\)

## B.1 The second quartic

With \(Q\) as above, define
\[
F_s(X)=(X^2-2)^2-4(2+s)X(X^2-2X+2)
=X^4-(8+4s)X^3+(12+8s)X^2-(16+8s)X+4.
\]
This quartic governs the \(x\)-coordinates of geometric points \(R\) satisfying \(x(2R)=x(Q)\). The two points with that doubled \(x\)-coordinate are \(Q\) and \(-Q\); choosing the sign of \(R\) gives \(2R=Q\).

**Rationality lemma.** Let \(k\) be a finite field of odd characteristic, \(Q\in C(k)\) a point of order not dividing two, and let \(x_0\in k\) be the \(x\)-coordinate of a geometric point \(R\) with \(2R=Q\). Frobenius fixes \(x_0\), so it sends \(R\) to \(\pm R\). Since it fixes \(Q\ne-Q\), it cannot send \(R\) to \(-R\). Hence \(R\in C(k)\). Thus a root of \(F_s\) over \(k\) is equivalent to \(Q\in2C(k)\), provided \(Q\ne -Q\).

For \(p\equiv7\pmod8\), the 2-Sylow subgroup of \(C(\mathbb F_p)\) is cyclic of order at least four. Its unique nonzero 2-torsion point \(T\) is itself twice a rational point. The two rational halves of \(P\) are \(Q\) and \(Q+T\), and they are simultaneously divisible by two. Consequently
\[
\boxed{F_s\text{ has a root modulo }p\iff P\in4C(\mathbb F_p).}
\]
Either embedding \(s\mapsto\pm\sqrt2\) may be used; the equivalence is independent of that choice.

## B.2 The two quartics share their splitting field

Recall the 8-torsion quartic
\[
H_s(X)=X^4-4sX^3+(8s-4)X^2-8sX+4.
\]
The investigator's **exact Magma output** over \(K_0=\mathbb Q(\sqrt2)\) reports
\[
|\operatorname{Gal}(H_s/K_0)|=8,\qquad
|\operatorname{Gal}(F_s/K_0)|=8,
\]
with both groups isomorphic to the dihedral group \(D_4\). It further reports
\[
|\operatorname{Gal}(H_sF_s/K_0)|=8.
\]
Because the splitting fields are Galois extensions of degree eight and their compositum has degree eight, **their splitting fields coincide**.

The discriminants are
\[
\begin{aligned}
\operatorname{disc}(H_s)&=2^{20}(2s-3)=-2^{20}(s-1)^2,\\
\operatorname{disc}(F_s)&=-2^{20}(17+12s)=-2^{20}(3+2s)^2.
\end{aligned}
\]
Both discriminants have square class \(-1\) in \(K_0\). This is consistent with, but by itself does not imply, equality of the splitting fields.

## B.3 The crucial joint permutation calculation

The Galois group of the product \(H_sF_s\) acts on eight roots in two invariant blocks of four. The exact Magma enumeration supplied by the investigator gives:

| Fixed-root behavior of a group element | Number of elements |
|:--|--:|
| Has a fixed root in **both** quartics | 3 |
| Has a fixed root in **neither** quartic | 5 |
| Fixed root only in \(H_s\) | 0 |
| Fixed root only in \(F_s\) | 0 |

The element-by-element output also confirms that the three elements fixing roots do so in both blocks (one identity and two reflections), while the other five elements fix none. **This is a finite exact Galois-group certificate, not a statistical claim.**

Therefore, at every prime ideal of \(K_0\) unramified in the common splitting field,
\[
H_s\text{ has a residue-field root}\iff F_s\text{ has a residue-field root}.
\]
For rational primes \(p\equiv7\pmod8\), the Frobenius action on the two conjugate quartics \(H_s,H_{-s}\) is synchronized: by the exact coset calculation in Sections 3–5, either both have roots or neither does. Combining this with the rationality lemmas gives the following result.

**Theorem B (computationally certified).** For every rational prime \(p\equiv7\pmod8\) unramified in the relevant splitting fields,
\[
\boxed{8\mid\#C(\mathbb F_p)\quad\Longleftrightarrow\quad P\in4C(\mathbb F_p).}
\]
In particular, if \(r=v_2(\#C(\mathbb F_p))\) and \(e=v_2(\operatorname{ord}(P\bmod p))\), then
\[
r\ge3\quad\Longrightarrow\quad e\le r-2.
\]
The last implication uses the cyclicity of the 2-Sylow subgroup. The reverse implication between these numerical conditions also holds when \(r\ge3\). The theorem is independent of the prime-count experiment; its computational dependencies are the exact group calculations stated above.

**Density corollary.** By the original Chebotarev calculation,
\[
\operatorname{dens}\{p\equiv7\pmod8:P\in4C(\mathbb F_p)\}=\boxed{\tfrac18},
\]
so the conditional density inside \(p\equiv7\pmod8\) is \(1/2\).

# Addendum C. The level-16 analogue is false

Consider \(p=31\equiv7\pmod8\). Exact Magma computations give
\[
\#C(\mathbb F_{31})=32,\quad
2P=(8,11),\quad4P=T=(0,0),\quad8P=\mathcal O.
\]
Hence \(P\) has order eight. Since \(C(\mathbb F_{31})\) has order 32 and only one nonzero rational 2-torsion point, it is cyclic of order 32. Its subgroup of eighth multiples has order four and cannot contain an element of order eight. Thus
\[
\boxed{16\mid\#C(\mathbb F_{31})\quad\text{but}\quad P\notin8C(\mathbb F_{31}).}
\]
This is an **exact counterexample** to the proposed implication at level 16; the analogous equivalence is false.

The investigator's finite-field census for the 2,399 primes \(p\le100000\) with \(p\equiv7\pmod8\) gives:

| | \(P\in8C(\mathbb F_p)\) | \(P\notin8C(\mathbb F_p)\) |
|:--|--:|--:|
| \(16\mid\#C(\mathbb F_p)\) | 301 | 294 |
| \(16\nmid\#C(\mathbb F_p)\) | 307 | 1497 |

The conditional sample frequency of eight-divisibility of \(P\) given \(16\mid\#C\) is \(301/595\approx0.50588\). The total sample frequency of \(P\in8C\) within \(p\equiv7\pmod8\) is \(608/2399\approx0.25344\). **Neither frequency is a proven density.**

# Addendum D. Higher-level distribution: conjectures, not theorems

The earlier numerical census reported the following counts of \(r=v_2(\#C(\mathbb F_p))\) and the number for which \(P\) has odd order:

| \(r\) | Number of primes | Number with odd-order \(P\) |
|--:|--:|--:|
| 2 | 1200 | 0 |
| 3 | 604 | 307 |
| 4 | 297 | 82 |
| 5 | 144 | 18 |
| 6 | 82 | 3 |
| 7 | 35 | 1 |
| 8 | 18 | 0 |
| 9 | 7 | 1 |
| 10 | 5 | 0 |
| 11 | 5 | 0 |
| 13 and 14 combined | 2 | 0 |

The total is \(412/2399\approx0.171738\) among the sampled primes \(p\equiv7\pmod8\). This is close to, but does not establish, the conjectured conditional density \(1/6\).

A possible model for the group-order valuation is
\[
\Pr(r=k\mid p\equiv7\pmod8)=2^{-(k-1)}\quad(k\ge2).
\]
The point-order data suggest, for \(k\ge3\), the additional *heuristic* conditional law
\[
\Pr(\operatorname{ord}(P\bmod p)\text{ odd}\mid r=k)=2^{-(k-2)},
\]
with conditional probability zero when \(r=2\). **If both laws held as actual prime densities**, then the conjectured conditional density would be
\[
\sum_{k=3}^{\infty}2^{-(k-1)}2^{-(k-2)}=\frac16.
\]
These hypotheses require a compatible infinite-level 2-adic/arboreal Galois analysis; the exact mod-8 theorem does not prove them.

The data also suggest the **separate conjecture**, for \(j\ge2\),
\[
\Pr(P\in2^jC(\mathbb F_p)\mid p\equiv7\pmod8)=2^{-(j-1)}.
\]
The \(j=2\) case is proved by Theorem B; \(j=3\) is consistent with the census, but unproved. Note that \(P\in2C(\mathbb F_p)\) holds for **all** such primes, not just half.

# Addendum E. Independent-review tasks for the new results

1. Verify the explicit point \(Q\) and the identities \(2Q=P\), \(F_P=(X^2-4X+2)(X^2+2)\).
2. Check the finite-field rationality lemma for the roots of \(F_s\), including the \(\pm R\) argument.
3. Independently reproduce the three exact relative Galois orders \(8,8,8\) for \(H_s\), \(F_s\), and \(H_sF_s\).
4. Reproduce the **joint action** on the two four-root blocks; equality of splitting fields alone is insufficient. The decisive counts are \((3,5,0,0)\).
5. Check the passage from the two conjugate quartics to the degree-eight polynomial in the \(7\bmod8\) cyclotomic coset.
6. Verify the \(p=31\) counterexample by exact group arithmetic.
7. Keep the level-16 frequencies and the proposed \(1/6\) density explicitly labeled **numerical/heuristic**.

**Overall scope:** The new algebraic proof explains the deterministic mod-8 relationship between the group order and the divisibility of \(P\). The level-16 experiment demonstrates that the deterministic equivalence does not extend automatically. Neither result establishes the proposed infinite-level odd-order density, nor the original rank-specialization infinitude problem.
