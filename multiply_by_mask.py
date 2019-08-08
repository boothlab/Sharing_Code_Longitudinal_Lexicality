#Uses transormed mask to deface raw images and saves defaced data
#conceptual idea and lines 13-18 from pydeface's __main__.py
#https://github.com/poldracklab/pydeface
#08/2018

import sys
from nibabel import load, Nifti1Image

subject = sys.argv[1]
session = sys.argv[2]

# multiply defacing mask by raw image and save
infile = "sub-" + subject + "_ses-T" + session + "_T1w.nii"
infile_img = load(infile)
tmpfile_img = load("invertmask.nii")
outdata = infile_img.get_data().squeeze() * tmpfile_img.get_data()  
outfile_img = Nifti1Image(outdata, infile_img.get_affine(),
                              infile_img.get_header())
outfile_img.to_filename("defaced.nii")
