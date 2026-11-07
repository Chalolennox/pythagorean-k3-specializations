# Run log for the curated CAS scripts

Fill in one block per script when you run it. A script counts as *executed* only when this file has its block, with the
software version, the date, the exact command and the output (or a file with the output, and its SHA-256).

| Script | Software and version | Date | Command | Output file | SHA-256 | Agrees with the expectation in README_INTEGRATION.md? |
| --- | --- | --- | --- | --- | --- | --- |
| 01_rank_specializations.sage | Sage x.y | | `sage 01_rank_specializations.sage > out01.txt` | out01.txt | | |
| 02_rank_specializations.magma | Magma V2.xx | | `magma -b 02_rank_specializations.magma > out02.txt` | out02.txt | | |
| 03_circle_recursion.magma | | | | | | |
| 04_exceptional_elimination.magma | | | | | | |
| 05_constant_x_genus.sage | | | | | | |
| 06_genus3_obstruction.sage | | | | | | |
| 07_pythagorean_power_sequence.magma | | | | | | |
| 08_local_reduction_pari.gp | PARI/GP 2.x | | `gp -q 08_local_reduction_pari.gp < /dev/null > out08.txt` | out08.txt | | |
| 09_rank3_points_check.sage | | | | | | |
| 10_twist_section_identity.sage | | | | | | |
