# DataScience Data Engineering Test

This repository contains a simple test for data engineering candidates at [DataScience](http://datascience.com).

This test comes from a recent real-world experience working on client data sets at DataScience.
The test is to transform a [poorly formatted TSV file](https://github.com/connecthq/data-engineering-test/blob/master/data/data.tsv)
into a properly formatted, machine-readable TSV file. You may notice that GitHub complains about errors in the file.
The file does not explicitly adhere to the TSV format, so just as GitHub cannot accurately parse the file, neither can
our [Hadoop](https://pig.apache.org/), [Pig](https://pig.apache.org/), or data warehouse utilities.

Your task is to write a simple script to transform [data/data.tsv](https://github.com/connecthq/data-engineering-test/blob/master/data/data.tsv)
into a properly formatted TSV file that can be read by any standard CSV parser. The resulting file should have the following properties:
* Each row contains the same number of fields
* Fields that contain reserved characters (e.g. `\t`, `\r`, `\n`) are quoted *(hint hint)*
* The file is UTF-8 encoded (`data/data.tsv` is UTF-16LE encoded)

Scripts can be written in *any language and use any tools* with which the candidate is familiar. The solution does *not*
need to be generic enough to apply to similar issues in other files; your algorithm can be designed specifically for this
data set. Extra points are awarded for efficient and scalable solutions.

### Bonus (optional)

For bonus points, ambitious candidates can parallelize their algorithm. A parallelizable implementation will
have the following properties:
* Given an arbitrary position and length, the algorithm cleans a portion of the full data set
* Given aligned positions and lengths (e.g. `0/500`, `501/500`, `1001/500`) multiple processes will produce
  correctly aligned output. For example, if process `1` given the input `position=0;length=500` processes
  rows `1-10`, then process `2` given the input `position=501;length=500` should process rows starting at `11`

To take the test, please complete the following steps:
1. Fork this repository
2. Write a script in the language of your choice to convert [data/data.tsv](https://github.com/connecthq/data-engineering-test/blob/master/data/data.tsv)
  into a standard CSV parseable file, adhering to guidelines in the previous section
3. Commit the script to the root directory of the repository
4. Submit a pull request to this repository or, if you value your privacy, email an archive to [colin@datascience.com](mailto:colin@datascience.com)
