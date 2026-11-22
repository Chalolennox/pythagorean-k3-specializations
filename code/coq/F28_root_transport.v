(* code/coq/F28_root_transport.v

   The owner's twenty-third Coq file (22 November 2026), unchanged except for this header.  Standalone; four ring identities (all checked by hand).
   WHAT IT PROVES: the "transport" of a rational root q/s to an integer root q u when s u = 1 mod p:
     f'(q u) = u^2 (3 q^2 + A s^2) - A (s u - 1)(s u + 1),
     f(q u)  = u^3 (q^3 + A q s^2 + B s^3) - (s u - 1)(A q u (s u + 1) + B ((s u)^2 + s u + 1)),
   and their specializations to (q, s) = (-3B, 2A): f'(-3B u) = -u^2 Delta - A (2 A u - 1)(2 A u + 1), f(-3B u) = B u^3 Delta - (2 A u - 1)(...).
   Hence, if p | Delta and u inverts 2A mod p (2 A u = 1 + (multiple of p)), r = -3B u is an integer double root of f mod p.
   WHAT IT DOES NOT PROVE: the existence of u (Bezout, primality of p) and the divisibilities themselves; both are in F28_large_prime_tangent.v
   (F28_double_root_exists, F28_discriminant_split_criterion, which repeat the two specialized identities). *)
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
(* SCALED DISCRIMINANT IDENTITIES           *)
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
(* DERIVATIVE TRANSPORT IDENTITY            *)
(* ======================================== *)

Theorem F28_derivative_transport_identity :
  forall A q s u : Z,
    F28_derivative A (q*u)
    =
    u^2*(3*q^2 + A*s^2)
      - A*(s*u-1)*(s*u+1).
Proof.
  intros A q s u.
  unfold F28_derivative.
  ring.
Qed.

(* ======================================== *)
(* CUBIC TRANSPORT IDENTITY                 *)
(* ======================================== *)

Theorem F28_cubic_transport_identity :
  forall A B q s u : Z,
    F28_cubic A B (q*u)
    =
    u^3*(q^3 + A*q*s^2 + B*s^3)
    - (s*u-1)*
      (A*q*u*(s*u+1)
       + B*((s*u)^2+s*u+1)).
Proof.
  intros A B q s u.
  unfold F28_cubic.
  ring.
Qed.

(* ======================================== *)
(* SPECIALIZED DERIVATIVE IDENTITY          *)
(* ======================================== *)

Theorem F28_candidate_derivative_identity :
  forall A B u : Z,
    F28_derivative A
      (F28_root_numerator B*u)
    =
    -u^2*F28_discriminant A B
    - A*
      (F28_root_denominator A*u-1)*
      (F28_root_denominator A*u+1).
Proof.
  intros A B u.
  unfold F28_derivative.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  unfold F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* SPECIALIZED CUBIC IDENTITY               *)
(* ======================================== *)

Theorem F28_candidate_cubic_identity :
  forall A B u : Z,
    F28_cubic A B
      (F28_root_numerator B*u)
    =
    B*u^3*F28_discriminant A B
    -
    (F28_root_denominator A*u-1)*
    (A*(F28_root_numerator B)*u*
       (F28_root_denominator A*u+1)
     + B*
       ((F28_root_denominator A*u)^2
        + F28_root_denominator A*u+1)).
Proof.
  intros A B u.
  unfold F28_cubic.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  unfold F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_derivative_transport_identity.
Check F28_cubic_transport_identity.
Check F28_candidate_derivative_identity.
Check F28_candidate_cubic_identity.

Print Assumptions F28_candidate_derivative_identity.
Print Assumptions F28_candidate_cubic_identity.
