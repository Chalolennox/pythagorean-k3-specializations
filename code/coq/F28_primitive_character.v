(* code/coq/F28_primitive_character.v

   The owner's thirteenth Coq file (22 November 2026): everything before the line "ADDED IN REVIEW" is the owner's text unchanged except for
   this header.  A standalone compilation unit that reproves F28_main_arithmetic directly (it does not use the reduction theorem) and combines
   it with the certificate algebra of F28_certificate.v / F28_character_comparison.v.
   WHAT IT PROVES: F28_primitive_character_comparison: for a prime p >= 5, a^2 + b^2 = c^2, gcd(a,b) = 1 and p | F(a,b,c),
        (a b is a square certificate mod p)  <->  (-6912 b c is a square certificate mod p),
   i.e. (ab/p) = +1 iff (-6912 b c / p) = +1, with the nondivisibility of a, b, c (F28_main_arithmetic) derived inside.  Note -6912 b = -c6_num b.
   WHAT IT DOES NOT PROVE: the right side is (-c6 . c / p), not the paper's (-c6/p); c a square mod p ("c is a square on the family", section 6)
   is not in Coq, no Legendre symbol, no Tate/Kodaira.  The added part proves the paper's form given a certificate for c
   (F28_primitive_split_criterion). *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28 - INTEGRATED ARITHMETIC THEOREM     *)
(* ======================================== *)

Definition F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_square_certificate
  (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2 - v^2).

(* ======================================== *)
(* DIVISIBILITY LEMMAS                      *)
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

Lemma F28_divide_sum :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x+y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [u Hu].
  destruct Hy as [v Hv].
  exists (u+v).
  rewrite Hu, Hv.
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

Lemma F28_nonzero_product :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    ~ (p | x*y).
Proof.
  intros p x y Hp Hx Hy Hxy.

  pose proof
    (F28_prime_product_split p x y Hp Hxy)
    as Hsplit.

  destruct Hsplit as [Hpx | Hpy].
  - exact (Hx Hpx).
  - exact (Hy Hpy).
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
    (F28_prime_product_split p 2 2 Hp H4)
    as Hsplit.

  destruct Hsplit as [H2 | H2].
  - exact (F28_not_divide_2 p Hlarge H2).
  - exact (F28_not_divide_2 p Hlarge H2).
Qed.

Lemma F28_not_divide_16 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 16).
Proof.
  intros p Hp Hlarge H16.

  replace 16 with (4*4) in H16 by ring.

  pose proof
    (F28_prime_product_split p 4 4 Hp H16)
    as Hsplit.

  destruct Hsplit as [H4 | H4].
  - exact
      (F28_not_divide_4 p Hp Hlarge H4).
  - exact
      (F28_not_divide_4 p Hp Hlarge H4).
Qed.

Lemma F28_not_divide_256 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 256).
Proof.
  intros p Hp Hlarge H256.

  replace 256 with (16*16)
    in H256 by ring.

  pose proof
    (F28_prime_product_split
       p 16 16 Hp H256)
    as Hsplit.

  destruct Hsplit as [H16 | H16].
  - exact
      (F28_not_divide_16 p Hp Hlarge H16).
  - exact
      (F28_not_divide_16 p Hp Hlarge H16).
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
    (F28_prime_product_split p 3 3 Hp H9)
    as Hsplit.

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
    (F28_prime_product_split p 3 9 Hp H27)
    as Hsplit.

  destruct Hsplit as [H3 | H9].
  - exact (F28_not_divide_3 p Hlarge H3).
  - exact
      (F28_not_divide_9 p Hp Hlarge H9).
Qed.

Theorem F28_not_divide_6912 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 6912).
Proof.
  intros p Hp Hlarge H6912.

  replace 6912 with (256*27)
    in H6912 by ring.

  pose proof
    (F28_prime_product_split
       p 256 27 Hp H6912)
    as Hsplit.

  destruct Hsplit as [H256 | H27].
  - exact
      (F28_not_divide_256
         p Hp Hlarge H256).
  - exact
      (F28_not_divide_27
         p Hp Hlarge H27).
Qed.

(* ======================================== *)
(* PRIMITIVE PYTHAGOREAN ARITHMETIC         *)
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
    (F28_prime_product_split p x x Hp Hsq)
    as Hsplit.

  destruct Hsplit as [Hx | Hx];
    exact Hx.
Qed.

