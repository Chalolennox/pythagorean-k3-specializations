(* code/coq/F28_primitive_reduction.v

   The owner's fifteenth Coq file (22 November 2026), unchanged except for this header.  A standalone compilation unit that integrates the
   fourteenth file (F28_reduction_invariants.v) with the arithmetic of F28_arithmetic.v (it reproves F28_main_arithmetic inside).
   WHAT IT PROVES: F28_primitive_reduction_conditions: for a prime p >= 5, a^2 + b^2 = c^2, gcd(a,b) = 1 and p | F(a,b,c), the INTEGRAL model
   Y^2 = X^3 + 4 a c^3 X - 8 b c^5 has p | Delta (Delta = -1024 c^9 F) and p does not divide c4 (= -192 a c^3).
   It states the same thing as F28_integral_model_conditions of F28_arithmetic.v (added in review), with the definitions F28_c4 and F28_delta.
   WHAT IT DOES NOT PROVE: that p | Delta and p not dividing c4 imply multiplicative reduction and minimality at p (Silverman VII.1.1,
   Tate's algorithm) is not in Coq; neither are the split/non-split distinction (see the certificate files), "c is a square on the family",
   the Legendre symbol and the local root numbers. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28 - PRIMITIVE REDUCTION CRITERION     *)
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
(* ALGEBRAIC IDENTITIES                     *)
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

Lemma F28_divide_difference :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x-y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [u Hu].
  destruct Hy as [v Hv].
  exists (u-v).
  rewrite Hu, Hv.
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

Lemma F28_prime_square_cancel :
  forall p x : Z,
    prime p ->
    (p | x^2) ->
    (p | x).
Proof.
  intros p x Hp Hsq.
  replace (x^2) with (x*x)
    in Hsq by ring.
  pose proof
    (F28_prime_product_split
       p x x Hp Hsq) as Hsplit.
  destruct Hsplit as [Hx | Hx];
    exact Hx.
Qed.

(* ======================================== *)
(* CONSTANT EXCLUSIONS                      *)
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
  assert (Hcases :
    k <= -1 \/ k = 0 \/ k >= 1) by lia.
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
       p 2 2 Hp H4) as Hsplit.
  destruct Hsplit as [H2 | H2].
  - exact (F28_not_divide_2 p Hlarge H2).
  - exact (F28_not_divide_2 p Hlarge H2).
Qed.

Lemma F28_not_divide_9 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 9).
Proof.
  intros p Hp Hlarge H9.
  replace 9 with (3*3) in H9 by ring.
  pose proof
    (F28_prime_product_split
       p 3 3 Hp H9) as Hsplit.
  destruct Hsplit as [H3 | H3].
  - exact (F28_not_divide_3 p Hlarge H3).
  - exact (F28_not_divide_3 p Hlarge H3).
Qed.

Lemma F28_not_divide_27 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 27).
Proof.
  intros p Hp Hlarge H27.
  replace 27 with (3*9) in H27 by ring.
  pose proof
    (F28_prime_product_split
       p 3 9 Hp H27) as Hsplit.
  destruct Hsplit as [H3 | H9].
  - exact (F28_not_divide_3 p Hlarge H3).
  - exact (F28_not_divide_9 p Hp Hlarge H9).
Qed.

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

  - assert (H3 : (p | 3)).
    {
      replace 3 with ((-3)*(-1)) by ring.
      apply F28_divide_product.
      exact Hneg3.
    }
    exact (F28_not_divide_3 p Hlarge H3).

  - pose proof
      (F28_prime_product_split
         p 4 (4*4) Hp H64)
      as Hsplit2.

    destruct Hsplit2 as [H4 | H16].
    + exact
        (F28_not_divide_4 p Hp Hlarge H4).
    + pose proof
        (F28_prime_product_split
           p 4 4 Hp H16)
        as Hsplit3.
      destruct Hsplit3 as [H4 | H4].
      * exact
          (F28_not_divide_4 p Hp Hlarge H4).
      * exact
          (F28_not_divide_4 p Hp Hlarge H4).
Qed.

(* ======================================== *)
(* PRIMITIVE NONDIVISIBILITY                *)
(* ======================================== *)

Lemma F28_primitive_coprimality :
  forall p a b : Z,
    5 <= p ->
    Z.gcd a b = 1 ->
    ~ ((p | a) /\ (p | b)).
Proof.
  intros p a b Hp Hgcd [Ha Hb].
  assert (Hdiv : (p | Z.gcd a b)).
  {
    apply Z.gcd_greatest.
    - exact Ha.
    - exact Hb.
  }
  rewrite Hgcd in Hdiv.
  apply Z.divide_1_r in Hdiv.
  lia.
Qed.

Lemma F28_pythagorean_prime_divisibility :
  forall p a b c : Z,
    prime p ->
    a^2+b^2=c^2 ->
    (p | a) ->
    (p | c) ->
    (p | b).
Proof.
  intros p a b c Hp Hpyth Ha Hc.
  apply (F28_prime_square_cancel p b).
  - exact Hp.
  - replace (b^2) with (c^2-a^2).
    + apply F28_divide_difference.
      * replace (c^2) with (c*c) by ring.
        apply F28_divide_product.
        exact Hc.
      * replace (a^2) with (a*a) by ring.
        apply F28_divide_product.
        exact Ha.
    + rewrite <- Hpyth.
      ring.
