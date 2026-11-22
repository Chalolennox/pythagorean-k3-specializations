(* code/coq/F28_square_scaling.v

   The owner's thirty-fourth Coq file (22 November 2026).  Everything before the line "ADDED IN REVIEW" is the owner's text with ONE change: the import line
   "From Stdlib Require Import ZArith Znumtheory Ring." is written "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.
   Standalone.  WHAT IT PROVES (checked by hand):
     F28_square_scaling_equivalence: prime p, p not dividing u, v, p | x u^2 - y v^2 ==> (certificate(x) <-> certificate(y))
       (witnesses v k, u l resp. u k, v l; y (v k)^2 - (u l)^2 = -(x u^2 - y v^2) k^2 + (x k^2 - l^2) u^2 and x (u k)^2 - (v l)^2 = (x u^2 - y v^2) k^2 + (y k^2 - l^2) v^2);
     F28_root_arithmetic_equivalence: prime p, p not dividing a, 3c, p | a^2 (3r) - (3c)^2 (ab) ==> (certificate(3r) <-> certificate(ab)).
   This is the bridge from the double root r to the paper's character: on the integral model r = 3 b c^2 / a mod p, so 3 r a^2 = a b (3c)^2 mod p and the class of 3r is that of ab.
   It replaces the remark 3 n d = ab (24 c^4)^2 of F28_discriminant_root.v by a statement about certificates.  WHAT IT DOES NOT PROVE: that the relation holds for the double root
   (see F28_candidate_root_relation.v and the added theorem), nor the Tate/Silverman bridge.
   ADDED IN REVIEW: F28_candidate_root_class: for the candidate root r = 24 b c^5 u of the paper's model (u with 8 a c^3 u = 1 mod p), certificate(3 r) <-> certificate(ab) for prime p >= 5 not
   dividing a, c (composition with the identity of the thirty-fifth file). *)

From Coq Require Import ZArith Znumtheory Ring.

Open Scope Z_scope.

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

(* ======================================== *)
(* GENERAL SQUARE-SCALING EQUIVALENCE       *)
(* ======================================== *)

Theorem F28_square_scaling_equivalence :
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

  - intros Hx.
    destruct Hx as [k [l [Hnk Hcert]]].
    unfold F28_square_certificate.
    exists (v*k).
    exists (u*l).
    split.
    + apply F28_nonzero_product.
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

  - intros Hy.
    destruct Hy as [k [l [Hnk Hcert]]].
    unfold F28_square_certificate.
    exists (u*k).
    exists (v*l).
    split.
    + apply F28_nonzero_product.
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
(* SPECIALIZED ARITHMETIC BRIDGE            *)
(* ======================================== *)

Theorem F28_root_arithmetic_equivalence :
  forall p a b c r : Z,
    prime p ->
    ~ (p | a) ->
    ~ (p | 3*c) ->
    (p | a^2*(3*r)-(3*c)^2*(a*b)) ->
    (F28_square_certificate p (3*r) <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c r Hp Ha H3c Hrelation.

  assert
    (Hnormalized :
      (p | (3*r)*a^2-(a*b)*(3*c)^2)).
  {
    replace
      ((3*r)*a^2-(a*b)*(3*c)^2)
      with
      (a^2*(3*r)-(3*c)^2*(a*b))
      by ring.
    exact Hrelation.
  }

  apply (F28_square_scaling_equivalence
    p (3*r) (a*b) a (3*c)).
  - exact Hp.
  - exact Ha.
  - exact H3c.
  - exact Hnormalized.
Qed.

Check F28_square_scaling_equivalence.
Check F28_root_arithmetic_equivalence.

Print Assumptions F28_root_arithmetic_equivalence.

(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026)       *)
(* ======================================== *)

From Coq Require Import Lia.

Lemma F28_large_prime_not_divide_three :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hp Hlarge Hdiv.
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

(* r = -3 B u = 24 b c^5 u, A = 4 a c^3, B = -8 b c^5: a^2 (3 r) - (3c)^2 (ab) = (2 A u - 1) * 9 a b c^2 (the identity of the thirty-fifth file). *)
Theorem F28_candidate_root_class :
  forall p a b c u : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | 2*(4*a*c^3)*u-1) ->
    (F28_square_certificate p (3*(-3*(-8*b*c^5)*u))
     <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c u Hp Hlarge Ha Hc Hinverse.

  assert (H3 : ~ (p | 3)).
  {
    apply (F28_large_prime_not_divide_three p).
    - exact Hp.
    - exact Hlarge.
  }

  assert (H3c : ~ (p | 3*c)).
  {
    apply (F28_nonzero_product p 3 c).
    - exact Hp.
    - exact H3.
    - exact Hc.
  }

  assert (Hrelation :
    (p | a^2*(3*(-3*(-8*b*c^5)*u))-(3*c)^2*(a*b))).
  {
    replace
      (a^2*(3*(-3*(-8*b*c^5)*u))-(3*c)^2*(a*b))
      with
      ((2*(4*a*c^3)*u-1)*(9*a*b*c^2))
      by ring.
    apply F28_divide_product.
    exact Hinverse.
  }

  apply (F28_root_arithmetic_equivalence
    p a b c (-3*(-8*b*c^5)*u)).
  - exact Hp.
  - exact Ha.
  - exact H3c.
  - exact Hrelation.
Qed.

Print Assumptions F28_candidate_root_class.
