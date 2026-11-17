<!-- Provenance: sent to the chat by the repository owner on 17 November 2026 ("this for today"). The text below the line is unmodified; its numerical claims were checked in code/verify_gap_k.py, check 8, and the identity is the one already stated in F.57 (e) (N_k = D_k O_k^2). -->
---
Factorization of the Gap Resultant — Problem H
Let
[
C:y^2=x^3-2x^2+2x,\qquad P=(1,1),
]
and define
[
H(t)=t^6-30t^4-24t^2-1,\qquad h(X)=H(1-X).
]
For a gap (k\geq1), put (a=x(kP)) and define the symmetric polynomial
[
\begin{aligned}
G_a(X,W)={}&(X-a)^2W^2\
&+(-2aX^2-2a^2X+8aX-4X-4a)W\
&+a^2X^2-4aX+4.
\end{aligned}
]
It describes the relation between the (x)-coordinates of points differing by (kP).
Factorization theorem
Define
[
D_k=\operatorname{Res}_X\left(
h(X),\operatorname{Res}_W(h(W),G_a(X,W))
\right)
]
and
[
\Delta_k=\operatorname{Res}_X(h(X),G_a(X,X)).
]
Proposition. For every gap (k\geq1),
[
\boxed{D_k=\Delta_k S_k^2}
]
for some (S_k\in\mathbb Q).
Proof. Let (\alpha_1,\ldots,\alpha_6) be the roots of the monic polynomial (h). Then
[
D_k=\prod_{i,j=1}^{6}G_a(\alpha_i,\alpha_j).
]
Since (G_a(X,W)=G_a(W,X)), the off-diagonal factors occur in equal pairs. Therefore,
[
D_k=
\underbrace{\prod_{i=1}^{6}G_a(\alpha_i,\alpha_i)}{\Delta_k}
\left(
\underbrace{\prod{i<j}G_a(\alpha_i,\alpha_j)}_{S_k}
\right)^2.
]
The product defining (S_k) is symmetric in the roots and hence rational. (\square)
Computational verification
Exact Magma calculations verified the identity for gaps (k=1,\ldots,6).
The off-diagonal factors exhibit repeated prime divisors:
[
\begin{aligned}
47&\mid S_2,\ S_5,\
83&\mid S_4,\ S_6,\
113&\mid S_1,\ S_6.
\end{aligned}
]
Finite-field calculations explain these overlaps:

* (p=47): The same root pair occurs at gaps (2) and (5), with (5\equiv-2\pmod7).
* (p=83): Different root pairs produce coincidences at gaps (4) and (6).
* (p=113): The relevant root pairs exist over (\mathbb F_{113^2}), with Frobenius exchanging their coordinates.

Consequence for Problem H
The factorization separates diagonal and off-diagonal coincidences exactly. However, (S_k) also detects intersections over extension fields, so
[
p\mid S_k
]
does not necessarily imply a qualifying-prime coincidence over (\mathbb F_p).
Conclusion. The factorization is an exact algebraic identity, and the finite-field experiments explain several repeated prime factors. It does not, by itself, establish correlations or sign-distribution bounds for Problem H.
