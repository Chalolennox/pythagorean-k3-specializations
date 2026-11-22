(* code/coq/F28_integral_invariants.v

   The owner's forty-fifth Coq file (22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Ring." is written "From Coq Require Import ZArith Ring."
   (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   For the integral model Y^2 = X^3 + A X + B with A = 4 a c^3, B = -8 b c^5 and F = 4 a^3 + 27 b^2 c, with the standard invariants c4 = -48 A, c6 = -864 B, Delta = -16 (4 A^3 + 27 B^2):
     c4 = -192 a c^3, c6 = 6912 b c^5, Delta = -1024 c^9 F  (all by ring; checked by hand: 4 A^3 + 27 B^2 = 256 a^3 c^9 + 1728 b^2 c^10 = 64 c^9 F);
     F28_F_divides_discriminant: p | F ==> p | Delta;
     F28_reduction_invariant_certificate: p | F and p not dividing -192 a c^3 ==> p | Delta and p not dividing c4  (the numerical criterion of multiplicative reduction, Silverman VII.1.1/Tate).
   The same invariants (with the powers of c included) are in F28_reduction_invariants.v and F28_primitive_reduction.v (14th/15th files); nothing new mathematically, and the identification of
   "p | Delta, p not dividing c4" with multiplicative reduction and minimality is Silverman/Tate, not in Coq. *)

From Coq Require Import ZArith Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: INTEGRAL WEIERSTRASS MODEL         *)
(* ======================================== *)

Definition F28_F (a b c : Z) : Z :=
  4*a^3+27*b^2*c.

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_c4 (A : Z) : Z :=
  -48*A.

Definition F28_c6 (B : Z) : Z :=
  -864*B.

Definition F28_discriminant (A B : Z) : Z :=
  -16*(4*A^3+27*B^2).

(* ======================================== *)
(* EXACT INVARIANT IDENTITIES               *)
(* ======================================== *)

Theorem F28_c4_identity :
  forall a c : Z,
    F28_c4 (F28_A a c) =
    -192*a*c^3.
Proof.
  intros a c.
  unfold F28_c4, F28_A.
  ring.
Qed.

Theorem F28_c6_identity :
  forall b c : Z,
    F28_c6 (F28_B b c) =
    6912*b*c^5.
Proof.
  intros b c.
  unfold F28_c6, F28_B.
  ring.
Qed.

Theorem F28_discriminant_identity :
  forall a b c : Z,
    F28_discriminant
      (F28_A a c) (F28_B b c) =
    -1024*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_discriminant.
  unfold F28_A, F28_B, F28_F.
  ring.
Qed.

(* ======================================== *)
(* DIVISIBILITY BY A FACTOR                 *)
(* ======================================== *)

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

(* ======================================== *)
(* DISCRIMINANT DIVISIBILITY                *)
(* ======================================== *)

Theorem F28_F_divides_discriminant :
  forall p a b c : Z,
    (p | F28_F a b c) ->
    (p | F28_discriminant
           (F28_A a c) (F28_B b c)).
Proof.
  intros p a b c HF.
  rewrite F28_discriminant_identity.
  replace (-1024*c^9*F28_F a b c)
    with (F28_F a b c*(-1024*c^9))
    by ring.
  apply F28_divide_product.
  exact HF.
Qed.

(* ======================================== *)
(* NONVANISHING OF c4                       *)
(* ======================================== *)

Theorem F28_c4_nonzero_certificate :
  forall p a c : Z,
    ~ (p | -192*a*c^3) ->
    ~ (p | F28_c4 (F28_A a c)).
Proof.
  intros p a c H.
  rewrite F28_c4_identity.
  exact H.
Qed.

(* ======================================== *)
(* COMBINED REDUCTION CERTIFICATE           *)
(* ======================================== *)

Definition F28_multiplicative_invariant_condition
  (p A B : Z) : Prop :=
  (p | F28_discriminant A B) /\
  ~ (p | F28_c4 A).

Theorem F28_reduction_invariant_certificate :
  forall p a b c : Z,
    (p | F28_F a b c) ->
    ~ (p | -192*a*c^3) ->
    F28_multiplicative_invariant_condition
      p (F28_A a c) (F28_B b c).
Proof.
  intros p a b c HF Hc4.
  unfold F28_multiplicative_invariant_condition.
  split.
  - apply F28_F_divides_discriminant.
    exact HF.
  - apply F28_c4_nonzero_certificate.
    exact Hc4.
Qed.

(* ======================================== *)
(* TYPECHECKING                             *)
(* ======================================== *)

Check F28_c4_identity.
Check F28_c6_identity.
Check F28_discriminant_identity.
Check F28_F_divides_discriminant.
Check F28_reduction_invariant_certificate.

Print Assumptions F28_reduction_invariant_certificate.
