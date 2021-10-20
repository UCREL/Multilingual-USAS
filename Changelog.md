# Major changes

MWE = Multi Word Expression

1. Changed the file extension of all semantic lexicon files from `.usas` to `.tsv` 
2. Added a [License file](./LICENSE) which contains the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. This file was added so that on GitHub under the About section in the right hand corner there is a link that says `View License` which will direct users to this [License file](./LICENSE).
3. Reformated the [README.md](./README.md) so that it contains more structure. New content is added around File formats of single and MWE lexicon files. Added a section on how to use the [test_collection.py python script.](./test_collection.py).
4. Within the [MWE lexicon for Chinese](./Chinese/mwe-chi.tsv). Line 119 and 101 was removed as it contained a MWE template but no USAS tags. The MWE templates were `平顶_noun 女帽_noun` and `一_num 法郎_msr N3.1/I1` respectively.