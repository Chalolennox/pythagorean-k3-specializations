(* code/coq/F28_discriminant_singular_root.v

   The owner's twenty-eighth Coq file (22 November 2026), the integrated version of the 22nd-27th files.  The text is the owner's, with ONE change: the five imports
   "From Stdlib Require Import ..." are written "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   WHAT IT PROVES: F28_discriminant_gives_singular_root: prime p >= 5, p | Delta = -4A^3 - 27B^2, p not dividing A ==> there is an integer r with p | r^3 + A r + B
   and p | 3 r^2 + A (the double root; r = -3 B u with 2 A u = 1 mod p).  Supporting lemmas (checked by hand): the two candidate identities (ring), the divisibility
   consequences, the modular inverse (Z.gcd_bezout), p >= 5 does not divide 2.
   Same statement as F28_double_root_exists in F28_large_prime_tangent.v (there with the hypothesis ~(p | 2A) instead of p >= 5, p not dividing A; and F28_discriminant_split_criterion
   there combines it with the certificate equivalence).  WHAT IT DOES NOT PROVE: anything about the character (-c6/p) = (3r/p) (see F28_large_prime_tangent.v) or the
   Tate/Silverman bridge.  Two routes to the same integer root now exist in the repository (rel_prime_bezout and Z.gcd_bezout); both are compiled in CI. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Zgcd_alt.
From Coq Require Import Ring.
From Coq Require Import Lia.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: DISCRIMINANT TO SINGULAR ROOT      *)
(* ======================================== *)

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

Definition F28_candidate_root (B u : Z) : Z :=
  F28_root_numerator B*u.

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

Lemma F28_divide_difference :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x-y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [k Hk].
  destruct Hy as [l Hl].
  exists (k-l).
  rewrite Hk, Hl.
  ring.
Qed.

Lemma F28_prime_product_split :
  forall p x y : Z,
    prime p ->
    (p | x*y) ->
    (p | x) \/ (p | y).
Proof.
  intros p x y Hp Hxy.
  eapply prime_mult; eauto.
Qed.

Lemma F28_nonzero_product :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    ~ (p | x*y).
Proof.
  intros p x y Hp Hx Hy Hxy.
  destruct
    (F28_prime_product_split p x y Hp Hxy)
    as [Hpx | Hpy].
  - exact (Hx Hpx).
  - exact (Hy Hpy).
Qed.

(* ======================================== *)
(* LARGE PRIMES DO NOT DIVIDE TWO           *)
(* ======================================== *)

Lemma F28_large_prime_not_divide_two :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 2).
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

Lemma F28_denominator_nonzero :
  forall p A : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    ~ (p | F28_root_denominator A).
Proof.
  intros p A Hp Hlarge HnotA.
  unfold F28_root_denominator.
  apply (F28_nonzero_product p 2 A).
  - exact Hp.
  - apply (F28_large_prime_not_divide_two p).
    + exact Hp.
    + exact Hlarge.
  - exact HnotA.
Qed.

(* ======================================== *)
(* MODULAR INVERSE VIA BEZOUT               *)
(* ======================================== *)

Lemma F28_bezout_to_inverse :
  forall p s k u : Z,
    p*k + s*u = 1 ->
    (p | s*u-1).
Proof.
  intros p s k u H.
  exists (-k).
  rewrite <- H.
  ring.
Qed.

Lemma F28_coprime_inverse :
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

Lemma F28_prime_inverse :
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
(* EXACT DISCRIMINANT IDENTITIES            *)
(* ======================================== *)

Lemma F28_candidate_derivative_identity :
  forall A B u : Z,
    F28_derivative A (F28_candidate_root B u) =
    -u^2*F28_discriminant A B
    - A*(F28_root_denominator A*u-1)*
        (F28_root_denominator A*u+1).
Proof.
  intros A B u.
  unfold F28_candidate_root,
    F28_derivative,
    F28_root_numerator,
    F28_root_denominator,
    F28_discriminant.
  ring.
Qed.

Lemma F28_candidate_cubic_identity :
  forall A B u : Z,
    F28_cubic A B (F28_candidate_root B u) =
    B*u^3*F28_discriminant A B
    -(F28_root_denominator A*u-1)*
     (A*(F28_root_numerator B)*u*
        (F28_root_denominator A*u+1)
      + B*((F28_root_denominator A*u)^2
           + F28_root_denominator A*u+1)).
Proof.
  intros A B u.
  unfold F28_candidate_root,
    F28_cubic,
    F28_root_numerator,
    F28_root_denominator,
    F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* CANDIDATE ROOT SATISFIES BOTH EQUATIONS  *)
(* ======================================== *)

Lemma F28_candidate_derivative_divisible :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | F28_root_denominator A*u-1) ->
    (p | F28_derivative A
       (F28_candidate_root B u)).
Proof.
  intros p A B u HD Hinv.
  rewrite F28_candidate_derivative_identity.

  apply F28_divide_difference.
  - replace (-u^2*F28_discriminant A B)
      with (F28_discriminant A B*(-u^2))
      by ring.
    apply F28_divide_product.
    exact HD.
  - replace
      (A*(F28_root_denominator A*u-1)*
         (F28_root_denominator A*u+1))
      with
      ((F28_root_denominator A*u-1)*
         (A*(F28_root_denominator A*u+1)))
      by ring.
    apply F28_divide_product.
    exact Hinv.
Qed.

Lemma F28_candidate_cubic_divisible :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | F28_root_denominator A*u-1) ->
    (p | F28_cubic A B
       (F28_candidate_root B u)).
Proof.
  intros p A B u HD Hinv.
  rewrite F28_candidate_cubic_identity.

  apply F28_divide_difference.
  - replace (B*u^3*F28_discriminant A B)
      with (F28_discriminant A B*(B*u^3))
      by ring.
    apply F28_divide_product.
    exact HD.
  - apply F28_divide_product.
    exact Hinv.
Qed.

(* ======================================== *)
(* MAIN THEOREM                             *)
(* ======================================== *)

Theorem F28_discriminant_gives_singular_root :
  forall p A B : Z,
    prime p ->
    5 <= p ->
    (p | F28_discriminant A B) ->
    ~ (p | A) ->
    exists r : Z,
      (p | F28_cubic A B r) /\
      (p | F28_derivative A r).
Proof.
  intros p A B Hp Hlarge HD HnotA.

  assert (Hden :
    ~ (p | F28_root_denominator A)).
  {
    apply (F28_denominator_nonzero p A).
    - exact Hp.
    - exact Hlarge.
    - exact HnotA.
  }

  destruct
    (F28_prime_inverse p
       (F28_root_denominator A)
       Hp Hden)
    as [u Hinv].

  exists (F28_candidate_root B u).

  split.
  - apply F28_candidate_cubic_divisible.
    + exact HD.
    + exact Hinv.
  - apply F28_candidate_derivative_divisible.
    + exact HD.
    + exact Hinv.
Qed.

(* ======================================== *)
(* FINAL VERIFICATION                       *)
(* ======================================== *)

Check F28_discriminant_gives_singular_root.

Print Assumptions
  F28_discriminant_gives_singular_root.
