<!-- Provenance: text supplied by the repository owner on 16 November 2026 as an independent review of the sketch "the values F(t_n) should be pairwise distinct" (the height argument), reproduced word for word below this line. -->

The idea is worth examining, but the proposed height argument does not prove that the values \(F(t_n)\) are eventually pairwise distinct. There are two separate problems.
1. The degree-six height formula is incorrect here
Recall
\[ F(t)=-4\frac{t^6-30t^4-24t^2-1}{(1+t^2)^3}. \]
As a rational map \(\mathbb P^1\to\mathbb P^1\), it has degree 6. Therefore,
\[ \boxed{h(F(t))=6h(t)+O(1)} \]
is correct, with an error bounded independently of \(t\).
For our sequence, however, we have
\[ t_n=1-x(nP), \]
where
\[ P=(1,1)\in E_0(\mathbb Q),\qquad E_0:y^2=x^3-2x^2+2x. \]
The canonical-height relation gives
\[ h(t_n)=2\widehat h(P)n^2+O(1) \]
up to the usual bounded difference between the logarithmic \(x\)-height and twice the canonical height.
Consequently,
\[ \boxed{ h(F(t_n))=12\widehat h(P)n^2+O(1). } \]
Thus the heights grow quadratically.
2. Quadratic growth does not imply injectivity
Suppose
\[ F(t_n)=F(t_m). \]
Then their heights are equal, so
\[ 12\widehat h(P)n^2+O(1) = 12\widehat h(P)m^2+O(1). \]
This yields
\[ \boxed{|n^2-m^2|\le C} \]
for some constant \(C\) independent of \(n,m\).
For positive integers \(n\ne m\),
\[ |n^2-m^2|\ge 2\min(n,m)+1. \]
Therefore, once \(n,m\) are sufficiently large, equality becomes impossible.
So the proposed argument actually works for positive indices, provided the height error is genuinely bounded uniformly in \(n\).
This is stronger than it first appears: it reduces possible collisions to a finite computation.
There is, however, an important symmetry.
3. The sequence must be indexed carefully
Because
\[ x(-nP)=x(nP), \]
we have
\[ t_{-n}=t_n \]
and hence
\[ F(t_{-n})=F(t_n). \]
Thus pairwise distinctness cannot hold over all integer indices.
It may hold for \(n\ge0\), after handling the point at infinity and any undefined parameter.
For \(n,m\ge0\), the quadratic height argument gives eventual injectivity.
4. What remains to make this rigorous?
We need an explicit constant \(C_0\) satisfying
\[ \left|h(x(Q))-2\widehat h(Q)\right|\le C_0 \]
for every relevant rational point \(Q\in E_0(\mathbb Q)\), together with a constant \(C_1\) satisfying
\[ |h(F(t))-6h(t)|\le C_1. \]
Then
\[ \left|h(F(t_n))-12n^2\widehat h(P)\right| \le 6C_0+C_1. \]
For any collision with \(n>m\ge0\),
\[ 12\widehat h(P)(n^2-m^2) \le 2(6C_0+C_1). \]
Hence
\[ n^2-m^2\le \frac{6C_0+C_1}{6\widehat h(P)}. \]
This gives an explicit finite bound for all possible collisions.
An important distinction
This argument proves eventual injectivity along the orbit \(t_n=1-x(nP)\). It does not prove the stronger global conjecture
\[ F(t)=F(u)\Longrightarrow t=\pm u \]
for arbitrary rational parameters.
But it would give an unconditional theorem about the sequence relevant to Problem H.
