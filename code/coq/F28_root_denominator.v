(* code/coq/F28_root_denominator.v

   The owner's twenty-fifth Coq file (22 November 2026), unchanged except for this header.  Standalone.
   F28_large_prime_not_divide_two: prime p >= 5 does not divide 2; F28_root_denominator_nonzero: prime p >= 5, p not dividing A ==> p not dividing 2A
   (the denominator of the double root r = -3B/(2A)).  Same statements as parts of F28_large_prime_constants.v and the inline step of
   F28_discriminant_split_criterion; nothing new mathematically, but the hypothesis "2A is invertible mod p" is now a named theorem.
   The nia case split on the cofactor k of 2 = k p is sound: k >= 1 gives k p >= 5, k <= -1 gives k p <= -5, k = 0 gives 2 = 0. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* PRIME PRODUCT DIVISIBILITY               *)
(* ======================================== *)

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
(* EXCLUDE DIVISIBILITY BY 2                *)
(* ======================================== *)

Theorem F28_large_prime_not_divide_two :
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

(* ======================================== *)
(* NONDIVISIBILITY OF 2A                    *)
(* ======================================== *)

Theorem F28_root_denominator_nonzero :
  forall p A : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    ~ (p | 2*A).
Proof.
  intros p A Hp Hlarge HnotA.

  apply (F28_nonzero_product p 2 A).
  - exact Hp.
  - apply (F28_large_prime_not_divide_two p).
    + exact Hp.
    + exact Hlarge.
  - exact HnotA.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_large_prime_not_divide_two.
Check F28_root_denominator_nonzero.

Print Assumptions F28_root_denominator_nonzero.
