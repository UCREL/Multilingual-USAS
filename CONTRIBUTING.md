# Contributing Guidelines

Thank you for considering contributing to the USAS lexicon resources, these guidelines will help you understand how the repository is organised and how you can help add to it.

## Contributing a Lexicon Resource

All lexicon resources are orgainsed based on their language name, for example all of the `Welsh` lexicons are within the [../Welsh](../Welsh) folder. Further we also have a meta data file, [../lexicon_resources.json](../lexicon_resources.json), which describes these resources in more detail and in a structured format.

The steps to take when wanting to contribute a lexicon resource:

1. When constructing the resource it must be written following the format of the resource you want to construct:
    1. For single word lexicon files, follow the [single word lexicon file format described in the README.](../README.md#single-word-lexicon-file-format)
    2. For Multi Word Expression (MWE) lexicon files, follow the [MWE lexicon file format described in the README,](../README.md#multi-word-expression-mwe-lexicon-file-format)

In both cases these files are described as TSV files, **however** these files at this stage should be **text files**. They should follow TSV files with respect to having header names and tabs separating the columns. The main differences is that with these files you can also include comments using a `#` symbol at the start of each comment line **but** the comment line cannot include a tab character.

2. Once you have constructed your text file version of the lexicon file, **fork** this GitHub repository so that you can make a **pull request** in step 5. 
3. Within your forked version of this repository, save your constructed text version of the lexicon file to the relevant language name folder, if your language name folder does not exist create one.
4. Add your resource to the meta data file, [../lexicon_resources.json](../lexicon_resources.json), of which the [USAS Lexicon Meta Data section of the README](../README.md#usas-lexicon-meta-data) should be a good guide on how to add your resource to the meta data file. **NOTE** that the file path to your lexicon file should have the `.tsv` file extension rather than the expected `.txt`, as in a later step our code will automatically create a `TSV` file from your text file version of the lexicon. 
5. Commit your changes to your forked version of the repository, and submit your pull request.

Once your pull request has been submitted, GitHub actions will perform some validation checks on you lexicon file, and then convert it from a **text file** to a **TSV file** in doing so it will remove all comments so that only the text file will have comments and TSV file will be comment free and represent a standard TSV file. If any of the validations checks fail, we will work with you on the pull request so that your lexicon passes all of the validation checks.

## Any problems, contact us

If you have any problems let us know at: ucrel@lancaster.ac.uk
