(* code/coq/F28_complete_arithmetic_bridge.v

   The owner's fortieth Coq file (22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Zgcd_alt Ring Lia." (split over two lines) is written
   "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone; it contains the lemmas of files 36-39.
   F28_complete_arithmetic_bridge: prime p >= 5, p not dividing a, c, p | F(a,b,c) = 4 a^3 + 27 b^2 c ==> there is an integer r with
     p | r^3 + A r + B,  p | 3 r^2 + A  (A = 4 a c^3, B = -8 b c^5; a double root mod p)  AND  (certificate(3 r) <-> certificate(a b)).
   Proof (read by hand): p not dividing 2A (F28_two_A_nonzero), inverse u of 2A mod p (Z.gcd_bezout), r = -3 B u = 24 b c^5 u, then F28_integrated_candidate_bridge (39th file: singularity from p | Delta = -64 c^9 F,
   class from the identity a^2(3r) - (3c)^2(ab) = (2Au - 1) * 9abc^2 and F28_square_scaling_equivalence), with p not dividing 3c.
   THIS IS THE CLOSED ARITHMETIC THEOREM FOR THE PAPER'S MODEL: from p | F to a double root whose tangent coefficient 3r has the square class of ab.  Together with the tangent criterion
   (F28_large_prime_tangent_character: certificate(864 B) <-> certificate(3 r) at every double root r with p >= 5, p not dividing A) one gets certificate(864 B) <-> certificate(a b) at that r.
   WHAT IT DOES NOT PROVE: that p not dividing a, c follows from the Pythagorean hypotheses (F28_main_arithmetic, F28_arithmetic.v); the Tate/Silverman bridge; minimality; root numbers; the parametrization. *)

From Coq Require Import
  ZArith Znumtheory Zgcd_alt Ring Lia.

Open Scope Z_scope.

(* ======================================== *)
(* DEFINITIONS                              *)
(* ======================================== *)

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_F (a b c : Z) : Z :=
  4*a^3+27*b^2*c.

Definition F28_cubic (A B x : Z) : Z :=
  x^3+A*x+B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2+A.

Definition F28_discriminant (A B : Z) : Z :=
  -4*A^3-27*B^2.

Definition F28_candidate_root (b c u : Z) : Z :=
  -3*F28_B b c*u.

Definition F28_square_certificate (p x : Z) : Prop :=
  exists k l : Z,
    ~ (p | k) /\
    (p | x*k^2-l^2).

(* ======================================== *)
(* DIVISIBILITY                             *)
(* ======================================== *)

Lemma F28_divide_product :
  forall p x y : Z,
    (p | x) -> (p | x*y).
Proof.
  intros p x y H.
  destruct H as [k Hk].
  exists (k*y).
  rewrite Hk.
  ring.
Qed.

Lemma F28_divide_sum :
  forall p x y : Z,
    (p | x) -> (p | y) -> (p | x+y).
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
    (p | x) -> (p | -x).
Proof.
  intros p x H.
  destruct H as [k Hk].
  exists (-k).
  rewrite Hk.
  ring.
Qed.

Lemma F28_divide_difference :
  forall p x y : Z,
    (p | x) -> (p | y) -> (p | x-y).
Proof.
  intros p x y Hx Hy.
  apply F28_divide_sum.
  - exact Hx.
  - apply F28_divide_neg.
    exact Hy.
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

(* ======================================== *)
(* SMALL CONSTANTS                          *)
(* ======================================== *)

Lemma F28_not_divide_two :
  forall p : Z,
    5 <= p -> ~ (p | 2).
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
    5 <= p -> ~ (p | 3).
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
(* NONZERO COEFFICIENTS                     *)
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
      (F28_nonzero_product p 2 (a*(c*(c*c)))).
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
(* MODULAR INVERSE                          *)
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
(* SQUARE-CLASS SCALING                     *)
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
(* DISCRIMINANT IDENTITIES                  *)
(* ======================================== *)

Lemma F28_discriminant_identity :
  forall a b c : Z,
    F28_discriminant
      (F28_A a c) (F28_B b c)
    =
    -64*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_discriminant, F28_A, F28_B, F28_F.
  ring.
Qed.

Lemma F28_F_divides_discriminant :
  forall p a b c : Z,
    (p | F28_F a b c) ->
    (p |
      F28_discriminant
        (F28_A a c) (F28_B b c)).
Proof.
  intros p a b c HF.
  rewrite F28_discriminant_identity.
  replace (-64*c^9*F28_F a b c)
    with (F28_F a b c*(-64*c^9))
    by ring.
  apply F28_divide_product.
  exact HF.
Qed.

(* ======================================== *)
(* CANDIDATE ROOT IDENTITIES                *)
(* ======================================== *)

