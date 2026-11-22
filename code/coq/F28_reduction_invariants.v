(* code/coq/F28_reduction_invariants.v

   The owner's fourteenth Coq file (22 November 2026), unchanged except for this header.  A standalone compilation unit.
   WHAT IT PROVES: for the INTEGRAL model Y^2 = X^3 + A X + B with A = 4 a c^3, B = -8 b c^5 (so the powers of c are included, which closes
   the gap flagged for c4_num in F28_arithmetic.v):
     F28_c4_identity   : c4 = -48 A = -192 a c^3;
     F28_delta_identity: Delta = -16 (4 A^3 + 27 B^2) = -1024 c^9 F(a,b,c);
     F28_delta_divisible: p | F implies p | Delta;
     F28_c4_nonzero    : p prime >= 5, p not dividing a and c, implies p does not divide c4;
     F28_reduction_invariant_conditions: the two together.
   WHAT IT DOES NOT PROVE: that these two conditions (p | Delta, p not dividing c4) give MULTIPLICATIVE reduction (Tate's algorithm / Silverman
   VII.1.1, minimality of the model at p) is not in Coq; the hypotheses "p does not divide a, c" are supplied by F28_main_arithmetic
   (F28_arithmetic.v), and F28_integral_model_conditions there combines everything for a primitive triple. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28 - REDUCTION INVARIANT CONDITIONS    *)
(* ======================================== *)

Definition F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_c4 (a c : Z) : Z :=
  -48*F28_A a c.

Definition F28_delta (a b c : Z) : Z :=
  -16*(4*(F28_A a c)^3
       +27*(F28_B b c)^2).

(* ======================================== *)
(* VERIFIED INVARIANT IDENTITIES            *)
(* ======================================== *)

Theorem F28_c4_identity :
  forall a c : Z,
    F28_c4 a c = -192*a*c^3.
Proof.
  intros a c.
  unfold F28_c4, F28_A.
  ring.
Qed.

Theorem F28_delta_identity :
  forall a b c : Z,
    F28_delta a b c =
      -1024*c^9*F a b c.
Proof.
  intros a b c.
  unfold F28_delta, F28_A, F28_B, F.
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

Lemma F28_prime_product_split :
  forall p x y : Z,
    prime p ->
    (p | x*y) ->
    (p | x) \/ (p | y).
Proof.
  intros p x y Hp Hxy.
  eapply prime_mult; eauto.
Qed.

(* ======================================== *)
(* VERIFIED DISCRIMINANT DIVISIBILITY       *)
(* ======================================== *)

Theorem F28_delta_divisible :
  forall p a b c : Z,
    (p | F a b c) ->
    (p | F28_delta a b c).
Proof.
  intros p a b c HF.

  rewrite F28_delta_identity.

  replace (-1024*c^9*F a b c)
    with (F a b c*(-1024*c^9))
    by ring.

  apply F28_divide_product.
  exact HF.
Qed.

(* ======================================== *)
(* SMALL PRIME EXCLUSIONS                   *)
(* ======================================== *)

Lemma F28_no_small_divisor :
  forall p n : Z,
    5 <= p ->
    0 < n ->
    n < 5 ->
    ~ (p | n).
Proof.
  intros p n Hp Hpos Hsmall Hdiv.
  destruct Hdiv as [k Hk].

  assert
    (Hcases : k <= -1 \/ k = 0 \/ k >= 1)
    by lia.

  destruct Hcases as [Hneg | [Hzero | Hpositive]].
  - nia.
  - subst k.
    nia.
  - nia.
Qed.

Lemma F28_not_divide_2 :
  forall p : Z,
    5 <= p ->
    ~ (p | 2).
Proof.
  intros p Hp.
  apply (F28_no_small_divisor p 2);
    lia.
Qed.

Lemma F28_not_divide_3 :
  forall p : Z,
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hp.
  apply (F28_no_small_divisor p 3);
    lia.
Qed.

Lemma F28_not_divide_4 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 4).
Proof.
  intros p Hp Hlarge H4.

  replace 4 with (2*2) in H4 by ring.

  pose proof
    (F28_prime_product_split
       p 2 2 Hp H4)
    as Hsplit.

  destruct Hsplit as [H2 | H2].
  - exact (F28_not_divide_2 p Hlarge H2).
  - exact (F28_not_divide_2 p Hlarge H2).
