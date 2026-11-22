(* code/coq/F28_arithmetic_character.v

   The owner's thirty-seventh Coq file (22 November 2026).  The text is the owner's, with ONE change: the import line "From Stdlib Require Import ZArith Znumtheory Zgcd_alt Ring Lia." is written
   "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   F28_arithmetic_character_exists: prime p >= 5, p not dividing a, c ==> there is an integer r (the candidate root 24 b c^5 u, with 2 A u = 1 mod p via Z.gcd_bezout) such that
   certificate(3 r) <-> certificate(a b).  Proof read by hand: p not dividing 2A = 8 a c^3 (F28_two_A_nonzero), inverse u, relation p | a^2 (3r) - (3c)^2 (ab) from the exact identity
   a^2(3r) - (3c)^2(ab) = (2Au - 1) * 9abc^2, then F28_square_scaling_equivalence with (u, v) = (a, 3c), p not dividing 3c.
   It overlaps with F28_candidate_root_class (F28_square_scaling.v, added in review) and F28_root_arithmetic_equivalence: same conclusion, here existential and with the inverse constructed inside.
   WHAT IT DOES NOT SAY: that r is a double root (F28_candidate_singular.v, F28_integrated_candidate_bridge.v) nor anything about (-c6/p). *)

From Coq Require Import ZArith Znumtheory Zgcd_alt Ring Lia.

Open Scope Z_scope.

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_candidate_root (b c u : Z) : Z :=
  -3*F28_B b c*u.

Definition F28_square_certificate (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2-v^2).

Lemma F28_divide_product :
  forall p x y : Z,
    (p | x) ->
    (p | x*y).
Proof.
  intros p x y H.
  destruct H as [k Hk].
  exists (k*y).
  rewrite Hk.
  ring.
Qed.

Lemma F28_divide_sum :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x+y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [k Hk].
  destruct Hy as [l Hl].
  exists (k+l).
  rewrite Hk, Hl.
  ring.
Qed.

Lemma F28_divide_neg :
  forall p x : Z,
    (p | x) ->
    (p | -x).
Proof.
  intros p x H.
  destruct H as [k Hk].
  exists (-k).
  rewrite Hk.
  ring.
Qed.

Lemma F28_nonzero_product :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    ~ (p | x*y).
Proof.
  intros p x y Hp Hx Hy Hxy.
  assert (Hs : (p | x) \/ (p | y)).
  {
    eapply prime_mult.
    - exact Hp.
    - exact Hxy.
  }
  destruct Hs as [Hpx | Hpy].
  - exact (Hx Hpx).
  - exact (Hy Hpy).
Qed.

Lemma F28_not_divide_two :
  forall p : Z,
    5 <= p ->
    ~ (p | 2).
Proof.
  intros p Hlarge Hdiv.
  destruct Hdiv as [k Hk].
  destruct (Z_le_gt_dec 0 k) as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k. lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

Lemma F28_not_divide_three :
  forall p : Z,
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hlarge Hdiv.
  destruct Hdiv as [k Hk].
  destruct (Z_le_gt_dec 0 k) as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k. lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

(* ======================================== *)
(* NONDIVISIBILITY OF 2A                    *)
(* ======================================== *)

Lemma F28_two_A_nonzero :
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
    apply F28_not_divide_two.
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

Lemma F28_three_c_nonzero :
  forall p c : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    ~ (p | 3*c).
Proof.
  intros p c Hp Hlarge Hc.
  apply (F28_nonzero_product p 3 c).
  - exact Hp.
  - apply F28_not_divide_three.
    exact Hlarge.
  - exact Hc.
Qed.

(* ======================================== *)
(* PRIME MODULAR INVERSE                    *)
(* ======================================== *)

Lemma F28_prime_inverse :
  forall p s : Z,
    prime p ->
    ~ (p | s) ->
    exists u : Z, (p | s*u-1).
