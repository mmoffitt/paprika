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
            AAAI/               A folder for each conference / journal to which you frequently submit papers.
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

(TODO: Talk about the PDFtk binaries)

Building the Index
------------------

Once you have aggregated your PDFs as specified above, you need only run the paprika script to build an index of your document metadata:

    ./paprika.py

This will iterate through every PDF underneath Papers/ to collect the metadata for each. The results are written into a comma-delimited ASCII file (Files/Papers.csv). Whenever you subsequently add or delete PDFs, simply run the paprika script again ... it will refresh metadata only for new files (based on timestamp) so that subsequent passes are lightning fast.

If for some reason you delete Files/Papers.csv, that's fine - it can rebuilt from scratch at any time, albeit slowly.

Updating Metadata
-----------------

Few very PDFs (even those that come from reputable sources like IEEE and ACM) are appropriately labelled with metadata. Fortunately, you can update the metadata for several documents (in bulk!) using Paprika.  Simply open the Files/Papers.csv file in your favorite spreadsheet program (e.g., Microsoft Excel) and you'll see entries like the following:

Renaming Documents
------------------

(TODO)

Exporting Subsets of Documents
------------------------------

(TODO)

Tips on Obtaining Documents
---------------------------

(TODO)

