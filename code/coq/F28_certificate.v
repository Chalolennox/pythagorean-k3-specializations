(* code/coq/F28_certificate.v

   The owner's ninth Coq file (22 November 2026), unchanged except for this header.  It is a separate compilation unit that repeats the
   definitions of F28_arithmetic.v.
   WHAT IT PROVES (no hypothesis on p besides the stated ones): if p | F(a,b,c) and p does not divide a, then x = a b c (-c6_num b)
   satisfies x a^2 = (216 b^2 c)^2 modulo p, i.e. x is a square mod p up to the square of the nonzero residue a (the "certificate").
   WHAT IT DOES NOT PROVE: the certificate does not exclude p | x (zero is a square too), no Legendre symbol or primality is used, and
   "c is a square on the family" is not in Coq.  The bridge F28_certificate_nonvanishing (p does not divide x, for a prime p >= 5,
   a primitive triple and p | F) is in F28_arithmetic.v, which has the needed lemmas. *)
From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Lia.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28 - QUADRATIC CHARACTER STAGE         *)
(* ======================================== *)

Definition F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition c4_num (a : Z) : Z :=
  -192*a.

Definition c6_num (b : Z) : Z :=
  6912*b.

(* ======================================== *)
(* PREVIOUSLY VERIFIED IDENTITY             *)
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

(* ======================================== *)
(* DIVISIBILITY HELPER                      *)
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

(* ======================================== *)
(* QUADRATIC RESIDUE CERTIFICATE            *)
(* ======================================== *)

Definition F28_square_certificate
  (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2 - v^2).

(* A certificate means that x becomes a
   square after multiplication by the
   square of a nonzero residue u.

   For prime p, this is equivalent to x
   being a square in F_p. *)

(* ======================================== *)
(* CONGRUENCE IN CERTIFICATE FORM           *)
(* ======================================== *)

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

(* ======================================== *)
(* MAIN NEW THEOREM                         *)
(* ======================================== *)

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

(* ======================================== *)
(* SIMPLIFIED CHARACTER ARGUMENT            *)
(* ======================================== *)

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
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_square_class_identity.
Check F28_certificate_congruence.

Check F28_quadratic_residue_certificate.
Check F28_character_product_certificate.

Print Assumptions
  F28_quadratic_residue_certificate.

Print Assumptions
  F28_character_product_certificate.

(* ======================================== *)
(* END                                      *)
(* ======================================== *)
