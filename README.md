# ChangeProneness

## Usage

At the lowest level, calc_diff is used to take in two files and output a decimal where 0.0 means the files are practically identical and 1.0 means they are completely different.

folder_compare analyzes two folders for file differences. It returns a dictionary where the keys are filenames found in both folders of the specified filetype and the values are the corresponding decimals calculated by calc_diff. It also returns a list files that are in one folder but not the other.

version_compare is used to look at two versions of a directory of code and output each file that was added, removed, or modified (with the percent of change) from the first directory to the second.

system_compare runs version compare on multiple versions in a row and outputs into a single CSV file.