Lemma F28_pythagorean_prime_divisibility :
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
  - replace (b^2) with (c^2-a^2).
    + apply F28_divide_difference.
      * replace (c^2) with (c*c)
          by ring.
        apply F28_divide_product.
        exact Hc.
      * replace (a^2) with (a*a)
          by ring.
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
    exact
      (F28_not_divide_4 p Hp Hlarge H4).

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
    exact
      (F28_not_divide_27
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
(* NONDIVISIBILITY FROM F = 0 MOD p         *)
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
(* NONDIVISIBILITY OF -6912bc               *)
(* ======================================== *)

Theorem F28_c6_factor_nonzero :
  forall p b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | b) ->
    ~ (p | c) ->
    ~ (p | -6912*b*c).
Proof.
  intros p b c Hp Hlarge Hnb Hnc.

  assert (Hconstant : ~ (p | -6912)).
  {
    intro Hnegative.

    assert (Hpositive : (p | 6912)).
    {
      replace 6912
        with ((-6912)*(-1)) by ring.
      apply F28_divide_product.
      exact Hnegative.
    }

    exact
      (F28_not_divide_6912
         p Hp Hlarge Hpositive).
  }

  assert (Hproduct : ~ (p | (-6912)*b)).
  {
    apply (F28_nonzero_product
             p (-6912) b).
    - exact Hp.
    - exact Hconstant.
    - exact Hnb.
  }

  replace (-6912*b*c)
    with (((-6912)*b)*c) by ring.

  apply (F28_nonzero_product
           p ((-6912)*b) c).
  - exact Hp.
  - exact Hproduct.
  - exact Hnc.
Qed.

(* ======================================== *)
(* DIRECT SQUARE-CLASS CERTIFICATE          *)
(* ======================================== *)

Theorem F28_direct_square_identity :
  forall a b c : Z,
    (a*b)*(-6912*b*c)-(32*a^2)^2
    =
    (-256*a)*F a b c.
Proof.
  intros a b c.
  unfold F.
  ring.
Qed.

Theorem F28_direct_product_certificate :
  forall p a b c : Z,
    (p | F a b c) ->
    ~ (p | a) ->
    F28_square_certificate
      p ((a*b)*(-6912*b*c)).
Proof.
  intros p a b c HF Hna.

  unfold F28_square_certificate.

  exists 1.
  exists (32*a^2).

  split.

  - intro H1.

    assert (Ha : (p | a)).
    {
      replace a with (1*a) by ring.
      apply F28_divide_product.
      exact H1.
    }

    exact (Hna Ha).

  - replace
      (((a*b)*(-6912*b*c))*1^2
         -(32*a^2)^2)
      with
      ((-256*a)*F a b c).
    + replace
        ((-256*a)*F a b c)
        with
        (F a b c*(-256*a))
        by ring.
      apply F28_divide_product.
      exact HF.
    + rewrite <- F28_direct_square_identity.
      ring.
Qed.

(* ======================================== *)
(* CERTIFICATE CANCELLATION                 *)
(* ======================================== *)

Theorem F28_certificate_cancel :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    F28_square_certificate p (x*y) ->
    F28_square_certificate p x ->
    F28_square_certificate p y.
Proof.
  intros p x y Hp Hnx Hxy Hx.

  destruct Hxy as
    [u [v [Hnu Hxyuv]]].

  destruct Hx as
    [r [s [Hnr Hxrs]]].

  unfold F28_square_certificate.

  exists (x*u*r).
  exists (v*s).

  split.

  - assert (Hnur : ~ (p | u*r)).
    {
      apply (F28_nonzero_product p u r).
      + exact Hp.
      + exact Hnu.
      + exact Hnr.
    }

    replace (x*u*r)
      with (x*(u*r)) by ring.

    apply (F28_nonzero_product
             p x (u*r)).
    + exact Hp.
    + exact Hnx.
    + exact Hnur.

  - replace
      (y*(x*u*r)^2-(v*s)^2)
      with
      ((x*y*u^2-v^2)*(x*r^2)
       +v^2*(x*r^2-s^2))
      by ring.

    apply F28_divide_sum.

    + apply F28_divide_product.
      exact Hxyuv.

    + replace
        (v^2*(x*r^2-s^2))
        with
        ((x*r^2-s^2)*v^2)
        by ring.

      apply F28_divide_product.
      exact Hxrs.
Qed.

Theorem F28_product_certificate_equivalence :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    F28_square_certificate p (x*y) ->
    (F28_square_certificate p x
     <-> F28_square_certificate p y).
Proof.
  intros p x y Hp Hnx Hny Hxy.

  split.

  - intro Hx.
    apply (F28_certificate_cancel p x y).
    + exact Hp.
    + exact Hnx.
    + exact Hxy.
    + exact Hx.

  - intro Hy.

    assert (Hyx :
      F28_square_certificate p (y*x)).
    {
      replace (y*x) with (x*y) by ring.
      exact Hxy.
    }

    apply (F28_certificate_cancel p y x).
    + exact Hp.
    + exact Hny.
    + exact Hyx.
    + exact Hy.
