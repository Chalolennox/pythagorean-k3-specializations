(* code/coq/F28_divisibility.v

   Divisibility steps of F.28 (the setup of section 3: a prime p >= 5 dividing F does not divide abc).
   Parts I-IV are the owner's second file, unchanged except for this header (Part I repeats the two identities of
   F28_identities.v; this file is a separate compilation unit).  Part V was added in review (22 November 2026).
   WHAT PARTS I-IV PROVE: for ANY integer p, if p | F and p divides one of a, b, c then p | 4a^3 (resp. p | 27b^2c).
   These are the first steps of the paper's three cases; they do not yet say that p does not divide abc.
   WHAT PART V ADDS: the statement of the paper (primality of p, p >= 5, a^2 + b^2 = c^2, gcd(a,b) = 1 as hypotheses):
   F28_prime_not_dividing_abc : p | F  ->  ~ p | a /\ ~ p | b /\ ~ p | c.
   NOT FORMALIZED: that a, b, c come from a rational t (the parametrization), the reduction types and local root numbers.
   Compiled in CI (.github/workflows/coq.yml). *)

From Coq Require Import ZArith.
From Coq Require Import Ring.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.

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
(* PART I: ALGEBRAIC IDENTITIES             *)
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
(* PART IV: VERIFICATION                    *)
(* ======================================== *)

Check F28_character_identity.
Check F28_discriminant_identity.
Check F28_divide_product.
Check F28_divide_difference.
Check F28_if_p_divides_c.
Check F28_if_p_divides_b.
Check F28_if_p_divides_a.

Print Assumptions F28_if_p_divides_c.
Print Assumptions F28_if_p_divides_b.
Print Assumptions F28_if_p_divides_a.

(* ======================================== *)
(* PART V (added in review): p >= 5 dividing F does not divide a, b or c *)
(* Hypotheses as in the paper (section 3, Setup): a^2 + b^2 = c^2, gcd(a,b) = 1 (so a, b, c pairwise coprime). *)
(* ======================================== *)

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

Theorem F28_prime_not_dividing_abc :
  forall p a b c : Z,
    prime p -> 5 <= p ->
    a^2 + b^2 = c^2 ->
    Z.gcd a b = 1 ->
    (p | F a b c) ->
    ~ (p | a) /\ ~ (p | b) /\ ~ (p | c).
Proof.
  intros p a b c Hp Hge Hpy Hg HF.
  assert (Hca : (p | a) -> (p | c) -> (p | b)).
  { intros Ha Hc.
    apply (F28_prime_div_sq p b Hp).
    replace (b^2) with (c^2 - a^2) by (rewrite <- Hpy; ring).
    apply F28_divide_difference.
    - replace (c^2) with (c*c) by ring.
      apply F28_divide_product.
      exact Hc.
    - replace (a^2) with (a*a) by ring.
      apply F28_divide_product.
      exact Ha. }
  repeat split.
  - intro Ha.
    pose proof (F28_if_p_divides_a p a b c HF Ha) as H27.
    destruct (prime_mult p Hp (27*b^2) c H27) as [H1 | H1].
    + destruct (prime_mult p Hp 27 (b^2) H1) as [H2 | H2].
      * exact (F28_ge5_not_div_27 p Hp Hge H2).
      * exact (F28_coprime_contradiction p a b Hge Hg Ha (F28_prime_div_sq p b Hp H2)).
    + exact (F28_coprime_contradiction p a b Hge Hg Ha (Hca Ha H1)).
  - intro Hb.
    pose proof (F28_if_p_divides_b p a b c HF Hb) as H4.
    exact (F28_coprime_contradiction p a b Hge Hg (F28_ge5_div_4a3 p a Hp Hge H4) Hb).
  - intro Hc.
    pose proof (F28_if_p_divides_c p a b c HF Hc) as H4.
    pose proof (F28_ge5_div_4a3 p a Hp Hge H4) as Ha.
    exact (F28_coprime_contradiction p a b Hge Hg Ha (Hca Ha Hc)).
Qed.

Print Assumptions F28_prime_not_dividing_abc.
