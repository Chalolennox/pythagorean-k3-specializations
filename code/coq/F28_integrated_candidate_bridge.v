(* code/coq/F28_integrated_candidate_bridge.v

   The owner's thirty-ninth Coq file (22 November 2026).  The text is the owner's, with ONE change: the import line "From Stdlib Require Import ZArith Znumtheory Ring." is written
   "From Coq Require Import ZArith Znumtheory Ring." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   F28_integrated_candidate_bridge: prime p, p not dividing a, 3c, p | F(a,b,c), p | 2 A u - 1 (A = 4 a c^3) ==> for the candidate root r = -3 B u = 24 b c^5 u of the paper's model:
     p | r^3 + A r + B  AND  p | 3 r^2 + A  AND  (certificate(3 r) <-> certificate(ab)).
   Checked by hand: the singularity part is that of F28_candidate_singular.v; the class part is F28_square_scaling_equivalence with the exact identity a^2(3r) - (3c)^2(ab) = (2Au - 1) 9abc^2.
   THIS IS THE COMPOSED STATEMENT for the candidate root: it is a double root and its class is that of ab.  Combined with the tangent criterion at that same r (F28_large_prime_tangent_character,
   valid for EVERY double root r with p >= 5, p not dividing A: certificate(864 B) <-> certificate(3 r)) it gives certificate(864 B) <-> certificate(ab), i.e. (-c6/p) = (ab/p); no uniqueness of the
   double root is needed.  That last composition is still two files apart (the files are standalone). *)

From Coq Require Import ZArith Znumtheory Ring.

Open Scope Z_scope.

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
(* DIVISIBILITY HELPERS                     *)
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
(* SQUARE-CLASS TRANSPORT                   *)
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
(* DISCRIMINANT                             *)
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
(* SINGULARITY FROM DISCRIMINANT            *)
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
(* INTEGRATED F.28 ARITHMETIC BRIDGE        *)
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
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_integrated_candidate_bridge.

Print Assumptions F28_integrated_candidate_bridge.
