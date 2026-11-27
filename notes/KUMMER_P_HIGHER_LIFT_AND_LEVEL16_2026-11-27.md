# P-component: level-16 exclusion and higher lifting
Proof given, human review pending. Owner Magma executions, not independently replayed.

J: y²=x³−2x²+2x, P=(1,1), T1=(0,0). T_m=Q(J[m]). B is the quarter-point field from KUMMER_TWO_ADIC_EIGHTH_INTERSECTION.md.

Owner runs 2026-11-27: M=B(sqrt(x(S))) degree 32, nonnormal, normal closure degree 64, derived length 2, maximal-order discriminant 2^138 (seed 1778952099). Direct root test over T8 returned zero roots (seed 1778952185). Relative tower run (seed 2499171641) verified full torsion bases at levels 2,4,8,16 with degrees 2,8,64,512. Verified 2R=P and 4S=P; IsSquare(x(S)) returned false at T16. Subsequent undefined square-root variable and timeout on d2 do not supply any further results. The negative result applies to the selected quarter point; changing quarter point adds 4-torsion, whose halves are in T8, so the Kummer characters over T16 are unchanged.

## Higher lifting
Let H be the closed P-translation image over T_infty in the Tate module Z2². Quarter divisibility gives H contained in 4Z2². Provided the eighth-division Frobenius exclusion at infinite level is certified (see earlier note and stabilization), H mod 8 is nonzero. If full, Nakayama gives H=4Z2². Otherwise its unique invariant line under the nontrivial mod-2 action is T1. Choose h=4v in H with v mod 2=T1. A half A of T1 has x(A)=±sqrt(2) by duplication. There exists g fixing Q(i) but exchanging sqrt(2) and -sqrt(2). Thus g=I+2M mod 4 and Mv mod 2 is independent of v: gA-A is neither O nor T1, since either would preserve x(A). Normality of the translation subgroup gives (g-I)h in H. Together with 2h these give independent vectors in (H intersect 8Z2²) mod 16. Closedness and Nakayama give 8Z2² contained in H. Thus conditional only on nonzero first layer, the index is 16 or 32, with no higher lifting obstruction. If the infinite exclusion of d2 is certified, index 32 iff d1 is square in T_infty, otherwise 16.

Remaining: exact positive containment at T32/T64/T128, or exact negative at T128 using established stabilization. No claim about Problem H. No new Magma execution by assistant.
