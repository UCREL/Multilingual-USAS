# Contributing Guidelines

Thank you for considering contributing to the USAS lexicon resources, these guidelines will help you understand how the repository is organised and how you can help add to it.

## Contributing a Lexicon Resource

All lexicon resources are orgainsed based on their language name, for example all of the `Welsh` lexicons are within the [./Welsh](./Welsh) folder. Further we also have a meta data file, [./language_resources.json](./language_resources.json), which describes these resources in more detail and in a structured format.

The steps to take when wanting to contribute a lexicon resource:

1. When constructing the resource it must be written following the format of the resource you want to construct:
    1. For single word lexicon files, follow the [single word lexicon file format described in the README.](./README.md#single-word-lexicon-file-format)
    2. For Multi Word Expression (MWE) lexicon files, follow the [MWE lexicon file format described in the README,](./README.md#multi-word-expression-mwe-lexicon-file-format)
    3. For autotag lexicon files, follow the [autotag lexicon file format described in the README.](./README.md#autotag-lexicon-file-format) Autotag files use the single word lexicon file format, but their `lemma` and `pos` values are patterns, which support `*` (zero or more of any character), `[...]` (a character class that matches exactly one character, e.g. `[0-9]`), and `[...]*` (zero or more characters from that class). Any single word entry whose `lemma` or `pos` is a pattern, e.g. `*-year-old`, should go in an autotag file named `semantic_lexicon_LANG_autotag.tsv`, whereby `LANG` is the same language suffix as the language's single word lexicon file, rather than in the single word lexicon file, as in a single word lexicon file `*`, `[` and `]` in the `lemma` are always literal. When writing autotag entries note that:
        * `[...]*` also matches **zero** characters, e.g. `[0-9]*ish` matches `9ish` and `10ish`, but also `ish`. If at least one character from the class is required, add a non-optional copy of the class before it, e.g. `[0-9][0-9]*ish`.
        * A literal `[` or `]` can only be written within a character class and has to be escaped with a `\`, e.g. `[\[]` matches `[` and `[\]]` matches `]`. An unescaped `[` within a character class, or a `]` that does not close a class, is invalid.
        * Every autotag entry needs a POS pattern, a `pos` value of just `*` is **not** allowed, however `*` alongside other characters is, e.g. `N*`.
        * Entries are matched in file order and only the first matching entry is used, so put more specific patterns before more general ones, see the [autotag lexicon file format section of the README](./README.md#autotag-lexicon-file-format).
    4. For all lexicon files, the `lemma`, `token`, and `pos` values cannot start or end with whitespace, e.g. `Noun ` is **not** allowed. For MWE lexicon files, each `{token}_{pos}` (or curly brace, e.g. `{N*/P*/R*}`) part of the `mwe_template` has to be separated by a single space (not a non-breaking space or tab), the `mwe_template` cannot start or end with whitespace, and neither the token nor the POS can be empty, e.g. `_*` is **not** allowed.

    In all cases these files are described as TSV files, **however** these files at this stage should be **text files**. They should follow TSV files with respect to having header names and tabs separating the columns. The main differences is that with these files you can also include comments using a `#` symbol at the start of each comment line **but** the comment line cannot include a tab character.

2. Once you have constructed your text file version of the lexicon file, **fork** this GitHub repository so that you can make a **pull request** in step 7, and then clone your fork to your computer.
3. Set up the development environment so that you can run the Python scripts in this repository, either locally or through a dev container, as described in the [Development Environment section of the README](./README.md#development-environment).
4. Within your forked version of this repository, save your constructed text version of the lexicon file to the relevant language name folder, if your language name folder does not exist create one.
5. Add your resource to the meta data file, [./language_resources.json](./language_resources.json), of which the [USAS Lexicon Meta Data section of the README](./README.md#usas-lexicon-meta-data) should be a good guide on how to add your resource to the meta data file, e.g. an autotag lexicon file is added with `"data type": "autotag"`. **NOTE** that the file path to your lexicon file should have the `.tsv` file extension rather than the expected `.txt`, as in the next step you will create a `TSV` file from your text file version of the lexicon.
6. From the root of the repository, run the following commands:

    ``` bash
    python txt_to_tsv.py
    python lexicon_statistics.py > ./lexicon_statistics.md
    python test_all_collections.py
    ```

    The first command converts your **text file** into a **TSV file** and checks it, in doing so it removes all comments so that only the text file will have comments and the TSV file will be comment free and represent a standard TSV file. The second command updates the [lexicon statistics table](./lexicon_statistics.md) and the last command checks that all of the TSV files are valid. If any of these commands fail, fix your text file and run the commands again.
7. Commit your changes, including the text file, the generated TSV file, `lexicon_statistics.md`, and `language_resources.json`, to your forked version of the repository, and submit your pull request. When creating the pull request leave the **"Allow edits by maintainers"** option ticked.

> [!NOTE]
> You need to run the commands in step 6 every time you change a lexicon text file. If you are unable to run them, still submit your pull request and say so in its description, a maintainer can then run the commands and push the result to your pull request (this requires the **"Allow edits by maintainers"** option to be ticked).

Once your pull request has been submitted, GitHub actions will check that your lexicon file is valid, and that the committed TSV files and `lexicon_statistics.md` are up to date with the text files, by running the same commands as in step 6. If any of the checks fail, we will work with you on the pull request so that your lexicon passes all of the checks.

## Any problems, contact us

If you have any problems let us know at: ucrel@lancaster.ac.uk
