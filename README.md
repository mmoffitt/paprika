paprika
=======

Paprika provides utilities to index, search, and organize PDFs by reading and writing metadata. It is specifically aimed at supporting large collections of research papers.

Introduction
------------

Whether you are a tenured academic or an industrial research scientist, it is likely that you have amassed hundreds (if not thousands) of research papers over the years. The task of organizing and searching these documents becomes a burden, especially if you aim to synchronize certain subsets of this collection with a tablet-friendly cloud-enabled filesystem (e.g., Dropbox).

Paprika is designed to help organize large collections of PDFs. You can think of it as a command-line 'iTunes-like' interface to your corpus of knowledge. It allows you to store documents in nearly any directory structure you like, and serves to maintain and manipulate document metadata (even in bulk) to make your literature search friction-free.

Getting Started
---------------

First, clone this repository to get the paprika.py python script. Put this a directory above of all your papers. You may use any directory structure you wish, although we recommend something similar to the following if you wish to scale to tens of thousands of papers.

    LIBRARY/                    Your entire library
        paprika.py              The paprika script
        Papers/                 All of your papers
            AAAI/               A folder for each of conference / journal in your collection
            DAC/
            ICCAD/
            IJCAI/
                2011/           Each subfolder can be a year of publication
                2012/
                2013/
                    [IJCAI 2013] Search Strategies for Optimal Multi-Way Number Partitioning.pdf
                    [IJCAI 2013] Semiring-Based Mini-Bucket Partitioning Schemes.pdf
                    [IJCAI 2013] Subset Selection of Search Heuristics.pdf
                    ...

You'll also want to install [PDFtk](http://www.pdflabs.com/tools/pdftk-server/) so that Paprika can read/write metadata in later steps.

Building the Index
------------------

Once you have aggregated your PDFs as specified above, you need only run the paprika script to build an index of your document metadata:

    ./paprika.py

This will iterate through every PDF underneath Papers/ to collect the metadata for each. The results are written into a comma-delimited ASCII file (Files/Papers.csv). Whenever you subsequently add or delete PDFs, simply run the paprika script again ... it will refresh metadata only for new files (based on timestamp) so that subsequent passes are lightning fast.

If for some reason you delete Files/Papers.csv, that's fine - it can rebuilt from scratch at any time, albeit slowly.

Updating Metadata
-----------------

Few very PDFs (even those that come from reputable sources like IEEE and ACM) are appropriately labelled with metadata. Fortunately, you can update the metadata for several documents (in bulk!) using Paprika.  Simply open the Files/Papers.csv file in your favorite spreadsheet program (e.g., Microsoft Excel) and you'll see entries like the following:

| File                                           | Modified | Title       | Subject | Author             | Keywords |
| ---------------------------------------------- | -------- | ----------- | ------- | ------------------ | -------- |
| [AAAI 2013] Concurrent Inference Graphs.pdf    | 3/14/15  | paper.dvi   | unknown | Dan                |          |
| [AAAI 2013] Tools for Preference Reasoning.pdf | 3/14/15  | garbage.pdf | N/A     | Microsoft User     |          |

Many of the above fields contain erroneous data. If you wish to search / export documents by these fields (as described in later sections), you can modify the data as follows:

| File                                           | Modified | Title                           | Subject   | Author             | Keywords |
| ---------------------------------------------- | -------- | ------------------------------- | --------- | ------------------ | -------- |
| [AAAI 2013] Concurrent Inference Graphs.pdf    | updated  | Concurrent Inference Graphs     | AAAI 2013 | Daniel R. Schlegel | graphs   |
| [AAAI 2013] Tools for Preference Reasoning.pdf | updated  | Tools for Preference Reasoning  | AAAI 2013 | Ying Zhu           | pref     |

Paprika will take note of any row where the _Modified_ date has been replaced by the word *updated*, and will write the new metadata *into the PDF itself* (iTunes does the same thing whenever you modify a song name / title). This way, you are free to delete the index at any time, as all the important data is self-contained in your raw PDFs.

If you intend on modifying the metadata for hundreds of documents, you may wish to use [DBLP](http://dblp.uni-trier.de/db/) to get the author and title information. This can be imported into Excel with relatively little grunt work, and copied into the appropriate columns.

Renaming Documents
------------------

(TODO)

Exporting Subsets of Documents
------------------------------

The biggest benefit of building the metadata index is that documents can be easily retrieved by title / author / subject / keywords. One option is to manually search the index for PDFs that match your requirements. This tends to be tedious, and 

The preferred way is to export documents of interest _a_ _priori_, so that at "read time" you are free to browse relevant PDFs in your collection. To do this, first create empty folders within three directories: Authors/, Topics/, and Subjects/. The struture will look as follows:

    LIBRARY/                    Your entire library
        paprika.py              The paprika script
        Papers/                 All of your papers
        Authors/                Names of authors you want to follow
            Michael D. Moffitt/ (Initially) empty folder
            Richard E. Korf/    (Initially) empty folder
        Keywords/               Tags for keywords or topics that interest you
            cgra/               (Initially) empty folder
            llvm/               (Initially) empty folder
        Subjects/               Names of your favorite conferences or journals
            ICAPS 2011/         (Initially) empty folder
            IJCAI 2013/         (Initially) empty folder

Then, run the the following command to create symbolic links from documents in the Papers/ directory to matching folders.

    ./paprika.py --export

The symlinks are tiny, so very little disk space is consumed in this process. You can then use another program (e.g., rsync) to synchonize the documents with DropBox or any other filesystem.

Tips on Obtaining Documents
---------------------------

(TODO)

