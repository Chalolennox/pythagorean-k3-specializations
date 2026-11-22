(* code/coq/F28_character_comparison.v

   The owner's twelfth Coq file (22 November 2026), unchanged except for this header.  A standalone compilation unit; it is NOT a
   superset of F28_certificate.v (it has no multiplicativity, no c6_num) but reuses its cancellation and equivalence theorems.
   WHAT IT PROVES: F28_direct_square_identity: (ab)(-6912 b c) - (32 a^2)^2 = (-256 a) F(a,b,c) (hand-checked: both sides equal
   -6912 a b^2 c - 1024 a^4), so for p | F and p not dividing a the number x = (ab)(-6912 b c) is a square mod p outright (u = 1);
   and F28_character_comparison: for a prime p >= 5 with p | F and p not dividing a, b, c,
        (ab is a square certificate mod p)  <->  (-6912 b c is a square certificate mod p),
   i.e. (ab/p) = +1 iff (-6912 b c / p) = +1, where -6912 b = -c6_num b.
   WHAT IT DOES NOT PROVE (the title "complete" should not be read as more): the right side is (-c6 . c / p), so to reach the paper's
   criterion "(ab/p) = +1 iff (-c6/p) = +1" one needs c to be a square mod p (true on the family, section 6, but not in Coq; the
   combination with a certificate for c is F28_split_criterion in F28_certificate.v); no Legendre symbol; no Tate/Kodaira step. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28 - COMPLETE CHARACTER COMPARISON     *)
(* ======================================== *)

Definition F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_square_certificate
  (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2 - v^2).

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
  apply F28_prime_product_split
    with (x := x) (y := y) in Hxy.
  - destruct Hxy as [H | H].
    + exact (Hx H).
    + exact (Hy H).
  - exact Hp.
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
    (k <= -1 \/ k = 0 \/ k >= 1)
    by lia.

  destruct H as [Hneg | [Hzero | Hpositive]].
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

(* ======================================== *)
(* NEW: PRIME DOES NOT DIVIDE 6912          *)
(* ======================================== *)

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

Lemma F28_not_divide_16 :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 16).
Proof.
  intros p Hp Hlarge H16.

  replace 16 with (4*4) in H16 by ring.

  pose proof
    (F28_prime_product_split
       p 4 4 Hp H16) as Hsplit.

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
       p 16 16 Hp H256) as Hsplit.

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
       p 256 27 Hp H6912) as Hsplit.

  destruct Hsplit as [H256 | H27].
  - exact
      (F28_not_divide_256
         p Hp Hlarge H256).
  - exact
      (F28_not_divide_27
         p Hp Hlarge H27).
Qed.

(* ======================================== *)
(* NEW: NONDIVISIBILITY OF -6912bc          *)
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
(* DIRECT SQUARE-CLASS IDENTITY             *)
(* ======================================== *)

Theorem F28_direct_square_identity :
  forall a b c : Z,
    (a*b)*(-6912*b*c) - (32*a^2)^2
    =
    (-256*a)*F a b c.
Proof.
  intros a b c.
  unfold F.
  ring.
Qed.

Theorem F28_direct_square_congruence :
  forall p a b c : Z,
    (p | F a b c) ->
    (p |
      (a*b)*(-6912*b*c)
        - (32*a^2)^2).
Proof.
  intros p a b c HF.

  rewrite F28_direct_square_identity.

  replace ((-256*a)*F a b c)
    with (F a b c*(-256*a))
    by ring.

  apply F28_divide_product.
  exact HF.
Qed.

(* ======================================== *)
(* DIRECT PRODUCT CERTIFICATE               *)
(* ======================================== *)

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
        - (32*a^2)^2)
      with
      ((a*b)*(-6912*b*c)
        - (32*a^2)^2)
      by ring.

    apply F28_direct_square_congruence.
    exact HF.
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
(* MAIN NEW THEOREM                         *)
(* ======================================== *)

Theorem F28_character_comparison :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    (p | F a b c) ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (F28_square_certificate p (a*b)
     <->
     F28_square_certificate p (-6912*b*c)).
Proof.
  intros p a b c
    Hp Hlarge HF Hna Hnb Hnc.

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
(* FINAL VERIFICATION                       *)
(* ======================================== *)

Check F28_not_divide_6912.
Check F28_c6_factor_nonzero.
Check F28_direct_square_identity.
Check F28_direct_product_certificate.
Check F28_character_comparison.

Print Assumptions F28_not_divide_6912.
Print Assumptions F28_c6_factor_nonzero.
Print Assumptions F28_direct_square_identity.
Print Assumptions F28_character_comparison.

(* ======================================== *)
(* END                                      *)
(* ======================================== *)
