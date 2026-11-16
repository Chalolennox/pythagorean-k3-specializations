<!-- Provenance: independent review of NOTE_coprimality_direct_proof.md, received 16 November 2026 17:06 (Europe/Berlin) as a text attachment; reviewer not named. Verbatim. It audits section (a) of F.55 only; the lattice recurrence (d) and the reduction (e) were not part of that review. -->

My conclusion: the direct proof of H1 is mathematically sound. I found no logical gap in the argument as written, assuming the standard division-polynomial identities (F1)–(F3) and the chord formula (F4).

This is a significant improvement: the coprimality theorem no longer needs to be imported from the literature.
1. Audit of the proof
Section	Assessment	Reason
§1: Duplication	Valid	Follows exactly from the curve equation and \(W_{2n}=2y_nW_n^4\)
§2: Parity induction	Valid	Both odd and even cases use strictly smaller indices
§3: Valuation	Valid	The two auxiliary factors in the duplication identity are odd
§4.1: Choice of \(m\)	Valid	The selected indices are correct for both parities of \(N\)
§4.2: Unit denominators	Valid	Minimality excludes all possible factors in the odd EDS recurrence
§4.3: Ward congruence	Valid	Both denominators are invertible modulo \(p\)
§4.4: Vanishing of \(y_m\)	Valid	Uses the common residue of \(t_m,t_{m+1}\) correctly
§4.5: Chord formula	Valid	\(s\ne0\) justifies division modulo \(p\)
§4.6: Resultant	Valid	Independently checked: \(\operatorname{Res}(f,g)=-16\)
§5: Coprimality consequence	Valid	Consecutive coprimality implies \(\gcd(A_n,B_n)=1\)

The critical minimal-counterexample argument
The most delicate step was §4.2, and it works.

Suppose \(p\mid W_N,W_{N+1}\), with \(N\) minimal. Set \(m=\lfloor N/2\rfloor\).

Since \(p\mid W_{2m+1}\), the odd-index recurrence gives
\[
W_{m+2}W_m^3
\equiv W_{m-1}W_{m+1}^3\pmod p.
\]

If \(p\mid W_m\), the right side vanishes, forcing \(p\mid W_{m-1}\) or \(p\mid W_{m+1}\). Both contradict minimality.

Likewise, if \(p\mid W_{m+1}\), the left side vanishes, forcing \(p\mid W_m\) or \(p\mid W_{m+2}\), again contradicting minimality.

Therefore
\[
\boxed{p\nmid W_mW_{m+1}.}
\]

This establishes precisely the denominator invertibility that was missing from the earlier sketch.

The subsequent Ward and chord arguments then force
\[
(1-s)(1+s^2)=0,\qquad 2s^3-s^2+1=0
\]

over \(\mathbb F_p\). Their resultant is \(-16\), excluding every odd prime.

No circular use of coprimality is apparent.
2. H1 can now be stated as a proved proposition
Proposition. Let
\[
C:y^2=x^3-2x^2+2x,\qquad P=(1,1),
\]

and \(W_n=\psi_n(P)\). Then, for every positive integer \(n\),
\[
\boxed{
W_n\equiv n\pmod2,\qquad
v_2(W_n)=v_2(n),\qquad
\gcd(W_n,W_{n+1})=1.
}
\]

Consequently,
\[
\boxed{\gcd(A_n,B_n)=1.}
\]

The proof is elementary once the classical division-polynomial identities are admitted.

One small editorial improvement: explicitly establish that \(P\) has infinite order, or cite a standard criterion and verify it for this curve. The supplied proof assumes this fact rather than proving it.
3. Does this make the original conjecture unconditional?
Potentially, yes.

The dependency structure is now:
H1: EDS valuation and coprimality
Proof audited

H2: Ward-derived isometry

 Follows from H1

H3: Odd-index base estimates

Reviewer reports proof

Even-index duplication induction

Conditional argument supplied

Full conjecture (C)

Final proof audit outstanding


The remaining issue is not coprimality. It is ensuring that the reviewer's full summation proof of H3 and the duplication induction are correct as written, rather than relying on their reported conclusions.

In particular, the even-index argument requires the uniform estimate
\[
v_2(R_k-R_\ell)\ge4+v_2(k^2-\ell^2).
\]

The supplied duplication proof establishes its propagation under doubling. The base cases are furnished by H3.
4. One remaining mathematical detail
The parity induction uses the assertion that \(W_n\ne0\) for nonzero \(n\), which follows from \(P\) having infinite order.

This can be verified independently using the Lutz–Nagell theorem. The model has integral coefficients and discriminant \(-256\). If \(P\) were torsion, the same theorem would apply to its multiples, but
\[
2P=\left(\frac14,-\frac58\right)
\]

has nonintegral coordinates. Hence \(P\) cannot be torsion.

That supplies the required infinite-order justification.

My assessment
The direct H1 proof is ready to incorporate into a formal manuscript. It is short, self-contained relative to standard division-polynomial identities, and handles the bad prime \(2\) without invoking a general coprimality theorem.

I would now consolidate the research into one complete proof document containing:
1. The direct H1 proof supplied here.
2. The complete odd-index summation argument establishing (O2) and H3.
3. The duplication induction establishing (E2).
4. The final passage from (O2), (E2), and mixed parity to the original valuation identity.
The crucial next task is a single continuous proof audit of those four pieces, checking every valuation and normalization at their interfaces.

If that succeeds, we can state the unconditional theorem
\[
\boxed{
v_2(N_n-N_m)=1+v_2(n^2-m^2)
\qquad(n\ne m,\ n,m\ge1).
}
\]

That would establish injectivity of the integer sequence \(N_n\), not merely provide numerical evidence for it.