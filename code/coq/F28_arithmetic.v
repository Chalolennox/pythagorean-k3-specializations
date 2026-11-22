(* code/coq/F28_arithmetic.v

   The owner's consolidated F.28 file (seventh version, 22 November 2026): Parts I-XIV unchanged except for this header; the short
   part after the line "ADDED IN REVIEW" is added.  The file proves, for a prime p >= 5, a^2 + b^2 = c^2, gcd(a,b) = 1 and p | F(a,b,c):
     F28_main_arithmetic        : p divides none of a, b, c;
     F28_c4_nondivisibility     : p does not divide c4_num a = -192 a   (the c4 of the model WITHOUT the powers of c).
   WHAT IS ADDED: F28_c4_integral_nondivisibility, the same for -192 a c^3, which is the c4 of the integral model
   Y^2 = X^3 + 4 a c^3 X - 8 b c^5 (see F28_c4_integral_model in F28_identities.v).
   NOT FORMALIZED: the parametrization of (a,b,c) by a rational t, minimality of the model, the conclusion "multiplicative
   reduction" itself, local root numbers.  Compiled in CI. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28 - ARITHMETIC FORMALIZATION          *)
(* ======================================== *)

Definition F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition c4_num (a : Z) : Z :=
  -192*a.

Definition c6_num (b : Z) : Z :=
  6912*b.

(* ======================================== *)
(* PART I: POLYNOMIAL IDENTITIES            *)
(* ======================================== *)

Theorem F28_character_identity :
  forall a b c : Z,
    a^3 * (-c6_num b) =
    216^2*b^3*c - 1728*b*F a b c.
Proof.
  intros a b c.
  unfold F, c6_num.
  ring.
Qed.

Theorem F28_discriminant_identity :
  forall a b c : Z,
    -16*(4*(4*a)^3 + 27*(-8*b)^2*c) =
    -1024*F a b c.
Proof.
  intros a b c.
  unfold F.
  ring.
Qed.

(* ======================================== *)
(* PART II: DIVISIBILITY HELPERS            *)
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
  destruct Hx as [u Hu].
  destruct Hy as [v Hv].
  exists (u-v).
  rewrite Hu, Hv.
  ring.
Qed.

(* ======================================== *)
(* PART III: BASIC DIVISIBILITY             *)
(* ======================================== *)

Theorem F28_if_p_divides_c :
  forall p a b c : Z,
    (p | F a b c) ->
    (p | c) ->
    (p | 4*a^3).
Proof.
  intros p a b c HF Hc.
  replace (4*a^3)
    with (F a b c - c*(27*b^2)).
  - apply F28_divide_difference.
    + exact HF.
    + apply F28_divide_product.
      exact Hc.
  - unfold F.
    ring.
Qed.

Theorem F28_if_p_divides_b :
  forall p a b c : Z,
    (p | F a b c) ->
    (p | b) ->
    (p | 4*a^3).
Proof.
  intros p a b c HF Hb.
  replace (4*a^3)
    with (F a b c - b*(27*b*c)).
  - apply F28_divide_difference.
    + exact HF.
    + apply F28_divide_product.
      exact Hb.
  - unfold F.
    ring.
Qed.

Theorem F28_if_p_divides_a :
  forall p a b c : Z,
    (p | F a b c) ->
    (p | a) ->
    (p | 27*b^2*c).
Proof.
  intros p a b c HF Ha.
  replace (27*b^2*c)
    with (F a b c - a*(4*a^2)).
  - apply F28_divide_difference.
    + exact HF.
    + apply F28_divide_product.
      exact Ha.
  - unfold F.
    ring.
Qed.

(* ======================================== *)
(* PART IV: NONDIVISIBILITY REDUCTION       *)
(* ======================================== *)

Theorem F28_nondivisibility_reduction :
  forall p a b c : Z,
    (p | F a b c) ->
    (~ ((p | a) /\ (p | b))) ->
    ((p | 4*a^3) -> (p | a)) ->
    ((p | 27*b^2*c) ->
       (p | b) \/ (p | c)) ->
    ((p | a) -> (p | c) -> (p | b)) ->
    ~ (p | a) /\
    ~ (p | b) /\
    ~ (p | c).
Proof.
  intros p a b c HF Hcop Hcancel4
         Hcancel27 Hpyth.

  assert (Hna : ~ (p | a)).
  {
    intro Ha.
    pose proof
      (F28_if_p_divides_a p a b c HF Ha)
      as Hbc.
    apply Hcancel27 in Hbc.
    destruct Hbc as [Hb | Hc].
    - apply Hcop.
      split; assumption.
    - apply Hcop.
      split.
      + exact Ha.
      + apply (Hpyth Ha Hc).
  }

  assert (Hnb : ~ (p | b)).
  {
    intro Hb.
    pose proof
      (F28_if_p_divides_b p a b c HF Hb)
      as Ha4.
    apply Hcancel4 in Ha4.
    apply Hcop.
    split; assumption.
  }

  assert (Hnc : ~ (p | c)).
  {
    intro Hc.
    pose proof
      (F28_if_p_divides_c p a b c HF Hc)
      as Ha4.
    apply Hcancel4 in Ha4.
    exact (Hna Ha4).
  }

  repeat split; assumption.
Qed.

(* ======================================== *)
(* PART V: PRIMITIVE COPRIMALITY            *)
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

(* ======================================== *)
(* PART VI: PYTHAGOREAN DIVISIBILITY        *)
(* ======================================== *)

Theorem F28_pythagorean_square_divisibility :
  forall p a b c : Z,
    a^2 + b^2 = c^2 ->
    (p | a) ->
    (p | c) ->
    (p | b^2).
Proof.
  intros p a b c Hpyth Ha Hc.

  assert (Ha2 : (p | a^2)).
  {
    replace (a^2) with (a*a) by ring.
    apply F28_divide_product.
    exact Ha.
  }

  assert (Hc2 : (p | c^2)).
  {
    replace (c^2) with (c*c) by ring.
    apply F28_divide_product.
    exact Hc.
  }

  replace (b^2) with (c^2 - a^2).
  - apply F28_divide_difference.
    + exact Hc2.
    + exact Ha2.
  - rewrite <- Hpyth.
    ring.
Qed.

(* ======================================== *)
(* PART VII: PRIME-SQUARE CANCELLATION      *)
(* ======================================== *)

Theorem F28_prime_square_cancel :
  forall p x : Z,
    prime p ->
    (p | x^2) ->
    (p | x).
Proof.
  intros p x Hp Hsq.

  replace (x^2) with (x*x) in Hsq
    by ring.

  assert (Hsplit : (p | x) \/ (p | x)).
  {
    eapply prime_mult; eauto.
  }

  destruct Hsplit as [Hx | Hx];
    exact Hx.
Qed.

Theorem F28_pythagorean_prime_divisibility :
  forall p a b c : Z,
    prime p ->
    a^2 + b^2 = c^2 ->
    (p | a) ->
    (p | c) ->
    (p | b).
Proof.
  intros p a b c Hp Hpyth Ha Hc.

  apply (F28_prime_square_cancel p b).
  - exact Hp.
  - apply (F28_pythagorean_square_divisibility
             p a b c).
    + exact Hpyth.
    + exact Ha.
    + exact Hc.
Qed.

(* ======================================== *)
(* PART VIII: SMALL FACTOR EXCLUSION        *)
(* ======================================== *)

Lemma F28_no_small_divisor :
  forall p n : Z,
    5 <= p ->
    0 < n ->
    n < 5 ->
    ~ (p | n).
Proof.
  intros p n Hp Hnpos Hsmall Hdiv.
  destruct Hdiv as [k Hk].

  assert (Hcases :
    k <= -1 \/ k = 0 \/ k >= 1) by lia.

  destruct Hcases as [Hneg | [Hzero | Hpos]].
  - nia.
  - subst k.
    nia.
  - nia.
Qed.

Lemma F28_prime_not_divide_2 :
  forall p : Z,
    5 <= p ->
    ~ (p | 2).
Proof.
  intros p Hp.
  apply (F28_no_small_divisor p 2);
    lia.
Qed.

Lemma F28_prime_not_divide_3 :
  forall p : Z,
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hp.
  apply (F28_no_small_divisor p 3);
    lia.
Qed.

(* ======================================== *)
(* PART IX: PRIME FACTOR CANCELLATION       *)
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

Lemma F28_prime_not_divide_4 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 4).
Proof.
  intros p Hp Hlarge H4.

  replace 4 with (2*2) in H4 by ring.

  pose proof
    (F28_prime_product_split p 2 2 Hp H4)
    as Hsplit.

  destruct Hsplit as [H2 | H2].
  - exact (F28_prime_not_divide_2 p Hlarge H2).
  - exact (F28_prime_not_divide_2 p Hlarge H2).
