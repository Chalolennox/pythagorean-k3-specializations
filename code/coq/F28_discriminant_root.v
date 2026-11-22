(* code/coq/F28_discriminant_root.v

   The owner's twenty-second Coq file (22 November 2026): everything before the line "ADDED IN REVIEW" is the owner's text unchanged except for
   this header.  Standalone.  For f(X) = X^3 + A X + B with Delta = -4 A^3 - 27 B^2, n = -3B, d = 2A:
     F28_scaled_derivative_identity: 3 n^2 + A d^2 = -Delta;   F28_scaled_cubic_identity: n^3 + A n d^2 + B d^3 = B Delta
   (both checked by hand: 27 B^2 + 4 A^3 = -Delta and -27 B^3 - 12 A^3 B + 8 A^3 B = B (-4 A^3 - 27 B^2)); hence p | Delta gives p | 3 n^2 + A d^2 and
   p | n^3 + A n d^2 + B d^3: (n : d) = (-3B : 2A) is a double root of the cubic mod p when 2A is invertible (r = -3B/(2A)).
   WHAT IT DOES NOT PROVE: the passage to an integer root r (needs the inverse of 2A mod p), done in F28_root_transport.v and F28_large_prime_tangent.v.
   WHAT IS ADDED: for the integral model A = 4 a c^3, B = -8 b c^5: Delta = -64 c^9 F(a,b,c) and 3 n d = a b (24 c^4)^2 (so the class of 3r = 3 n d / d^2
   is that of ab: the root of the paper's model satisfies (3r/p) = (ab/p)). *)
From Coq Require Import ZArith.
From Coq Require Import Ring.

Open Scope Z_scope.

Definition F28_cubic (A B x : Z) : Z :=
  x^3 + A*x + B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_discriminant (A B : Z) : Z :=
  -4*A^3 - 27*B^2.

Definition F28_root_numerator (B : Z) : Z :=
  -3*B.

Definition F28_root_denominator (A : Z) : Z :=
  2*A.

(* ======================================== *)
(* CORRECT SCALED DERIVATIVE IDENTITY       *)
(* ======================================== *)

Theorem F28_scaled_derivative_identity :
  forall A B : Z,
    3*(F28_root_numerator B)^2
    + A*(F28_root_denominator A)^2
    =
    -F28_discriminant A B.
Proof.
  intros A B.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  unfold F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* SCALED CUBIC IDENTITY                    *)
(* ======================================== *)

Theorem F28_scaled_cubic_identity :
  forall A B : Z,
    (F28_root_numerator B)^3
    + A*(F28_root_numerator B)
       *(F28_root_denominator A)^2
    + B*(F28_root_denominator A)^3
    =
    B*F28_discriminant A B.
Proof.
  intros A B.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  unfold F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* DIVISIBILITY HELPERS                     *)
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
(* DERIVATIVE DIVISIBILITY                  *)
(* ======================================== *)

Theorem F28_scaled_derivative_divisible :
  forall p A B : Z,
    (p | F28_discriminant A B) ->
    (p |
      3*(F28_root_numerator B)^2
      + A*(F28_root_denominator A)^2).
Proof.
  intros p A B HD.

  rewrite F28_scaled_derivative_identity.

  destruct HD as [k Hk].
  exists (-k).
  rewrite Hk.
  ring.
Qed.

(* ======================================== *)
(* CUBIC DIVISIBILITY                       *)
(* ======================================== *)

Theorem F28_scaled_cubic_divisible :
  forall p A B : Z,
    (p | F28_discriminant A B) ->
    (p |
      (F28_root_numerator B)^3
      + A*(F28_root_numerator B)
         *(F28_root_denominator A)^2
      + B*(F28_root_denominator A)^3).
Proof.
  intros p A B HD.

  rewrite F28_scaled_cubic_identity.

  replace (B*F28_discriminant A B)
    with (F28_discriminant A B*B)
    by ring.

  apply F28_divide_product.
  exact HD.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_scaled_derivative_identity.
Check F28_scaled_cubic_identity.
Check F28_scaled_derivative_divisible.
Check F28_scaled_cubic_divisible.

Print Assumptions F28_scaled_derivative_divisible.
Print Assumptions F28_scaled_cubic_divisible.

(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026): the integral model of the paper *)
(* ======================================== *)

Theorem F28_integral_discriminant_identity :
  forall a b c : Z,
    F28_discriminant (4*a*c^3) (-8*b*c^5)
    =
    -64*c^9*(4*a^3 + 27*b^2*c).
Proof.
  intros a b c.
  unfold F28_discriminant.
  ring.
Qed.

Theorem F28_integral_discriminant_divisible :
  forall p a b c : Z,
    (p | 4*a^3 + 27*b^2*c) ->
    (p | F28_discriminant (4*a*c^3) (-8*b*c^5)).
Proof.
  intros p a b c HF.
  rewrite F28_integral_discriminant_identity.
  replace (-64*c^9*(4*a^3 + 27*b^2*c))
    with ((4*a^3 + 27*b^2*c)*(-64*c^9))
    by ring.
  apply F28_divide_product.
  exact HF.
Qed.

Theorem F28_integral_root_class_identity :
  forall a b c : Z,
    3*(F28_root_numerator (-8*b*c^5))
      *(F28_root_denominator (4*a*c^3))
    =
    (a*b)*(24*c^4)^2.
Proof.
  intros a b c.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  ring.
Qed.

Print Assumptions F28_integral_root_class_identity.
