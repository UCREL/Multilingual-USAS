# Contributing Guidelines

Thank you for considering contributing to the USAS lexicon resources, these guidelines will help you understand how the repository is organised and how you can help add to it.

## Contributing a Lexicon Resource

All lexicon resources are orgainsed based on their language name, for example all of the `Welsh` lexicons are within the [./Welsh](./Welsh) folder. Further we also have a meta data file, [./language_resources.json](./language_resources.json), which describes these resources in more detail and in a structured format.

The steps to take when wanting to contribute a lexicon resource:

1. When constructing the resource it must be written following the format of the resource you want to construct:
    1. For single word lexicon files, follow the [single word lexicon file format described in the README.](./README.md#single-word-lexicon-file-format)
    2. For Multi Word Expression (MWE) lexicon files, follow the [MWE lexicon file format described in the README,](./README.md#multi-word-expression-mwe-lexicon-file-format)

    In both cases these files are described as TSV files, **however** these files at this stage should be **text files**. They should follow TSV files with respect to having header names and tabs separating the columns. The main differences is that with these files you can also include comments using a `#` symbol at the start of each comment line **but** the comment line cannot include a tab character.

2. Once you have constructed your text file version of the lexicon file, **fork** this GitHub repository so that you can make a **pull request** in step 7, and then clone your fork to your computer.
3. Set up the development environment so that you can run the Python scripts in this repository, either locally or through a dev container, as described in the [Development Environment section of the README](./README.md#development-environment).
4. Within your forked version of this repository, save your constructed text version of the lexicon file to the relevant language name folder, if your language name folder does not exist create one.
5. Add your resource to the meta data file, [./language_resources.json](./language_resources.json), of which the [USAS Lexicon Meta Data section of the README](./README.md#usas-lexicon-meta-data) should be a good guide on how to add your resource to the meta data file. **NOTE** that the file path to your lexicon file should have the `.tsv` file extension rather than the expected `.txt`, as in the next step you will create a `TSV` file from your text file version of the lexicon.
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