Qed.

(* ======================================== *)
(* FINAL INTEGRATED F.28 CHARACTER THEOREM  *)
(* ======================================== *)

Theorem F28_primitive_character_comparison :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    a^2 + b^2 = c^2 ->
    Z.gcd a b = 1 ->
    (p | F a b c) ->
    (F28_square_certificate p (a*b)
     <->
     F28_square_certificate p (-6912*b*c)).
Proof.
  intros p a b c
    Hp Hlarge Hpyth Hgcd HF.

  pose proof
    (F28_main_arithmetic
       p a b c Hp Hlarge Hpyth Hgcd HF)
    as Hmain.

  destruct Hmain as [Hna [Hnb Hnc]].

  apply
    (F28_product_certificate_equivalence
       p (a*b) (-6912*b*c)).

  - exact Hp.

  - apply (F28_nonzero_product p a b).
    + exact Hp.
    + exact Hna.
    + exact Hnb.

  - apply (F28_c6_factor_nonzero p b c).
    + exact Hp.
    + exact Hlarge.
    + exact Hnb.
    + exact Hnc.

  - apply F28_direct_product_certificate.
    + exact HF.
    + exact Hna.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_main_arithmetic.
Check F28_c6_factor_nonzero.
Check F28_direct_square_identity.
Check F28_primitive_character_comparison.

Print Assumptions F28_main_arithmetic.
Print Assumptions F28_primitive_character_comparison.

(* ======================================== *)
(* END                                      *)
(* ======================================== *)

(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026): the paper's criterion given that c is a square *)
(* ======================================== *)

Theorem F28_certificate_multiplicative :
  forall p x y : Z,
    prime p ->
    F28_square_certificate p x ->
    F28_square_certificate p y ->
    F28_square_certificate p (x*y).
Proof.
  intros p x y Hp Hx Hy.
  destruct Hx as [u [v [Hnu Hxu]]].
  destruct Hy as [r [s [Hnr Hyr]]].
  unfold F28_square_certificate.
  exists (u*r).
  exists (v*s).
  split.
  - apply (F28_nonzero_product p u r).
    + exact Hp.
    + exact Hnu.
    + exact Hnr.
  - replace (x*y*(u*r)^2-(v*s)^2)
      with ((x*u^2-v^2)*(y*r^2) + v^2*(y*r^2-s^2))
      by ring.
    apply F28_divide_sum.
    + apply F28_divide_product.
      exact Hxu.
    + replace (v^2*(y*r^2-s^2)) with ((y*r^2-s^2)*v^2) by ring.
      apply F28_divide_product.
      exact Hyr.
Qed.

Theorem F28_certificate_multiply_iff :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    F28_square_certificate p x ->
    (F28_square_certificate p (x*y)
     <-> F28_square_certificate p y).
Proof.
  intros p x y Hp Hnx Hx.
  split.
  - intro Hxy.
    exact (F28_certificate_cancel p x y Hp Hnx Hxy Hx).
  - intro Hy.
    exact (F28_certificate_multiplicative p x y Hp Hx Hy).
Qed.

(* c is a square mod p on the family (section 6).  Given that, the character comparison reads (ab/p) = +1 iff (-6912 b / p) = +1,
   and -6912 b = -c6_num b: the paper's criterion "split multiplicative iff (ab/p) = +1". *)
Theorem F28_primitive_split_criterion :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    a^2 + b^2 = c^2 ->
    Z.gcd a b = 1 ->
    (p | F a b c) ->
    F28_square_certificate p c ->
    (F28_square_certificate p (a*b)
     <->
     F28_square_certificate p (-6912*b)).
Proof.
  intros p a b c Hp Hlarge Hpyth Hgcd HF Hc.
  destruct (F28_main_arithmetic p a b c Hp Hlarge Hpyth Hgcd HF)
    as [Hna [Hnb Hnc]].
  pose proof (F28_primitive_character_comparison p a b c
                Hp Hlarge Hpyth Hgcd HF) as Hcmp.
  pose proof (F28_certificate_multiply_iff p c (-6912*b) Hp Hnc Hc)
    as Hmul.
  replace (c*(-6912*b)) with (-6912*b*c) in Hmul by ring.
  split.
  - intro Hab.
    exact (proj1 Hmul (proj1 Hcmp Hab)).
  - intro H6.
    exact (proj2 Hcmp (proj2 Hmul H6)).
Qed.

Print Assumptions F28_primitive_split_criterion.
