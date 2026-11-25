# Multiplication blocks: full affine span (25 November 2026)

Let a_n and b_n be the parity of the number of distinct qualifying primes on nP and nP+T, respectively (not the global root-number parity on the mirror branch). Put A_n=(a_n,a_{2n},a_{3n},a_{6n}) and B_n=(b_n,a_{2n},b_{3n},a_{6n}), in row-major order. The shared entries follow from 2T=0.

## Reused arithmetic data

The exact eligible-prime rectangle output of 24 November (through n=9) gives:
- a_1,...,a_9 = 0,1,1,1,1,0,0,1,0.
- b_1,...,b_9 = 0,1,0,1,0,1,0,1,1.

The canonical paper, F.38, records the complete probable-prime factorization at 12P, with s=3, f=+1, W=-1. Thus a_12=1. The listed factors are 23, 83, 18397, 7851197, 172604961553, 3022285517285783321, and 63444875642234219830688037601870240082732857828883494817671516344727361247789078750329402859044190800003740275757566803. No new factorization or primality certification is claimed.

## Full affine span without the quadratic-twist witness

Write z=a_18, which need not be known. The five rows, augmented by a leading 1, are:

    A_1  1 0 1 1 0
    B_1  1 0 1 0 0
    A_2  1 1 1 0 1
    A_3  1 1 0 0 z
    B_3  1 0 0 1 z

Exact Gaussian elimination over F_2 gives the identity matrix for both z=0 and z=1. Thus the affine span of the combined original and mirror blocks is all of F_2^4, on the recorded arithmetic data. Conditional on the recorded arithmetic data, every nonzero affine coefficient vector is excluded. This strengthens the earlier calculation using x=1/3: no twist witness is needed, and its factorization is not relied upon.

## Scope and stopping criterion

Conditional on the recorded arithmetic inputs, close the search for a universal affine parity identity on the union of these two branches. This does not exclude branch-specific identities, nonlinear restrictions, eventual identities, or establish recurrence of any configuration. It does not prove Problem H or exclude the all-odd block. The original branch alone remains a separate affine-span question. The arithmetic input from F.38 uses probable primes, as explicitly stated in the paper.

## Review correction: exact dependence on the arithmetic input

Proof given (ChatGPT, AI-authored; human review pending). In the displayed augmented matrix replace the last entry of A_2 by w=a_12. Add B_1 to each of the other rows, then add the resulting A_1 row to the resulting B_3 row. The four rows with leading zero, after dropping that coordinate, are (0,0,1,0), (1,0,0,w), (1,1,0,z), (0,1,0,z). Adding the last two gives (1,0,0,0); adding this to the second gives (0,0,0,w). Thus the augmented rank is 5 if w=1 and 4 if w=0, independently of z. Exact elimination independently executed by ChatGPT on all four (w,z) combinations: ranks 4,4,5,5 in lexicographic order. This confirms Claude comment 7167339349. The full-span conclusion is conditional on the recorded a_n,b_n and in particular on the probable-prime factorization in F.38; if w=0 these five rows alone do not establish full span. The original 24 November raw rectangle log has not been recovered in this review; its listed bits remain inputs, not independently verified here.