Proof.
  intros p s Hp Hnotdiv.

  assert (Hgcd : Z.gcd p s = 1).
  {
    apply Zis_gcd_gcd.
    - lia.
    - apply prime_rel_prime.
      + exact Hp.
      + exact Hnotdiv.
  }

  pose proof
    (Z.gcd_bezout p s 1 Hgcd) as Hbezout.

  unfold Z.Bezout in Hbezout.
  destruct Hbezout as [k [u Hidentity]].

  exists u.
  exists (-k).
  rewrite <- Hidentity.
  ring.
Qed.

(* ======================================== *)
(* GENERAL SQUARE-SCALING THEOREM           *)
(* ======================================== *)

Lemma F28_square_scaling_equivalence :
  forall p x y u v : Z,
    prime p ->
    ~ (p | u) ->
    ~ (p | v) ->
    (p | x*u^2-y*v^2) ->
    (F28_square_certificate p x <->
     F28_square_certificate p y).
Proof.
  intros p x y u v Hp Hnu Hnv Hrelation.
  split.

  - intros [k [l [Hnk Hcert]]].
    unfold F28_square_certificate.
    exists (v*k).
    exists (u*l).
    split.
    + apply (F28_nonzero_product p v k).
      * exact Hp.
      * exact Hnv.
      * exact Hnk.
    + replace
        (y*(v*k)^2-(u*l)^2)
        with
        ((-(x*u^2-y*v^2))*k^2
         +(x*k^2-l^2)*u^2)
        by ring.
      apply F28_divide_sum.
      * apply F28_divide_product.
        apply F28_divide_neg.
        exact Hrelation.
      * apply F28_divide_product.
        exact Hcert.

  - intros [k [l [Hnk Hcert]]].
    unfold F28_square_certificate.
    exists (u*k).
    exists (v*l).
    split.
    + apply (F28_nonzero_product p u k).
      * exact Hp.
      * exact Hnu.
      * exact Hnk.
    + replace
        (x*(u*k)^2-(v*l)^2)
        with
        ((x*u^2-y*v^2)*k^2
         +(y*k^2-l^2)*v^2)
        by ring.
      apply F28_divide_sum.
      * apply F28_divide_product.
        exact Hrelation.
      * apply F28_divide_product.
        exact Hcert.
Qed.

(* ======================================== *)
(* EXACT CANDIDATE ROOT IDENTITY            *)
(* ======================================== *)

Lemma F28_candidate_identity :
  forall a b c u : Z,
    a^2*(3*F28_candidate_root b c u)
      -(3*c)^2*(a*b)
    =
    (2*F28_A a c*u-1)*(9*a*b*c^2).
Proof.
  intros a b c u.
  unfold F28_candidate_root, F28_A, F28_B.
  ring.
Qed.

(* ======================================== *)
(* INTEGRATED ARITHMETIC THEOREM            *)
(* ======================================== *)

Theorem F28_arithmetic_character_exists :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    exists r : Z,
      (F28_square_certificate p (3*r) <->
       F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hc.

  assert (HA : ~ (p | 2*F28_A a c)).
  {
    apply F28_two_A_nonzero.
    - exact Hp.
    - exact Hlarge.
    - exact Ha.
    - exact Hc.
  }

  destruct
    (F28_prime_inverse p (2*F28_A a c)
      Hp HA) as [u Hu].

  exists (F28_candidate_root b c u).

  assert (Hrelation :
    (p |
      (3*F28_candidate_root b c u)*a^2
      -(a*b)*(3*c)^2)).
  {
    replace
      ((3*F28_candidate_root b c u)*a^2
       -(a*b)*(3*c)^2)
      with
      (a^2*(3*F28_candidate_root b c u)
       -(3*c)^2*(a*b))
      by ring.

    rewrite F28_candidate_identity.
    apply F28_divide_product.
    exact Hu.
  }

  apply
    (F28_square_scaling_equivalence
      p
      (3*F28_candidate_root b c u)
      (a*b)
      a
      (3*c)).
  - exact Hp.
  - exact Ha.
  - apply F28_three_c_nonzero.
    + exact Hp.
    + exact Hlarge.
    + exact Hc.
  - exact Hrelation.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_arithmetic_character_exists.
Print Assumptions F28_arithmetic_character_exists.
