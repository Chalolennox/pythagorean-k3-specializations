(* code/coq/F28_identities.v

   Polynomial identities used in the proof of F.28 (exact root-number formula), checked with `ring`.
   Part 1 is the owner's file, unchanged except for this header; part 2 was added in review (22 November 2026).
   WHAT IS CHECKED: ring identities over Z.  WHAT IS NOT: the quadratic-character reasoning, Rizzo's tables, the local root
   numbers at 2, 3 and at primes dividing c, Appendix B.  So F.28 as a whole is not machine-checked.
   Compiled in CI (.github/workflows/coq.yml, `coqc`); not compiled by the reviewer locally (no Coq in that sandbox).

   NOTATION.  F a b c = 4a^3 + 27 b^2 c (the "triple form"); the sextic F(U,V) = U^6 - 30U^4V^2 - 24U^2V^4 - V^6 of the paper
   satisfies F(a,b,c) = -4 F(U,V) for (a,b,c) = (V^2-U^2, 2UV, U^2+V^2) (Theorem F28_triple_vs_sextic below). *)

From Coq Require Import ZArith.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* PART 1.  F.28: CORRECTED ARITHMETIC IDENTITIES  (owner)  *)
(* ======================================== *)

Definition F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition c4_num (a : Z) : Z :=
  -192*a.

Definition c6_num (b : Z) : Z :=
  6912*b.

(* ---------------------------------------- *)
(* 1. Character identity                    *)
(* ---------------------------------------- *)

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

(* ---------------------------------------- *)
(* 2. Discriminant numerator identity       *)
(* Delta = -1024*F/c^3  (model y^2 = x^3 + 4(a/c)x - 8(b/c); numerator after clearing c^3) *)
(* ---------------------------------------- *)

Theorem F28_discriminant_identity :
  forall a b c : Z,
    -16 * (4*(4*a)^3
           + 27*(-8*b)^2*c)
    =
    -1024*F a b c.
Proof.
  intros a b c.
  unfold F.
  ring.
Qed.

(* ---------------------------------------- *)
(* 3. c4 numerator identity                 *)
(* ---------------------------------------- *)

Theorem F28_c4_identity :
  forall a : Z,
    c4_num a = -192*a.
Proof.
  intro a.
  unfold c4_num.
  reflexivity.
Qed.

(* ---------------------------------------- *)
(* 4. c6 numerator identity                 *)
(* ---------------------------------------- *)

Theorem F28_c6_identity :
  forall b : Z,
    c6_num b = 6912*b.
Proof.
  intro b.
  unfold c6_num.
  reflexivity.
Qed.

(* ======================================== *)
(* PART 2.  Added in review: the integral model and the steps of the proof of F.28 *)
(* ======================================== *)

(* The integral model Y^2 = X^3 + A X + B with A = 4 a c^3, B = -8 b c^5 has Delta = -16 (4 A^3 + 27 B^2) = -1024 c^9 F.
   (Parts 1.3 and 1.4 are definitional; these are the statements with the powers of c.) *)

Theorem F28_discriminant_integral_model :
  forall a b c : Z,
    -16 * (4*(4*a*c^3)^3 + 27*(-8*b*c^5)^2)
    =
    -1024*c^9*F a b c.
Proof.
  intros a b c.
  unfold F.
  ring.
Qed.

Theorem F28_c4_integral_model :
  forall a c : Z,
    -48*(4*a*c^3) = -192*a*c^3.
Proof.
  intros a c.
  ring.
Qed.

Theorem F28_c6_integral_model :
  forall b c : Z,
    -864*(-8*b*c^5) = 6912*b*c^5.
Proof.
  intros b c.
  ring.
Qed.

(* The triple form and the sextic form of F. *)

Theorem F28_triple_vs_sextic :
  forall U V : Z,
    F (V^2 - U^2) (2*U*V) (U^2 + V^2)
    =
    -4*(U^6 - 30*U^4*V^2 - 24*U^2*V^4 - V^6).
Proof.
  intros U V.
  unfold F.
  ring.
Qed.

(* Delta = 2^12 c0^9 F(U,V) for a = V^2 - U^2, b = 2UV, c0 = U^2 + V^2, as stated in F.28. *)

Theorem F28_discriminant_UV :
  forall U V : Z,
    -16 * (4*(4*(V^2 - U^2)*(U^2 + V^2)^3)^3
           + 27*(-8*(2*U*V)*(U^2 + V^2)^5)^2)
    =
    4096*(U^2 + V^2)^9*(U^6 - 30*U^4*V^2 - 24*U^2*V^4 - V^6).
Proof.
  intros U V.
  ring.
Qed.

(* A prime p >= 5 dividing F cannot divide V^2 - U^2 or c0 = U^2 + V^2:
   F(U,V) = -54 V^6 (mod V^2 - U^2) and F(U,V) = -8 V^6 (mod U^2 + V^2), with explicit quotients. *)

Theorem F28_F_mod_difference :
  forall U V : Z,
    U^6 - 30*U^4*V^2 - 24*U^2*V^4 - V^6
    =
    -54*V^6 + (U^2 - V^2)*(U^4 - 29*U^2*V^2 - 53*V^4).
Proof.
  intros U V.
  ring.
Qed.

Theorem F28_F_mod_hypotenuse :
  forall U V : Z,
    U^6 - 30*U^4*V^2 - 24*U^2*V^4 - V^6
    =
    -8*V^6 + (U^2 + V^2)*(U^4 - 31*U^2*V^2 + 7*V^4).
Proof.
  intros U V.
  ring.
Qed.

(* Axiom check: each line prints "Closed under the global context". *)
Print Assumptions F28_character_identity.
Print Assumptions F28_discriminant_identity.
Print Assumptions F28_discriminant_integral_model.
Print Assumptions F28_triple_vs_sextic.
Print Assumptions F28_discriminant_UV.
Print Assumptions F28_F_mod_difference.
Print Assumptions F28_F_mod_hypotenuse.
