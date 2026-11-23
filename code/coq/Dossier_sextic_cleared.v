(* code/coq/Dossier_sextic_cleared.v

   THIS FILE: (3a) sextic_cleared_identity: h(X) hT(X) = X^6 R(X + 2/X) (R as in F.26), a univariate polynomial identity.
   Written by Claude (a language model) in review, 23 November 2026.  NO HUMAN HAS CHECKED IT; the only compile check is CI (Coq 8.20.1).  Standalone (ZArith, Lia, Ring only).
   Not one of the owner's files.  Part of the elementary dossier theorems (split into several files so that CI shows which part is slow or failing):
     Dossier_crt_two_adic.v   (1) generalized CRT compatibility, (2) the 2-adic covering of the positive integers;
     Dossier_sextic_cleared.v (3a) the quotient sextic R of x -> 2/x: the cleared identity h hT = X^6 R(X + 2/X);
     Dossier_sextic_norm.v    (3b) the norm form R(z1+z2) = h(z1) h(z2) for z1 z2 = 2, with an explicit cofactor;
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

(* ============================================================ *)
(* VERIFICATION                                                 *)
(* ============================================================ *)

Check sextic_cleared_identity.

Print Assumptions sextic_cleared_identity.
