# Problem H: discussion questions after the support and Kummer investigations

**Status:** discussion only, 22 November 2026. No new theorem, numerical result, or proposed proof of Problem H. Written with an AI assistant; not human reviewed. This note is intended to collect *questions to discuss*, not to reopen settled experiments.

## Baseline and scope

Problem H asks whether the global root number of E_{t_n} is +1 for infinitely many n, with t_n = 1 - x(nP) on C: y^2 = x^3 - 2x^2 + 2x, P=(1,1). The paper reduces the sign to explicit periodic/local terms and a parity bit counting **distinct qualifying prime divisors** of the relevant orbit values; this is not the parity of valuations counted with multiplicity.

Read first:
- paper/paper.md, especially Problem H, Appendix B and F.24/F.40;
- notes/REVIEW_2026-11-19_support_two.md;
- notes/REVIEW_2026-11-22_support_structure_proved.md (PR #81);
- notes/REVIEW_2026-11-22_kummer_compositum.md (PR #82).

The notes establish root counts 0/2/6, even support sizes <=12 (attained on the T branch at p=5251537), the p=5 mod 8 index-parity character, the incompatible pair (149,197), and the field equality F=L* with a new relative degree-eight layer. They **do not** solve orbit accessibility or Problem H. The notes explicitly lack human mathematical review.

## Discussion A: separate root-level Chebotarev from actual orbit membership

**Question.** On p=5 mod 8, what precise conditional distribution of chi_p(a+i) can be proved among degree-one roots a of H satisfying the *root-level* qualification characters? State the distribution with its correct sample space: primes, prime-root pairs, or conjugacy classes. Do not silently replace the event “root-level qualifying” with “accessible in <P mod p>”.

**Potential deliverable:** a finite Galois-class table or a proof that a proposed bias is absent, with denominators and conditioning explicitly stated. The existing 12-row Kummer certificate and PR #82 should be the starting point, not recomputed as a purported discovery.

**Stop condition:** if the distribution is already implied by the old/new square-class independence and has no accessibility consequence, record that and close this question. Independence of characters alone does not produce active primes.

## Discussion B: isolate the genuinely missing accessibility condition

For a root a of H modulo p, let Q be a point of C(F_p) with t(Q)=a, when it exists. Distinguish:
1. H(a)=0;
2. the local square-class conditions on g(a), x(Q), etc.;
3. Q in <P mod p> (or <P mod p>+T for the other branch).

**Question.** Can the failure of (3), even when (1) and (2) hold, be classified by an explicit quotient C(F_p)/<P>? Does any proposed criterion really avoid solving a discrete-log/subgroup-membership problem? The known 2-isogeny/2-descent obstruction is insufficient: PR #82 observes that qualified points can have the same 2-descent class as the orbit without being accessible.

**Potential deliverable:** a precise obstruction statement (or counterexample) on a restricted, clearly specified class of primes. Do not claim a uniform finite-extension Chebotarev characterization without proof.

**Stop condition:** if the proposed invariant reduces to the already studied 2-descent class, or requires uncontrolled division fields, record the limitation rather than repeating the computation.

## Discussion C: from prime support to sign parity

Even infinitely many accessible primes, or infinitely many incompatible prime pairs, would not automatically imply infinitely many n with root number +1.

**Question.** What *additional* statement about the parity of distinct qualifying prime divisors along the integer sequence would be sufficient? Formulate any candidate as a separate, explicitly conditional lemma. Check carefully whether the claim requires a sieve for polynomial values on an elliptic orbit, a parity-breaking input, or a result currently unavailable.

**Potential deliverable:** a dependency diagram separating (i) root-level splitting, (ii) orbit accessibility, (iii) simultaneous divisibility of F_n, and (iv) parity of the global sign. Identify exactly which implication fails in a proposed proof.

**Stop condition:** do not present a heuristic coin-toss model, density estimate, or finite search as a proof of sign changes.

## Discussion D: what the finite support experiments can actually test

PR #81 already reports p=149,197, the sharp bound 12, and sums of |S_{p,j}|/m_p up to 30000. Avoid repeating those experiments.

**Question.** Which *new, falsifiable* assertion about support intersections or parity classes would distinguish two competing mechanisms? Any experiment must state its sampling universe, both branches, cutoff, and expected counterexample. Incompatibility of two periodic supports is a statement about their intersection, not a global obstruction to other primes or to positive root numbers.

**Potential deliverable:** one sharply specified test only if it answers a mathematical question not already settled in the notes.

## Discussion E: formalization and evidence labels

Stage 14 Coq work is a conditional bridge: the local root-number theorem is supplied as a hypothesis, not formalized from local-field theory. Keep separate:
- algebraic statements checked by Coq;
- standard external theorems cited (including Rohrlich);
- exact computational certificates;
- finite observations;
- open conjectures.

A discussion PR should not silently upgrade “proof given, no human review” to “proved” under the repository's claims policy.

## Suggested discussion order

First settle A's exact conditioning and check whether it yields anything not already in PR #82. Then assess B's accessibility gap. Only then consider C's parity gap. D is optional and should not be used to substitute computation for the missing implication. No change to the paper's conclusions is proposed.

**Bottom line:** The recent work describes possible prime support and some incompatibilities; it does not control the full parity of prime divisors of F_n. Problem H remains open.
