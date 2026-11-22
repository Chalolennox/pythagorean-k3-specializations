(* code/coq/F28_inverse_existence.v

   The owner's twenty-seventh Coq file (22 November 2026).  The text is the owner's, with ONE change: the five imports "From Stdlib Require Import ..." (Rocq 9
   naming) are written "From Coq Require Import ..." because the CI compiles with Coq 8.20.1, where the prefix Stdlib does not exist.  Plus this header.
   Standalone.  WHAT IT PROVES (all checked by hand):
     F28_bezout_to_inverse: p k + s u = 1 ==> p | s u - 1 (s u - 1 = -p k);
     F28_coprime_inverse: gcd(p, s) = 1 ==> some u with p | s u - 1 (Z.gcd_bezout);
     F28_prime_inverse: prime p, p not dividing s ==> some u with p | s u - 1 (prime_rel_prime, Zis_gcd_gcd);
     F28_denominator_inverse: the same for s = 2A.
   This supplies the existence of u that the twenty-fourth to twenty-sixth files assumed; it is the same Bezout step as in F28_double_root_exists
   (F28_large_prime_tangent.v), reached through Z.gcd_bezout instead of rel_prime_bezout. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Zgcd_alt.
From Coq Require Import Ring.
From Coq Require Import Lia.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: MODULAR INVERSE EXISTENCE          *)
(* ======================================== *)

Definition F28_root_denominator (A : Z) : Z :=
  2*A.

(* ======================================== *)
(* BEZOUT IDENTITY TO MODULAR INVERSE       *)
(* ======================================== *)

Theorem F28_bezout_to_inverse :
  forall p s k u : Z,
    p*k + s*u = 1 ->
    (p | s*u-1).
Proof.
  intros p s k u H.
  exists (-k).
  rewrite <- H.
  ring.
Qed.

(* ======================================== *)
(* COPRIMALITY TO MODULAR INVERSE           *)
(* ======================================== *)

Theorem F28_coprime_inverse :
  forall p s : Z,
    Z.gcd p s = 1 ->
    exists u : Z, (p | s*u-1).
Proof.
  intros p s Hgcd.

  pose proof
    (Z.gcd_bezout p s 1 Hgcd)
    as Hbezout.

  unfold Z.Bezout in Hbezout.
  destruct Hbezout as [k [u Hidentity]].

  exists u.
  apply (F28_bezout_to_inverse p s k u).

  rewrite <- Hidentity.
  ring.
Qed.

(* ======================================== *)
(* PRIME NONDIVISIBILITY TO COPRIMALITY     *)
(* ======================================== *)

Theorem F28_prime_inverse :
  forall p s : Z,
    prime p ->
    ~ (p | s) ->
    exists u : Z, (p | s*u-1).
Proof.
  intros p s Hp Hnotdiv.

  apply F28_coprime_inverse.

  apply Zis_gcd_gcd.
  - lia.
  - apply prime_rel_prime.
    + exact Hp.
    + exact Hnotdiv.
Qed.

(* ======================================== *)
(* APPLICATION TO DENOMINATOR 2A            *)
(* ======================================== *)

Theorem F28_denominator_inverse :
  forall p A : Z,
    prime p ->
    ~ (p | 2*A) ->
    exists u : Z,
      (p | F28_root_denominator A*u-1).
Proof.
  intros p A Hp Hnotdiv.
  unfold F28_root_denominator.
  apply F28_prime_inverse.
  - exact Hp.
  - exact Hnotdiv.
Qed.

(* ======================================== *)
(* FINAL CHECKS                             *)
(* ======================================== *)

Check F28_bezout_to_inverse.
Check F28_coprime_inverse.
Check F28_prime_inverse.
Check F28_denominator_inverse.

Print Assumptions F28_denominator_inverse.