Qed.

Lemma F28_prime_not_divide_27 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 27).
Proof.
  intros p Hp Hlarge H27.

  replace 27 with (3*(3*3)) in H27
    by ring.

  pose proof
    (F28_prime_product_split
       p 3 (3*3) Hp H27)
    as Hsplit.

  destruct Hsplit as [H3 | H9].
  - exact (F28_prime_not_divide_3 p Hlarge H3).
  - pose proof
      (F28_prime_product_split p 3 3 Hp H9)
      as Hsplit2.
    destruct Hsplit2 as [H3 | H3].
    + exact (F28_prime_not_divide_3 p Hlarge H3).
    + exact (F28_prime_not_divide_3 p Hlarge H3).
Qed.

(* ======================================== *)
(* PART X: CANCELLATION OF 4*a^3            *)
(* ======================================== *)

Theorem F28_cancel_4a3 :
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
    exact
      (F28_prime_not_divide_4
         p Hp Hlarge H4).

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

(* ======================================== *)
(* PART XI: CANCELLATION OF 27*b^2*c        *)
(* ======================================== *)

Theorem F28_cancel_27b2c :
  forall p b c : Z,
    prime p ->
    5 <= p ->
    (p | 27*b^2*c) ->
    (p | b) \/ (p | c).
Proof.
  intros p b c Hp Hlarge Hdiv.

  replace (27*b^2*c)
    with (27*(b^2*c)) in Hdiv
    by ring.

  pose proof
    (F28_prime_product_split
       p 27 (b^2*c) Hp Hdiv)
    as Hsplit.

  destruct Hsplit as [H27 | Hbc].
  - exfalso.
    exact
      (F28_prime_not_divide_27
         p Hp Hlarge H27).

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