Qed.

Lemma F28_cancel_4a3 :
  forall p a : Z,
    prime p ->
    5 <= p ->
    (p | 4*a^3) ->
    (p | a).
Proof.
  intros p a Hp Hlarge Hdiv.
  pose proof
    (F28_prime_product_split
       p 4 (a^3) Hp Hdiv)
    as Hsplit.
  destruct Hsplit as [H4 | Ha3].
  - exfalso.
    exact (F28_not_divide_4 p Hp Hlarge H4).
  - replace (a^3) with (a*(a*a))
      in Ha3 by ring.
    pose proof
      (F28_prime_product_split
         p a (a*a) Hp Ha3)
      as Hsplit2.
    destruct Hsplit2 as [Ha | Ha2].
    + exact Ha.
    + replace (a*a) with (a^2)
        in Ha2 by ring.
      apply (F28_prime_square_cancel p a).
      * exact Hp.
      * exact Ha2.
Qed.

Lemma F28_cancel_27b2c :
  forall p b c : Z,
    prime p ->
    5 <= p ->
    (p | 27*b^2*c) ->
    (p | b) \/ (p | c).
Proof.
  intros p b c Hp Hlarge Hdiv.
  replace (27*b^2*c)
    with (27*(b^2*c))
    in Hdiv by ring.
  pose proof
    (F28_prime_product_split
       p 27 (b^2*c) Hp Hdiv)
    as Hsplit.
  destruct Hsplit as [H27 | Hbc].
  - exfalso.
    exact (F28_not_divide_27 p Hp Hlarge H27).
  - pose proof
      (F28_prime_product_split
         p (b^2) c Hp Hbc)
      as Hsplit2.
    destruct Hsplit2 as [Hb2 | Hc].
    + left.
      apply (F28_prime_square_cancel p b).
      * exact Hp.
      * exact Hb2.
    + right.
      exact Hc.
Qed.

Theorem F28_main_arithmetic :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    a^2+b^2=c^2 ->
    Z.gcd a b=1 ->
    (p | F a b c) ->
    ~ (p | a) /\
    ~ (p | b) /\
    ~ (p | c).
Proof.
  intros p a b c
    Hp Hlarge Hpyth Hgcd HF.

  assert (Hcop :
    ~ ((p | a) /\ (p | b))).
  {
    apply (F28_primitive_coprimality p a b).
    - exact Hlarge.
    - exact Hgcd.
  }

  assert (Hna : ~ (p | a)).
  {
    intro Ha.
    assert (Hbc : (p | 27*b^2*c)).
    {
      replace (27*b^2*c)
        with (F a b c-a*(4*a^2)).
      - apply F28_divide_difference.
        + exact HF.
        + apply F28_divide_product.
          exact Ha.
      - unfold F.
        ring.
    }
    pose proof
      (F28_cancel_27b2c
         p b c Hp Hlarge Hbc)
      as Hsplit.
    destruct Hsplit as [Hb | Hc].
    - apply Hcop.
      split; assumption.
    - apply Hcop.
      split.
      + exact Ha.
      + apply
          (F28_pythagorean_prime_divisibility
             p a b c Hp Hpyth Ha Hc).
  }

  assert (Hnb : ~ (p | b)).
  {
    intro Hb.
    assert (Ha4 : (p | 4*a^3)).
    {
      replace (4*a^3)
        with (F a b c-b*(27*b*c)).
      - apply F28_divide_difference.
        + exact HF.
        + apply F28_divide_product.
          exact Hb.
      - unfold F.
        ring.
    }
    pose proof
      (F28_cancel_4a3
         p a Hp Hlarge Ha4)
      as Ha.
    apply Hcop.
    split; assumption.
  }

  assert (Hnc : ~ (p | c)).
  {
    intro Hc.
    assert (Ha4 : (p | 4*a^3)).
    {
      replace (4*a^3)
        with (F a b c-c*(27*b^2)).
      - apply F28_divide_difference.
        + exact HF.
        + apply F28_divide_product.
          exact Hc.
      - unfold F.
        ring.
    }
    apply Hna.
    apply (F28_cancel_4a3 p a).
    - exact Hp.
    - exact Hlarge.
    - exact Ha4.
  }

  repeat split; assumption.
Qed.

(* ======================================== *)
(* c4 NONDIVISIBILITY                       *)
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
(* DISCRIMINANT DIVISIBILITY                *)
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
(* FINAL INTEGRATED THEOREM                 *)
(* ======================================== *)

Theorem F28_primitive_reduction_conditions :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    a^2+b^2=c^2 ->
    Z.gcd a b=1 ->
    (p | F a b c) ->
    (p | F28_delta a b c) /\
    ~ (p | F28_c4 a c).
Proof.
  intros p a b c
    Hp Hlarge Hpyth Hgcd HF.

  pose proof
    (F28_main_arithmetic
       p a b c Hp Hlarge Hpyth Hgcd HF)
    as Hmain.

  destruct Hmain as [Hna [Hnb Hnc]].

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

Check F28_main_arithmetic.
Check F28_delta_identity.
Check F28_c4_nonzero.
Check F28_primitive_reduction_conditions.

Print Assumptions F28_main_arithmetic.
Print Assumptions F28_primitive_reduction_conditions.
