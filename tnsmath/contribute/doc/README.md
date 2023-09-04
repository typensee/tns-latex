Contribute to the documentation of `tnscore`
============================================

> **I beg your pardon for my english...**
>
> English is not my native language, so be nice if you notice misunderstandings, misspellings, or grammatical errors in my documents and codes.


Where are the translations?
---------------------------

The translations made are in the `contribute/doc` folder which has the following minimal structure.

<!-- FOLDER STRUCT. AUTO - START -->

    + doc
        * LICENSE.txt
        * README.md
        + changes
            * LICENSE.txt
        + user
            + changelog
                * test_one_date.tex
                + fr
            + manual
                + fr

<!-- FOLDER STRUCT. AUTO - END -->


Start a new translation
-----------------------

As the author of `tnscore` is a French amateur coder, the documentation is only actively maintained in French. Here is how to translate it.

  1. The user manual translations are made inside the folder `contribute/doc/user/manual`, where as the ones about changes log for the users are done inside `contribute/doc/user/changelog`.

  1. The folders `fr` inside `manual` and `changelog` contains the last version of the french files to be translated.

  1. Start by copying and pasting on of the `fr` folder where you want to do your translation.

  1. Translate the files without touching the structure used.

  1. Once the work is well advanced, or even finished, send it to the author of `tnscore`.


> The documentation will necessarily be licensed under a *"Creative Commons - Attribution - Non-Commercial - Share Alike 4.0 International"* license.


Update one translation
----------------------

If you wish to update a translation proposal, you should quickly indicate in English the changes made and date them (no need to go into too much detail).


Regular users of `GitHub`
------------------------

It is possible to use `git merge requests` to indicate one contribution.