(* ======================================== *)
(* PART XII: MAIN ARITHMETIC THEOREM        *)
(* ======================================== *)

Theorem F28_main_arithmetic :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    a^2 + b^2 = c^2 ->
    Z.gcd a b = 1 ->
    (p | F a b c) ->
    ~ (p | a) /\
    ~ (p | b) /\
    ~ (p | c).
Proof.
  intros p a b c
         Hp Hlarge Hpyth Hgcd HF.

  apply
    (F28_nondivisibility_reduction
       p a b c HF).

  - apply
      (F28_primitive_coprimality p a b).
    + exact Hlarge.
    + exact Hgcd.

  - apply (F28_cancel_4a3 p a).
    + exact Hp.
    + exact Hlarge.

  - apply (F28_cancel_27b2c p b c).
    + exact Hp.
    + exact Hlarge.

  - intros Ha Hc.
    apply
      (F28_pythagorean_prime_divisibility
         p a b c).
    + exact Hp.
    + exact Hpyth.
    + exact Ha.
    + exact Hc.
Qed.

(* ======================================== *)
(* PART XIII: c4 NONDIVISIBILITY            *)
(* CORRECTED - NO POWER INDUCTION           *)
(* ======================================== *)

Lemma F28_prime_not_divide_neg3 :
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

  exact
    (F28_prime_not_divide_3
       p Hlarge H3).
Qed.

Lemma F28_prime_not_divide_neg192 :
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
      (F28_prime_not_divide_neg3
         p Hlarge Hneg3).

  - pose proof
      (F28_prime_product_split
         p 4 (4*4) Hp H64)
      as Hsplit2.

    destruct Hsplit2 as [H4 | H16].

    + exact
        (F28_prime_not_divide_4
           p Hp Hlarge H4).

    + pose proof
        (F28_prime_product_split
           p 4 4 Hp H16)
        as Hsplit3.

      destruct Hsplit3 as [H4 | H4].
      * exact
          (F28_prime_not_divide_4
             p Hp Hlarge H4).
      * exact
          (F28_prime_not_divide_4
             p Hp Hlarge H4).
Qed.

Theorem F28_c4_nondivisibility :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    a^2 + b^2 = c^2 ->
    Z.gcd a b = 1 ->
    (p | F a b c) ->
    ~ (p | c4_num a).
Proof.
  intros p a b c
         Hp Hlarge Hpyth Hgcd HF Hc4.

  pose proof
    (F28_main_arithmetic
       p a b c Hp Hlarge Hpyth Hgcd HF)
    as Hmain.

  destruct Hmain as [Hna [Hnb Hnc]].

  unfold c4_num in Hc4.

  replace (-192*a) with ((-192)*a)
    in Hc4 by ring.

  pose proof
    (F28_prime_product_split
       p (-192) a Hp Hc4)
    as Hsplit.

  destruct Hsplit as [H192 | Ha].

  - exact
      (F28_prime_not_divide_neg192
         p Hp Hlarge H192).

  - exact (Hna Ha).
Qed.

(* ======================================== *)
(* PART XIV: FINAL VERIFICATION             *)
(* ======================================== *)

Check F28_character_identity.
Check F28_discriminant_identity.

Check F28_primitive_coprimality.
Check F28_pythagorean_prime_divisibility.

Check F28_cancel_4a3.
Check F28_cancel_27b2c.

Check F28_main_arithmetic.
Check F28_prime_not_divide_neg192.
Check F28_c4_nondivisibility.

Print Assumptions F28_main_arithmetic.
Print Assumptions F28_c4_nondivisibility.

(* ======================================== *)
(* END                                      *)
(* ======================================== *)

(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026): c4 of the integral model, with the powers of c *)
(* ======================================== *)

Theorem F28_c4_integral_nondivisibility :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    a^2 + b^2 = c^2 ->
    Z.gcd a b = 1 ->
    (p | F a b c) ->
    ~ (p | -192*a*c^3).
Proof.
  intros p a b c Hp Hlarge Hpyth Hgcd HF Hdiv.
  destruct (F28_main_arithmetic p a b c Hp Hlarge Hpyth Hgcd HF)
    as [Hna [Hnb Hnc]].
  destruct (F28_prime_product_split p (-192*a) (c^3) Hp Hdiv)
    as [H1 | H2].
  - exact (F28_c4_nondivisibility p a b c Hp Hlarge Hpyth Hgcd HF H1).
  - apply Hnc.
    replace (c^3) with (c*(c*c)) in H2 by ring.
    destruct (F28_prime_product_split p c (c*c) Hp H2) as [H3 | H3].
    + exact H3.
    + destruct (F28_prime_product_split p c c Hp H3) as [H4 | H4];
        exact H4.
Qed.

Print Assumptions F28_c4_integral_nondivisibility.
