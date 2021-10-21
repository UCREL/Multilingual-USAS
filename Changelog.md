# Major changes

MWE = Multi Word Expression

1. Changed the file extension of all semantic lexicon files from `.usas` to `.tsv` 
2. Added a [License file](./LICENSE) which contains the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. This file was added so that on GitHub under the About section in the right hand corner there is a link that says `View License` which will direct users to this [License file](./LICENSE).
3. Reformated the [README.md](./README.md) so that it contains more structure. New content is added around File formats of single and MWE lexicon files.
4. Within the [MWE lexicon for Chinese](./Chinese/mwe-chi.tsv). Line 119 and 101 was removed as it contained a MWE template but no USAS tags. The MWE templates were `平顶_noun 女帽_noun` and `一_num 法郎_msr N3.1/I1` respectively.
5. Within the [single lexicon for Dutch](./Dutch/semantic_lexicon_dut.tsv). Line 218 we have added a tab so that the POS entry is now blank/None as no POS information existed, without adding this extra tab the TSV file would not be valid. The changed meant on line 218 it went from `alstublieft	E4.2+ E2+ X7+ Z4` to `alstublieft		E4.2+ E2+ X7+ Z4`
6. For the [Malay single lexicon](./Malay/semantic_laexicon_ms.tsv), I tested to see if the first column was a repeat of the second column using the [test_token_is_equal_to_lemma.py python script](./test_token_is_equal_to_lemma.py) and it was. The first and the second column both represented the `lemma` field. In addition the [Malay single lexicon](./Malay/semantic_laexicon_ms.tsv) also contained a `POS` column that only contained the word `POS` therefore this column was also removed.
7. Created a scripts section within the [README.md](./README.md), the scripts section contains explanations on what the new python scripts do and how to use them.