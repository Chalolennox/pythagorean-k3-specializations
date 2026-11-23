(* code/coq/Dossier_Fs_g_hom.v

   THIS FILE: (4) Fs_mod_U, Fs_mod_V, Fs_factorization, Fs_mod_V_minus_U, Fs_mod_V_plus_U (F_s = -V^6, U^6, -54U^6); (5) g_hom_tau: g_hom(-(a+b), b-a) = 4 g_hom(a,b).
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
(* (4) THE CONGRUENCES OF F_s (Lemma R of F.52)                 *)
(* ============================================================ *)

Definition Fs (U V : Z) : Z :=
  U^6 - 30*U^4*V^2 - 24*U^2*V^4 - V^6.

Theorem Fs_mod_U :
  forall U V : Z, (U | Fs U V + V^6).
Proof.
  intros U V.
  exists (U^5 - 30*U^3*V^2 - 24*U*V^4).
  unfold Fs.
  ring.
Qed.

Theorem Fs_mod_V :
  forall U V : Z, (V | Fs U V - U^6).
Proof.
  intros U V.
  exists (-30*U^4*V - 24*U^2*V^3 - V^5).
  unfold Fs.
  ring.
Qed.

Definition Fs_cofactor (U V : Z) : Z :=
  -30*U^4 - 24*U^2*(V^2 + U^2) - (V^4 + V^2*U^2 + U^4).

(* F_s(U,V) + 54 U^6 = (V - U)(V + U) K : F_s(U, +-U) = -54 U^6 *)
Theorem Fs_factorization :
  forall U V : Z,
    Fs U V + 54*U^6 = (V - U) * ((V + U) * Fs_cofactor U V).
Proof.
  intros U V.
  unfold Fs, Fs_cofactor.
  ring.
Qed.

Theorem Fs_mod_V_minus_U :
  forall U V W : Z, (W | V - U) -> (W | Fs U V + 54*U^6).
Proof.
  intros U V W [c Hc].
  rewrite Fs_factorization.
  rewrite Hc.
  exists (c * ((V + U) * Fs_cofactor U V)).
  ring.
Qed.

Theorem Fs_mod_V_plus_U :
  forall U V W : Z, (W | V + U) -> (W | Fs U V + 54*U^6).
Proof.
  intros U V W [c Hc].
  rewrite Fs_factorization.
  rewrite Hc.
  exists (c * ((V - U) * Fs_cofactor U V)).
  ring.
Qed.

(* ============================================================ *)
(* (5) g(tau(t)) = 4 g(t) / (1 - t)^4, homogeneous form         *)
(* ============================================================ *)

(* t = a/b, g(t) = 2 t (1 - t^2) = g_hom(a,b)/b^4; tau(t) = 1 - 2/(1 - t) = -(a + b)/(b - a). *)
Definition g_hom (a b : Z) : Z :=
  2*a*b*(b^2 - a^2).

Theorem g_hom_tau :
  forall a b : Z,
    g_hom (-(a + b)) (b - a) = 4 * g_hom a b.
Proof.
  intros a b.
  unfold g_hom.
  ring.
Qed.

(* ============================================================ *)
(* VERIFICATION                                                 *)
(* ============================================================ *)

Check Fs_mod_U.
Check Fs_mod_V.
Check Fs_mod_V_minus_U.
Check Fs_mod_V_plus_U.
Check g_hom_tau.

Print Assumptions Fs_mod_U.
Print Assumptions Fs_mod_V.
Print Assumptions Fs_mod_V_minus_U.
Print Assumptions Fs_mod_V_plus_U.
Print Assumptions g_hom_tau.
