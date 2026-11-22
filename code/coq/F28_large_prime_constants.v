(* code/coq/F28_large_prime_constants.v

   The owner's twentieth Coq file (22 November 2026), unchanged except for this header.  Standalone.
   WHAT IT PROVES: a prime p >= 5 does not divide 2, 3, or 864 = 2^5 * 3^3 (the last by splitting the product 2*2*2*2*2*3*3*3 with an Ltac
   `repeat match` loop and excluding each factor); hence p not dividing r gives p not dividing 3r, and p not dividing B gives p not dividing 864 B.
   I read it: the sign analysis of k in 2 = k p and 3 = k p (nia) is correct, the factorization 2^5 * 3^3 = 864 is right, and the loop terminates
   (each split removes one factor; a leaf (p | 2) or (p | 3) no longer matches the product pattern).  The only part whose behaviour I cannot run
   is the Ltac loop; CI decides.
   WHY IT MATTERS: these are the constant exclusions behind F28_nodal_split_criterion in F28_tangent_character.v (nondivisibility of 3r and 864 B for
   a prime p >= 5), which proves them inline by a chain of F28_nonzero_product. *)
From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* PRIME DIVISIBILITY HELPERS               *)
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
(* EXCLUDING SMALL PRIME DIVISORS           *)
(* ======================================== *)

Theorem F28_large_prime_not_divide_two :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 2).
Proof.
  intros p Hp Hlarge Hdiv.
  destruct Hdiv as [k Hk].
  assert (Hpositive : 0 < p) by lia.
  assert (Hbound : 0 <= k \/ k < 0) by lia.
  destruct Hbound as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k. lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

Theorem F28_large_prime_not_divide_three :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hp Hlarge Hdiv.
  destruct Hdiv as [k Hk].
  assert (Hpositive : 0 < p) by lia.
  destruct (Z_le_gt_dec 0 k) as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k. lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

(* ======================================== *)
(* CONSTANT 864 = 2^5 * 3^3                 *)
(* ======================================== *)

Theorem F28_large_prime_not_divide_864 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 864).
Proof.
  intros p Hp Hlarge Hdiv.

  assert (Hnot2 : ~ (p | 2)).
  {
    apply (F28_large_prime_not_divide_two p).
    - exact Hp.
    - exact Hlarge.
  }

  assert (Hnot3 : ~ (p | 3)).
  {
    apply (F28_large_prime_not_divide_three p).
    - exact Hp.
    - exact Hlarge.
  }

  replace 864 with (2*2*2*2*2*3*3*3) in Hdiv
    by ring.

  repeat match type of Hdiv with
  | (p | ?x * ?y) =>
      let H := fresh "Hsplit" in
      pose proof
        (F28_prime_product_split p x y Hp Hdiv)
        as H;
      clear Hdiv;
      destruct H as [Hdiv | Hdiv]
  end.

  all: first [exact (Hnot2 Hdiv) |
              exact (Hnot3 Hdiv)].
Qed.

(* ======================================== *)
(* CONSEQUENCES FOR r AND B                 *)
(* ======================================== *)

Theorem F28_three_r_nonzero :
  forall p r : Z,
    prime p ->
    5 <= p ->
    ~ (p | r) ->
    ~ (p | 3*r).
Proof.
  intros p r Hp Hlarge Hr.
  apply (F28_nonzero_product p 3 r).
  - exact Hp.
  - apply (F28_large_prime_not_divide_three p).
    + exact Hp.
    + exact Hlarge.
  - exact Hr.
Qed.

Theorem F28_864_B_nonzero :
  forall p B : Z,
    prime p ->
    5 <= p ->
    ~ (p | B) ->
    ~ (p | 864*B).
Proof.
  intros p B Hp Hlarge HB.
  apply (F28_nonzero_product p 864 B).
  - exact Hp.
  - apply (F28_large_prime_not_divide_864 p).
    + exact Hp.
    + exact Hlarge.
  - exact HB.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_large_prime_not_divide_two.
Check F28_large_prime_not_divide_three.
Check F28_large_prime_not_divide_864.
Check F28_three_r_nonzero.
Check F28_864_B_nonzero.

Print Assumptions F28_large_prime_not_divide_864.
Print Assumptions F28_864_B_nonzero.