Qed.

Lemma F28_not_divide_neg3 :
  forall p : Z,
    5 <= p ->
    ~ (p | -3).
Proof.
  intros p Hlarge Hneg3.

  assert (H3 : (p | 3)).
  {
    replace 3 with ((-3)*(-1))
      by ring.
    apply F28_divide_product.
    exact Hneg3.
  }

  exact (F28_not_divide_3 p Hlarge H3).
Qed.

(* ======================================== *)
(* NONDIVISIBILITY OF -192                  *)
(* ======================================== *)

Lemma F28_not_divide_neg192 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | -192).
Proof.
  intros p Hp Hlarge H192.

  replace (-192)
    with ((-3)*(4*(4*4)))
    in H192 by ring.

  pose proof
    (F28_prime_product_split
       p (-3) (4*(4*4)) Hp H192)
    as Hsplit1.

  destruct Hsplit1 as [Hneg3 | H64].

  - exact
      (F28_not_divide_neg3
         p Hlarge Hneg3).

  - pose proof
      (F28_prime_product_split
         p 4 (4*4) Hp H64)
      as Hsplit2.

    destruct Hsplit2 as [H4 | H16].

    + exact
        (F28_not_divide_4
           p Hp Hlarge H4).

    + pose proof
        (F28_prime_product_split
           p 4 4 Hp H16)
        as Hsplit3.

      destruct Hsplit3 as [H4 | H4].

      * exact
          (F28_not_divide_4
             p Hp Hlarge H4).

      * exact
          (F28_not_divide_4
             p Hp Hlarge H4).
Qed.

(* ======================================== *)
(* NEW: c4 NONDIVISIBILITY                  *)
(* ======================================== *)

Theorem F28_c4_nonzero :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    ~ (p | F28_c4 a c).
Proof.
  intros p a c Hp Hlarge Hna Hnc Hc4.

  rewrite F28_c4_identity in Hc4.

  replace (-192*a*c^3)
    with ((-192)*(a*(c*(c*c))))
    in Hc4 by ring.

  pose proof
    (F28_prime_product_split
       p (-192) (a*(c*(c*c))) Hp Hc4)
    as Hsplit1.

  destruct Hsplit1 as [H192 | Hrest].

  - exact
      (F28_not_divide_neg192
         p Hp Hlarge H192).

  - pose proof
      (F28_prime_product_split
         p a (c*(c*c)) Hp Hrest)
      as Hsplit2.

    destruct Hsplit2 as [Ha | Hcube].

    + exact (Hna Ha).

    + pose proof
        (F28_prime_product_split
           p c (c*c) Hp Hcube)
        as Hsplit3.

      destruct Hsplit3 as [Hc | Hsquare].

      * exact (Hnc Hc).

      * pose proof
          (F28_prime_product_split
             p c c Hp Hsquare)
          as Hsplit4.

        destruct Hsplit4 as [Hc | Hc].
        -- exact (Hnc Hc).
        -- exact (Hnc Hc).
Qed.

(* ======================================== *)
(* NEW: COMBINED REDUCTION CONDITIONS       *)
(* ======================================== *)

Theorem F28_reduction_invariant_conditions :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    (p | F a b c) ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_delta a b c) /\
    ~ (p | F28_c4 a c).
Proof.
  intros p a b c Hp Hlarge HF Hna Hnc.

  split.

  - apply F28_delta_divisible.
    exact HF.

  - apply (F28_c4_nonzero p a c).
    + exact Hp.
    + exact Hlarge.
    + exact Hna.
    + exact Hnc.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_delta_identity.
Check F28_delta_divisible.
Check F28_not_divide_neg192.
Check F28_c4_nonzero.
Check F28_reduction_invariant_conditions.

Print Assumptions F28_delta_divisible.
Print Assumptions F28_c4_nonzero.
Print Assumptions
  F28_reduction_invariant_conditions.

(* ======================================== *)
(* END                                      *)
(* ======================================== *)
