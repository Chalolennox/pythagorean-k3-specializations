(* code/coq/Dossier_sextic_F26.v

   THIS FILE: (3) sextic_cleared_identity: h(X) hT(X) = X^6 R(X + 2/X) (R as in F.26); sextic_norm_identity: R(z1+z2) = h(z1) h(z2) when z1 z2 = 2, through the explicit cofactor Rcof.
   Written by Claude (a language model) in review, 23 November 2026.  NO HUMAN HAS CHECKED IT; the only compile check is CI (Coq 8.20.1).  Standalone (ZArith, Lia, Ring only).
   Not one of the owner's files.  Part of the elementary dossier theorems (split into three files so that CI shows which part is slow or failing):
     Dossier_crt_two_adic.v   (1) generalized CRT compatibility, (2) the 2-adic covering of the positive integers;
     Dossier_sextic_F26.v     (3) the quotient sextic R of x -> 2/x (cleared identity, norm form with explicit cofactor);
     Dossier_Fs_g_hom.v       (4) the F_s congruences of Lemma R (F.52), (5) the homogeneous g(tau(t)) identity.
   The statements about x(Q+T) = 2/x and the rational form of g(tau(t)) are in Dossier_elementary_rational.v (QArith).
   WHAT IT DOES NOT PROVE: anything about elliptic curves or root numbers; polynomial identity, divisibility and counting only.  Each identity was also checked in exact arithmetic with
   code/verify_dossier_elementary.py.  The statements were chosen by Claude from the dossier text, so whether they are the statements the owner wants is for a human to check. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

(* ============================================================ *)
(* (3) THE QUOTIENT SEXTIC OF x -> 2/x  (paper F.26)            *)
(* ============================================================ *)

(* h(x) = H(1 - x) with H(t) = t^6 - 30 t^4 - 24 t^2 - 1 *)
Definition hZ (x : Z) : Z :=
  (1 - x)^6 - 30*(1 - x)^4 - 24*(1 - x)^2 - 1.

(* hT(X) = X^6 h(2/X), cleared of denominators:  (1 - 2/X) X = X - 2 *)
Definition hT (X : Z) : Z :=
  (X - 2)^6 - 30*(X - 2)^4*X^2 - 24*(X - 2)^2*X^4 - X^6.

Definition RZ (u : Z) : Z :=
  -54*u^6 + 648*u^5 - 1242*u^4 - 11404*u^3 + 62082*u^2 - 113832*u + 73224.

(* h(X) hT(X) = X^6 R(X + 2/X), with X^6 R(X + 2/X) = sum_k r_k (X^2 + 2)^k X^(6-k) *)
Theorem sextic_cleared_identity :
  forall X : Z,
    hZ X * hT X =
      -54*(X^2 + 2)^6
      + 648*(X^2 + 2)^5*X
      - 1242*(X^2 + 2)^4*X^2
      - 11404*(X^2 + 2)^3*X^3
      + 62082*(X^2 + 2)^2*X^4
      - 113832*(X^2 + 2)*X^5
      + 73224*X^6.
Proof.
  intros X.
  unfold hZ, hT.
  ring.
Qed.

Definition Rcof (z1 z2 : Z) : Z :=
  (-35154) + (52542)*z2^1 + (-25938)*z2^2 + (3002)*z2^3 + (1026)*z2^4 + (-162)*z2^5 + (52542)*z1^1 + (-66537)*z1^1*z2^1 + (28068)*z1^1*z2^2 + (-2385)*z1^1*z2^3 + (-1334)*z1^1*z2^4 + (189)*z1^1*z2^5 + (-25938)*z1^2 + (28068)*z1^2*z2^1 + (-11682)*z1^2*z2^2 + (1344)*z1^2*z2^3 + (630)*z1^2*z2^4 + (-100)*z1^2*z2^5 + (3002)*z1^3 + (-2385)*z1^3*z2^1 + (1344)*z1^3*z2^2 + (-301)*z1^3*z2^3 + (-78)*z1^3*z2^4 + (15)*z1^3*z2^5 + (1026)*z1^4 + (-1334)*z1^4*z2^1 + (630)*z1^4*z2^2 + (-78)*z1^4*z2^3 + (-38)*z1^4*z2^4 + (6)*z1^4*z2^5 + (-162)*z1^5 + (189)*z1^5*z2^1 + (-100)*z1^5*z2^2 + (15)*z1^5*z2^3 + (6)*z1^5*z2^4 + (-1)*z1^5*z2^5.

Lemma sextic_norm_cofactor :
  forall z1 z2 : Z,
    RZ (z1 + z2) - hZ z1 * hZ z2 = (z1*z2 - 2) * Rcof z1 z2.
Proof.
  intros z1 z2.
  unfold RZ, hZ, Rcof.
  ring.
Qed.

(* R(U) = Res_Z(Z^2 - U Z + 2, h(Z)) is the quadratic norm: R(z1 + z2) = h(z1) h(z2) when z1 z2 = 2 *)
Theorem sextic_norm_identity :
  forall z1 z2 : Z,
    z1 * z2 = 2 -> RZ (z1 + z2) = hZ z1 * hZ z2.
Proof.
  intros z1 z2 Hz.
  pose proof (sextic_norm_cofactor z1 z2) as E.
  rewrite Hz in E.
  assert (E2 : (2 - 2) * Rcof z1 z2 = 0) by ring.
  rewrite E2 in E.
  lia.
Qed.

(* ============================================================ *)
(* VERIFICATION                                                 *)
(* ============================================================ *)

Check sextic_cleared_identity.
Check sextic_norm_identity.

Print Assumptions sextic_cleared_identity.
Print Assumptions sextic_norm_identity.