Lemma F28_candidate_derivative_identity :
  forall A B u : Z,
    F28_derivative A (-3*B*u)
    =
    -(u^2)*F28_discriminant A B
    -A*((2*A*u-1)*(2*A*u+1)).
Proof.
  intros A B u.
  unfold F28_derivative, F28_discriminant.
  ring.
Qed.

Lemma F28_candidate_cubic_identity :
  forall A B u : Z,
    F28_cubic A B (-3*B*u)
    =
    B*F28_discriminant A B*u^3
    -(2*A*u-1)*
      (A*(-3*B)*u*(2*A*u+1)
       +B*((2*A*u)^2+2*A*u+1)).
Proof.
  intros A B u.
  unfold F28_cubic, F28_discriminant.
  ring.
Qed.

Lemma F28_candidate_arithmetic_identity :
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
(* SINGULARITY                              *)
(* ======================================== *)

Lemma F28_candidate_derivative_zero :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | 2*A*u-1) ->
    (p | F28_derivative A (-3*B*u)).
Proof.
  intros p A B u HD Hu.
  rewrite F28_candidate_derivative_identity.
  apply F28_divide_difference.
  - replace
      (-(u^2)*F28_discriminant A B)
      with
      (F28_discriminant A B*(-u^2))
      by ring.
    apply F28_divide_product.
    exact HD.
  - replace
      (A*((2*A*u-1)*(2*A*u+1)))
      with
      ((2*A*u-1)*(A*(2*A*u+1)))
      by ring.
    apply F28_divide_product.
    exact Hu.
Qed.

Lemma F28_candidate_cubic_zero :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | 2*A*u-1) ->
    (p | F28_cubic A B (-3*B*u)).
Proof.
  intros p A B u HD Hu.
  rewrite F28_candidate_cubic_identity.
  apply F28_divide_difference.
  - replace
      (B*F28_discriminant A B*u^3)
      with
      (F28_discriminant A B*(B*u^3))
      by ring.
    apply F28_divide_product.
    exact HD.
  - apply F28_divide_product.
    exact Hu.
Qed.

(* ======================================== *)
(* INTEGRATED CANDIDATE BRIDGE              *)
(* ======================================== *)

Theorem F28_integrated_candidate_bridge :
  forall p a b c u : Z,
    prime p ->
    ~ (p | a) ->
    ~ (p | 3*c) ->
    (p | F28_F a b c) ->
    (p | 2*F28_A a c*u-1) ->
    let r := F28_candidate_root b c u in
      (p | F28_cubic
        (F28_A a c) (F28_B b c) r)
      /\
      (p | F28_derivative (F28_A a c) r)
      /\
      (F28_square_certificate p (3*r) <->
       F28_square_certificate p (a*b)).
Proof.
  intros p a b c u Hp Ha H3c HF Hu.
  simpl.

  assert (HD :
    (p |
      F28_discriminant
        (F28_A a c) (F28_B b c))).
  {
    apply F28_F_divides_discriminant.
    exact HF.
  }

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
    rewrite F28_candidate_arithmetic_identity.
    apply F28_divide_product.
    exact Hu.
  }

  split.
  - unfold F28_candidate_root.
    apply F28_candidate_cubic_zero.
    + exact HD.
    + exact Hu.

  - split.
    + unfold F28_candidate_root.
      apply F28_candidate_derivative_zero.
      * exact HD.
      * exact Hu.

    + apply
        (F28_square_scaling_equivalence
          p
          (3*F28_candidate_root b c u)
          (a*b)
          a
          (3*c)).
      * exact Hp.
      * exact Ha.
      * exact H3c.
      * exact Hrelation.
Qed.

(* ======================================== *)
(* FINAL EXISTENTIAL THEOREM                *)
(* ======================================== *)

Theorem F28_complete_arithmetic_bridge :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    exists r : Z,
      (p | F28_cubic
        (F28_A a c) (F28_B b c) r)
      /\
      (p | F28_derivative (F28_A a c) r)
      /\
      (F28_square_certificate p (3*r) <->
       F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.

  assert (HA : ~ (p | 2*F28_A a c)).
  {
    apply F28_two_A_nonzero.
    - exact Hp.
    - exact Hlarge.
    - exact Ha.
    - exact Hc.
  }

  destruct
    (F28_prime_inverse
      p (2*F28_A a c) Hp HA)
    as [u Hu].

  exists (F28_candidate_root b c u).

  apply
    (F28_integrated_candidate_bridge
      p a b c u).
  - exact Hp.
  - exact Ha.
  - apply F28_three_c_nonzero.
    + exact Hp.
    + exact Hlarge.
    + exact Hc.
  - exact HF.
  - exact Hu.
Qed.

(* ======================================== *)
(* FINAL VERIFICATION                       *)
(* ======================================== *)

Check F28_integrated_candidate_bridge.
Check F28_complete_arithmetic_bridge.

Print Assumptions F28_complete_arithmetic_bridge.
