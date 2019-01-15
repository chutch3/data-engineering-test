# Data Engineering Test

This repository contains a simple test for data engineering candidates.

The task is to transform a [poorly formatted TSV file](hhttps://github.com/humana-dec/data-engineering-test/blob/master/data/data.tsv)
into a properly formatted, machine-readable TSV file. If you clicked on the link above you may notice that GitHub complains about
errors in the file. The file does not explicitly adhere to the TSV format, so just as GitHub cannot accurately parse the file,
neither can our [Hadoop](https://hadoop.apache.org/), [Pig](https://pig.apache.org/), or data warehouse utilities.

### Instructions

Your task is to write a simple script to transform [data.tsv](https://github.com/humana-dec/data-engineering-test/blob/master/data/data.tsv)
into a properly formatted tab-separated values (TSV) file that can be read by any standard CSV/TSV parser. The resulting file should have the
following properties:

* Each row contains the same number of fields
* Fields are separated by tabs `\t`
* Fields that contain reserved characters (e.g. `\t`, `\r`, `\n`) are quoted *(hint hint)*
* The file is UTF-8 encoded (`data.tsv` is UTF-16LE encoded)

Scripts can be written in *any language and use any tools* with which the candidate is familiar. The solution does *not*
need to be generic enough to apply to similar issues in other files; your algorithm can be designed specifically for this
data set. Extra points are awarded for resource-efficient and scalable solutions.

To take the test, please complete the following steps:

1. Fork this repository
2. Write a script in the language of your choice to convert [data/data.tsv](https://github.com/humana-dec/data-engineering-test/blob/master/data/data.tsv)
  into a standard CSV parseable file, adhering to guidelines in the previous section
3. Commit the script to the root directory of the repository
4. Submit a pull request to this repository.

### Bonus (optional)

For bonus points, ambitious candidates can parallelize their algorithm. A parallelizable implementation will
have the following properties:

* Given an arbitrary byte `position` and `length`, the algorithm cleans a portion of the full data set and produces
  a unique TSV output file
* Concatenating the outputs of multiple processes should result in a well-formed TSV file containing no duplicates

*It's important to note that the arbitrary `position` may not necessarily be the start of a new line.*
