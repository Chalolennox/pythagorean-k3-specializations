(* code/coq/F28_reduction.v

   Nondivisibility REDUCTION for F.28 (the owner's third file, parts before the line "ADDED IN REVIEW" unchanged except for this header).
   WHAT THE OWNER'S THEOREM PROVES: F28_nondivisibility_reduction is a conditional statement.  From p | F and four ASSUMED facts
     (no common divisor of a and b; 4a^3 cancellation; 27b^2c cancellation; "p | a and p | c imply p | b")
   it derives that p divides none of a, b, c.  The four assumptions are exactly where primality, p >= 5, a^2 + b^2 = c^2 and
   gcd(a,b) = 1 enter; the reduction does not prove them, so by itself it does not establish "p does not divide abc".
   WHAT IS ADDED: F28_reduction_hypotheses_hold shows that the four assumptions HOLD for every prime p >= 5 with a^2 + b^2 = c^2 and
   gcd(a,b) = 1 (so the reduction is not vacuous), and F28_nondivisibility_prime combines both into the unconditional statement.
   (The helper lemmas are repeated from F28_divisibility.v, which is a separate compilation unit.)
   NOT FORMALIZED: the parametrization of (a,b,c) by a rational t, reduction types, local root numbers.  Compiled in CI. *)

From Coq Require Import ZArith.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28 - NEXT ARITHMETIC MILESTONE         *)
(* ======================================== *)

Definition F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition c4_num (a : Z) : Z :=
  -192*a.

Definition c6_num (b : Z) : Z :=
  6912*b.

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
(* NONDIVISIBILITY REDUCTION                *)
(* ======================================== *)

Theorem F28_nondivisibility_reduction :
  forall p a b c : Z,
    (p | F a b c) ->

    (* Primitive Pythagorean condition,
       expressed as no common p-divisor. *)
    (~ ((p | a) /\ (p | b))) ->

    (* Prime cancellation for 4*a^3. *)
    ((p | 4*a^3) -> (p | a)) ->

    (* Prime cancellation for 27*b^2*c. *)
    ((p | 27*b^2*c) ->
       (p | b) \/ (p | c)) ->

    (* Pythagorean consequence:
       p divides a and c implies p divides b. *)
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
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_character_identity.
Check F28_discriminant_identity.
Check F28_nondivisibility_reduction.

Print Assumptions F28_nondivisibility_reduction.

(* ======================================== *)
(* END                                      *)
(* ======================================== *)


(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026): discharging the assumptions of the reduction *)
(* ======================================== *)

From Coq Require Import Znumtheory.
From Coq Require Import Lia.

Lemma F28_prime_not_div_small :
  forall p n : Z, prime p -> 0 < n -> n < p -> ~ (p | n).
Proof.
  intros p n Hp Hn Hlt H.
  pose proof (Z.divide_pos_le p n Hn H) as H1.
  lia.
Qed.

Lemma F28_prime_div_sq :
  forall p a : Z, prime p -> (p | a^2) -> (p | a).
Proof.
  intros p a Hp H.
  replace (a^2) with (a*a) in H by ring.
  destruct (prime_mult p Hp a a H) as [H1 | H1]; exact H1.
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

Lemma F28_coprime_contradiction :
  forall p a b : Z, 5 <= p -> Z.gcd a b = 1 -> (p | a) -> (p | b) -> False.
Proof.
  intros p a b Hge Hg Ha Hb.
  pose proof (Z.gcd_greatest a b p Ha Hb) as H.
  rewrite Hg in H.
  pose proof (Z.divide_pos_le p 1 ltac:(lia) H) as H1.
  lia.
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
  - intros [Ha Hb].
    exact (F28_coprime_contradiction p a b Hge Hg Ha Hb).
  - intro H.
    exact (F28_ge5_div_4a3 p a Hp Hge H).
  - intro H.
    destruct (prime_mult p Hp (27*b^2) c H) as [H1 | H1].
    + destruct (prime_mult p Hp 27 (b^2) H1) as [H2 | H2].
      * exfalso.
        exact (F28_ge5_not_div_27 p Hp Hge H2).
      * left.
        exact (F28_prime_div_sq p b Hp H2).
    + right.
      exact H1.
  - intros Ha Hc.
    apply (F28_prime_div_sq p b Hp).
    replace (b^2) with (c^2 - a^2) by (rewrite <- Hpy; ring).
    apply F28_divide_difference.
    + replace (c^2) with (c*c) by ring.
      apply F28_divide_product.
      exact Hc.
    + replace (a^2) with (a*a) by ring.
      apply F28_divide_product.
      exact Ha.
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
