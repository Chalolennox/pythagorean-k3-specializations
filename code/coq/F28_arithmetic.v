(* code/coq/F28_arithmetic.v

   The owner's consolidated F.28 file (sixth version, 22 November 2026): Parts I-IX unchanged except for this header; the part
   after the line "ADDED IN REVIEW" is added.  It regroups the earlier files (identities, divisibility helpers, the conditional
   reduction F28_nondivisibility_reduction) and adds:
     F28_primitive_coprimality           : 5 <= p, gcd a b = 1  =>  ~ (p | a /\ p | b)         (first assumption of the reduction)
     F28_pythagorean_square_divisibility : a^2 + b^2 = c^2, p | a, p | c  =>  p | b^2           (any integer p)
     F28_prime_square_cancel             : p prime, p | x^2  =>  p | x
     F28_pythagorean_prime_divisibility  : p prime, a^2 + b^2 = c^2, p | a, p | c  =>  p | b     (last assumption of the reduction)
   WHAT IS STILL OPEN HERE: the two cancellation assumptions of the reduction (4a^3 and 27b^2c) need p prime and p >= 5 (p does not
   divide 27).  The added part supplies them and the unconditional corollary.
   NOT FORMALIZED: the parametrization of (a,b,c) by a rational t, reduction types, local root numbers.  Compiled in CI. *)

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
    a^3 * (-c6_num b)
    =
    216^2*b^3*c
    - 1728*b*F a b c.
Proof.
  intros a b c.
  unfold F, c6_num.
  ring.
Qed.

Theorem F28_discriminant_identity :
  forall a b c : Z,
    -16*(4*(4*a)^3
         + 27*(-8*b)^2*c)
    =
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
(* PART III: DIVISIBILITY IMPLICATIONS      *)
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
(* PART VI: PYTHAGOREAN SQUARE DIVISIBILITY *)
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
(* NEW                                      *)
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

(* ======================================== *)
(* PART VIII: PYTHAGOREAN PRIME DIVISIBILITY*)
(* NEW                                      *)
(* ======================================== *)

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
(* PART IX: VERIFICATION                    *)
(* ======================================== *)

Check F28_character_identity.
Check F28_discriminant_identity.
Check F28_nondivisibility_reduction.
Check F28_primitive_coprimality.
Check F28_pythagorean_square_divisibility.

Check F28_prime_square_cancel.
Check F28_pythagorean_prime_divisibility.

Print Assumptions F28_prime_square_cancel.
Print Assumptions
  F28_pythagorean_prime_divisibility.

(* ======================================== *)
(* END                                      *)
(* ======================================== *)

(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026): p >= 5 cancellation and the unconditional statement *)
(* ======================================== *)

Lemma F28_prime_not_div_small :
  forall p n : Z, prime p -> 0 < n -> n < p -> ~ (p | n).
Proof.
  intros p n Hp Hn Hlt H.
  pose proof (Z.divide_pos_le p n Hn H) as H1.
  lia.
Qed.

Lemma F28_prime_div_cube :
  forall p a : Z, prime p -> (p | a^3) -> (p | a).
Proof.
  intros p a Hp H.
  replace (a^3) with (a*(a*a)) in H by ring.
  destruct (prime_mult p Hp a (a*a) H) as [H1 | H1].
  - exact H1.
  - destruct (prime_mult p Hp a a H1) as [H2 | H2]; exact H2.
Qed.

Lemma F28_ge5_div_4a3 :
  forall p a : Z, prime p -> 5 <= p -> (p | 4*a^3) -> (p | a).
Proof.
  intros p a Hp Hge H.
  destruct (prime_mult p Hp 4 (a^3) H) as [H1 | H1].
  - exfalso.
    refine (F28_prime_not_div_small p 4 Hp _ _ H1); lia.
  - exact (F28_prime_div_cube p a Hp H1).
Qed.

Lemma F28_ge5_not_div_27 :
  forall p : Z, prime p -> 5 <= p -> ~ (p | 27).
Proof.
  intros p Hp Hge H.
  replace 27 with (3*(3*3)) in H by reflexivity.
  destruct (prime_mult p Hp 3 (3*3) H) as [H1 | H1].
  - refine (F28_prime_not_div_small p 3 Hp _ _ H1); lia.
  - destruct (prime_mult p Hp 3 3 H1) as [H2 | H2];
      refine (F28_prime_not_div_small p 3 Hp _ _ H2); lia.
Qed.

Theorem F28_reduction_hypotheses_hold :
  forall p a b c : Z,
    prime p -> 5 <= p ->
    a^2 + b^2 = c^2 ->
    Z.gcd a b = 1 ->
    (~ ((p | a) /\ (p | b))) /\
    ((p | 4*a^3) -> (p | a)) /\
    ((p | 27*b^2*c) -> (p | b) \/ (p | c)) /\
    ((p | a) -> (p | c) -> (p | b)).
Proof.
  intros p a b c Hp Hge Hpy Hg.
  repeat split.
  - exact (F28_primitive_coprimality p a b Hge Hg).
  - intro H.
    exact (F28_ge5_div_4a3 p a Hp Hge H).
  - intro H.
    destruct (prime_mult p Hp (27*b^2) c H) as [H1 | H1].
    + destruct (prime_mult p Hp 27 (b^2) H1) as [H2 | H2].
      * exfalso.
        exact (F28_ge5_not_div_27 p Hp Hge H2).
      * left.
        exact (F28_prime_square_cancel p b Hp H2).
    + right.
      exact H1.
  - intros Ha Hc.
    exact (F28_pythagorean_prime_divisibility p a b c Hp Hpy Ha Hc).
Qed.

Theorem F28_nondivisibility_prime :
  forall p a b c : Z,
    prime p -> 5 <= p ->
    a^2 + b^2 = c^2 ->
    Z.gcd a b = 1 ->
    (p | F a b c) ->
    ~ (p | a) /\ ~ (p | b) /\ ~ (p | c).
Proof.
  intros p a b c Hp Hge Hpy Hg HF.
  destruct (F28_reduction_hypotheses_hold p a b c Hp Hge Hpy Hg)
    as [H1 [H2 [H3 H4]]].
  exact (F28_nondivisibility_reduction p a b c HF H1 H2 H3 H4).
Qed.

Print Assumptions F28_reduction_hypotheses_hold.
Print Assumptions F28_nondivisibility_prime.
