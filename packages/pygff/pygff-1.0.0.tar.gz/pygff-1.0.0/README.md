# PyGFF
---
A Python package to read and write Grace Format Files (*.gff*).

## Easiest way to install PyGFF:
`pip install pygff`

## Basic usage:
1. Loading a *.gff* file:
	```
	from pygff import load
	data = load('image.gff')
	```
2. Saving a numpy array `np_arr` as a *.gff* file:
	```
	from pygff import GFF, save
	save('image.gff', GFF(np_arr))
	```

## What is GFF?
GFF is an open source file format for multimodal biomedical images. The format supports datasets with up to five dimensions (three spatial dimensions, time-variant, and multi-channel) and a rich set of metadata key-value pairs. By default, the implementation uses a lossless compression algorithm to reduce file size and cryptographic hashing for secure writing. Multithreading is also used if possible to speed up reading and writing of *.gff* files.

The PyGFF package is developed by [Gremse-IT GmbH](https://gremse-it.com/) (Aachen, Germany) as a Python interface for [Imalytics Preclinical 3.0](https://gremse-it.com/imalytics-preclinical/) which utilizes *.gff* by default for underlay, overlay, segmentation, and project files. 

For more details, please check out this publication:

> Yamoah, Grace Gyamfuah et al. “Data Curation for Preclinical and Clinical Multimodal Imaging Studies.” 
> Molecular imaging and biology vol. 21,6 (2019): 1034-1043. doi:10.1007/s11307-019-01339-0

Full text: https://pubmed.ncbi.nlm.nih.gov/30868426/

## How to build the package yourself:
1. Clone the repository: `git clone git@bitbucket.org:felixgremse/gff_file_format.git`
2. Make sure you have the Python build package installed: `py -m pip install --upgrade build`
3. Then, install `pygff` in editable mode using: `py -m pip install -e .`	

## Examples:
Example notebooks can be found in the `/examples/` directory of the repository. They are not included with the PyGFF package. We recommed that you to start with `01_load_and_save.ipynb` to learn more about loading, saving, and GFF objects. More tutorials will be added in the future.

Running the examples requires the packages `jupyter`, `matplotlib`, `numpy`, and `scipy` to be installed. Also, please download the required example datasets if you have not cloned the repository yet.

## How to run package tests:
1. Go to the `./test/` directory and simply run `pytest`

## License:
The PyGFF package is licensed under the terms of the [MIT license](https://opensource.org/licenses/MIT).

All *.gff* files and Jupyter notebooks contained in the `/examples/` directory of the repository are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).