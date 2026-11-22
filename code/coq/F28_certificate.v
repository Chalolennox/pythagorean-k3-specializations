(* code/coq/F28_certificate.v

   The owner's eleventh Coq file (22 November 2026), unchanged except for this header; it supersedes the ninth and tenth (it contains
   their certificate theorems and adds cancellation).  Standalone compilation unit (repeats the definitions of F28_arithmetic.v).
   WHAT IT PROVES: the "square certificate" p | x u^2 - v^2 (p not dividing u) for x = a b c (-c6_num b) when p | F and p does not
   divide a; squares have certificates; certificates are closed under products (p prime) and congruence; and (p prime, p not dividing x)
   cancellation: if x and x y have certificates then so does y (F28_certificate_cancel, F28_certificate_multiply_iff,
   F28_product_certificate_equivalence).
   WHAT IT DOES NOT PROVE: a certificate allows x = 0 (v = 0), and the file has no Legendre symbol; for p not dividing x a certificate
   means that x is a NONZERO square mod p.  The added part combines the owner's theorems into the paper's criterion
   F28_split_criterion: (ab/p) = +1 iff (-c6/p) = +1, given c a square mod p.  "c is a square on the family" is not in Coq. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28 - QUADRATIC CERTIFICATE CANCELLATION *)
(* ======================================== *)

Definition F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition c6_num (b : Z) : Z :=
  6912*b.

Definition F28_square_certificate
  (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2 - v^2).

(* ======================================== *)
(* PREVIOUSLY VERIFIED IDENTITIES           *)
(* ======================================== *)

Theorem F28_square_class_identity :
  forall a b c : Z,
    a^3*b*c*(-c6_num b)
      - (216*b^2*c)^2
    =
    (-1728*b^2*c)*F a b c.
Proof.
  intros a b c.
  unfold F, c6_num.
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

Theorem F28_certificate_congruence :
  forall p a b c : Z,
    (p | F a b c) ->
    (p |
      (a*b*c*(-c6_num b))*a^2
        - (216*b^2*c)^2).
Proof.
  intros p a b c HF.

  replace
    ((a*b*c*(-c6_num b))*a^2
       - (216*b^2*c)^2)
    with
    (a^3*b*c*(-c6_num b)
       - (216*b^2*c)^2)
    by ring.

  rewrite F28_square_class_identity.

  replace
    ((-1728*b^2*c)*F a b c)
    with
    (F a b c*(-1728*b^2*c))
    by ring.

  apply F28_divide_product.
  exact HF.
Qed.

Theorem F28_quadratic_residue_certificate :
  forall p a b c : Z,
    (p | F a b c) ->
    ~ (p | a) ->
    F28_square_certificate
      p (a*b*c*(-c6_num b)).
Proof.
  intros p a b c HF Hna.

  unfold F28_square_certificate.

  exists a.
  exists (216*b^2*c).

  split.
  - exact Hna.
  - apply F28_certificate_congruence.
    exact HF.
Qed.

Theorem F28_character_product_certificate :
  forall p a b c : Z,
    (p | F a b c) ->
    ~ (p | a) ->
    F28_square_certificate
      p ((a*b)*(-6912*b*c)).
Proof.
  intros p a b c HF Hna.

  replace
    ((a*b)*(-6912*b*c))
    with
    (a*b*c*(-c6_num b))
    by (unfold c6_num; ring).

  apply F28_quadratic_residue_certificate.
  - exact HF.
  - exact Hna.
Qed.

(* ======================================== *)
(* VERIFIED PRIME PRODUCT LEMMAS            *)
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

  pose proof
    (F28_prime_product_split
       p x y Hp Hxy)
    as Hsplit.

  destruct Hsplit as [Hpx | Hpy].
  - exact (Hx Hpx).
  - exact (Hy Hpy).
Qed.

(* ======================================== *)
(* VERIFIED SQUARE CERTIFICATES             *)
(* ======================================== *)

Theorem F28_square_has_certificate :
  forall p z : Z,
    ~ (p | z) ->
    F28_square_certificate p (z^2).
Proof.
  intros p z Hz.

  unfold F28_square_certificate.

  exists 1.
  exists z.

  split.
  - intro H1.

    assert (Hzdiv : (p | z)).
    {
      replace z with (1*z) by ring.
      apply F28_divide_product.
      exact H1.
    }

    exact (Hz Hzdiv).

  - replace (z^2*1^2-z^2)
      with 0 by ring.

    exists 0.
    ring.
