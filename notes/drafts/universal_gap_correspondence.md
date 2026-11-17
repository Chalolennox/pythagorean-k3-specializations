<!-- Provenance: pasted into the chat by the repository owner on 17 November 2026 (message "add this"), origin not stated. Reviewed in notes/REVIEW_2026-11-17_gap_three_dossier.md, section 5; checked in code/verify_gap_three.py (check 11).
     The text below the line is unmodified. -->

---

I found a useful simplification: all the gap correspondences \(G_k(t,w)=0\) come from one universal symmetric biquadratic polynomial. We do not need to derive a new equation for each \(k\).
Let
\[ C:y^2=x^3-2x^2+2x,\qquad P=(1,1), \]
and write
\[ kP=(u_k,v_k). \]
For \(k\ne0\), define
\[ \begin{aligned} \Phi_u(X,Z)={}&(X-u)^2Z^2\\ &+(-2u^2X-2uX^2+8uX-4u-4X)Z\\ &+u^2X^2-4uX+4. \end{aligned} \]
Then the gap-\(k\) correspondence is simply
\[ \boxed{G_k(t,w)=\Phi_{u_k}(1-t,1-w).} \]
This has three important properties:

* It is symmetric in \(t,w\).
* It has bidegree \((2,2)\), regardless of \(k\).
* It depends only on \(u_k=x(kP)\), not on \(v_k\).

The third property is particularly useful: the correspondences for \(kP\) and \(-kP\) are identical.
Exact verification at gap three
For \(3P=(49/9,-287/27)\), substitution gives
\[ \begin{aligned} 81G_3(t,w)={}&81t^2w^2+720(t^2w+tw^2)\\ &+1600(t^2+w^2)-4802tw\\ &+1044(t+w)-1683, \end{aligned} \]
where \(G_3\) on the left denotes the universal rational-coefficient expression.
Thus, after multiplying by 81, we recover exactly the independent reviewer's nine-term polynomial.
This is a symbolic identity, not a numerical fit.
Why the universal formula works
Write \(Q=(X,Y)\), \(R=(u,v)\), and \(Q+R=(Z,W)\). The elliptic-curve addition law gives
\[ Z=\left(\frac{Y-v}{X-u}\right)^2+2-X-u. \]
Rearranging and using \(Y^2=f(X)\), \(v^2=f(u)\), where \(f(X)=X^3-2X^2+2X\), gives
\[ \bigl((X-u)^2(Z+X+u-2)-f(X)-f(u)\bigr)^2 =4f(X)f(u). \]
The difference between the two sides factors exactly as
\[ (X-u)^2\Phi_u(X,Z). \]
This proves the universal correspondence away from the removable factor \(X=u\), and the polynomial identity extends to all points by closure.
