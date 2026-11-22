(* code/coq/F28_two_A_nonzero.v

   The owner's thirty-sixth Coq file (22 November 2026).  The text is the owner's, with ONE change: the import line "From Stdlib Require Import ZArith Znumtheory Ring Lia." is written
   "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   NOTE ON THE SUBMISSION: the message carrying this file continued, after the line "Print Assumptions F28_two_A_nonzero.", with stray fragments ("Qed. Qed.", an unfinished second proof
   of the same lemma, a dangling "exact Hlarge. - exact Hc. Qed.") that do not compile; they are NOT included here.  The file ends at the Print Assumptions line.
   F28_two_A_nonzero: prime p >= 5, p not dividing a, c ==> p not dividing 2 A = 8 a c^3  (the product of the non-divisible factors 2, 2, 2, a, c, c, c, peeled one at a time with prime_mult;
   2 * F28_A a c = 2*(2*(2*(a*(c*(c*c))))) by ring).
   This is exactly the hypothesis ~(p | 2*A) of F28_double_root_exists (F28_large_prime_tangent.v) for the paper's model; the same fact is already used inside
   F28_specialized_singular_root.v in the form p not dividing A together with p >= 5.  Nothing new mathematically. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Lemma F28_nonzero_product :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    ~ (p | x*y).
Proof.
  intros p x y Hp Hx Hy Hxy.
  assert (Hsplit : (p | x) \/ (p | y)).
  {
    eapply prime_mult.
    - exact Hp.
    - exact Hxy.
  }
  destruct Hsplit as [Hpx | Hpy].
  - exact (Hx Hpx).
  - exact (Hy Hpy).
Qed.

Lemma F28_large_prime_not_divide_two :
  forall p : Z,
    5 <= p ->
    ~ (p | 2).
Proof.
  intros p Hlarge Hdiv.
  destruct Hdiv as [k Hk].
  destruct (Z_le_gt_dec 0 k) as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k.
      lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

(* ======================================== *)
(* NONDIVISIBILITY OF 2A                    *)
(* ======================================== *)

Theorem F28_two_A_nonzero :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    ~ (p | 2*F28_A a c).
Proof.
  intros p a c Hp Hlarge Ha Hc.

  assert (H2 : ~ (p | 2)).
  {
    apply F28_large_prime_not_divide_two.
    exact Hlarge.
  }

  assert (Hcc : ~ (p | c*c)).
  {
    apply (F28_nonzero_product p c c).
    - exact Hp.
    - exact Hc.
    - exact Hc.
  }

  assert (Hccc : ~ (p | c*(c*c))).
  {
    apply (F28_nonzero_product p c (c*c)).
    - exact Hp.
    - exact Hc.
    - exact Hcc.
  }

  assert (Haccc : ~ (p | a*(c*(c*c)))).
  {
    apply (F28_nonzero_product p a (c*(c*c))).
    - exact Hp.
    - exact Ha.
    - exact Hccc.
  }

  assert (Hfirst :
    ~ (p | 2*(a*(c*(c*c))))).
  {
    apply
      (F28_nonzero_product
        p 2 (a*(c*(c*c)))).
    - exact Hp.
    - exact H2.
    - exact Haccc.
  }

  assert (Hsecond :
    ~ (p | 2*(2*(a*(c*(c*c)))))).
  {
    apply
      (F28_nonzero_product
        p 2 (2*(a*(c*(c*c))))).
    - exact Hp.
    - exact H2.
    - exact Hfirst.
  }

  assert (Hthird :
    ~ (p | 2*(2*(2*(a*(c*(c*c))))))).
  {
    apply
      (F28_nonzero_product
        p 2 (2*(2*(a*(c*(c*c)))))).
    - exact Hp.
    - exact H2.
    - exact Hsecond.
  }

  replace (2*F28_A a c)
    with (2*(2*(2*(a*(c*(c*c))))))
    by (unfold F28_A; ring).

  exact Hthird.
Qed.

Check F28_two_A_nonzero.
Print Assumptions F28_two_A_nonzero.