Qed.

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

  - replace
      (x*y*(u*r)^2-(v*s)^2)
      with
      ((x*u^2-v^2)*(y*r^2)
       +v^2*(y*r^2-s^2))
      by ring.

    apply F28_divide_sum.

    + apply F28_divide_product.
      exact Hxu.

    + replace
        (v^2*(y*r^2-s^2))
        with
        ((y*r^2-s^2)*v^2)
        by ring.

      apply F28_divide_product.
      exact Hyr.
Qed.

Theorem F28_certificate_congruence_invariant :
  forall p x y : Z,
    (p | x-y) ->
    F28_square_certificate p y ->
    F28_square_certificate p x.
Proof.
  intros p x y Hxy Hy.

  destruct Hy as [u [v [Hnu Hyuv]]].

  unfold F28_square_certificate.

  exists u.
  exists v.

  split.
  - exact Hnu.

  - replace
      (x*u^2-v^2)
      with
      ((x-y)*u^2+(y*u^2-v^2))
      by ring.

    apply F28_divide_sum.

    + apply F28_divide_product.
      exact Hxy.

    + exact Hyuv.
Qed.

(* ======================================== *)
(* NEW: CANCELLATION OF CERTIFICATES        *)
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

(* ======================================== *)
(* NEW: MULTIPLICATION EQUIVALENCE          *)
(* ======================================== *)

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
    apply (F28_certificate_cancel p x y).
    + exact Hp.
    + exact Hnx.
    + exact Hxy.
    + exact Hx.

  - intro Hy.
    apply (F28_certificate_multiplicative
             p x y).
    + exact Hp.
    + exact Hx.
    + exact Hy.
Qed.

(* ======================================== *)
(* NEW: PRODUCT CERTIFICATE EQUIVALENCE     *)
(* ======================================== *)

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
(* FINAL VERIFICATION                       *)
(* ======================================== *)

Check F28_character_product_certificate.

Check F28_square_has_certificate.
Check F28_certificate_multiplicative.
Check F28_certificate_congruence_invariant.

Check F28_certificate_cancel.
Check F28_certificate_multiply_iff.
Check F28_product_certificate_equivalence.

Print Assumptions F28_certificate_cancel.
Print Assumptions F28_certificate_multiply_iff.
Print Assumptions
  F28_product_certificate_equivalence.

(* ======================================== *)
(* END                                      *)
(* ======================================== *)

(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026): the character relation and the split criterion *)
(* ======================================== *)

(* If p | F, p does not divide a and c, and c is a square mod p (as it is on the family), then a b (-c6) is a square
   class mod p.  The hypotheses "p does not divide a, c" are supplied by F28_main_arithmetic in F28_arithmetic.v. *)
Theorem F28_character_relation :
  forall p a b c : Z,
    prime p ->
    (p | F a b c) ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_square_certificate p c ->
    F28_square_certificate p (a*b*(-c6_num b)).
Proof.
  intros p a b c Hp HF Hna Hnc Hc.
  pose proof (F28_quadratic_residue_certificate p a b c HF Hna) as Hq.
  replace (a*b*c*(-c6_num b)) with (c*(a*b*(-c6_num b))) in Hq by ring.
  exact (F28_certificate_cancel p c (a*b*(-c6_num b)) Hp Hnc Hq Hc).
Qed.

(* The paper's criterion, in certificate form: (ab/p) = +1 iff (-c6/p) = +1, where "(-c6/p) = +1" is the split-multiplicative
   condition.  Nonvanishing hypotheses: p does not divide a, b, c, -c6 (F28_main_arithmetic and F28_certificate_nonvanishing). *)
Theorem F28_split_criterion :
  forall p a b c : Z,
    prime p ->
    (p | F a b c) ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    ~ (p | -c6_num b) ->
    F28_square_certificate p c ->
    (F28_square_certificate p (a*b)
     <-> F28_square_certificate p (-c6_num b)).
Proof.
  intros p a b c Hp HF Hna Hnb Hnc Hn6 Hc.
  pose proof (F28_character_relation p a b c Hp HF Hna Hnc Hc) as Hrel.
  exact (F28_product_certificate_equivalence p (a*b) (-c6_num b) Hp
           (F28_nonzero_product p a b Hp Hna Hnb) Hn6 Hrel).
Qed.

Print Assumptions F28_character_relation.
Print Assumptions F28_split_criterion.
