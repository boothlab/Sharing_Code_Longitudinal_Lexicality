#!/bin/bash

#Defacing for mulitimodal longitudinal lexicality dataset
#08/2018

rootdir=#location of bids folder
datadir=${rootdir}/bids
tools=${rootdir}/defacing_tools


for n in {001..188}; do
     anatdir1=${datadir}/sub-${n}/ses-T1/anat/
     anatdir2=${datadir}/sub-${n}/ses-T2/anat/
     echo "working on subj ${n}"
     
     cp ${tools}/multipy_by_mask.py ${anatdir1}

     cd ${anatdir1}
     nifti_tool -mod_hdr -overwrite -mod_field slice_code '0' -infiles sub-${n}_ses-T1_T1w.nii
     mri_robust_register --mov sub-${n}_ses-T1_T1w.nii --dst ${tools}/MNI152_T1_1mm.nii.gz --lta tmp.lta --mapmov registered.nii --iscale --satit >> ${rootdir}/output_reading_deface
     mri_concatenate_lta -invert1 tmp.lta identity.nofile inverttmp.lta >> ${rootdir}/output_reading_deface
     mri_convert -at inverttmp.lta ${tools}/defacemask.nii invertmask.nii >> ${rootdir}/output_reading_deface
     python multiply_by_mask.py ${n} 1

   if [ -d ${anatdir2} ]; then
     cp ${tools}/multiply_by_mask.py ${anatdir2} 
     cd ${anatdir2}
     gunzip *T1w.nii.gz
     nifti_tool -mod_hdr -overwrite -mod_field slice_code '0' -infiles sub-${n}_ses-T2_T1w.nii 
     mri_robust_register --mov sub-${n}_ses-T2_T1w.nii --dst ${tools}/MNI152_T1_1mm.nii.gz --lta tmp.lta --mapmov registered.nii --iscale --satit >> ${rootdir}/output_reading_deface
     mri_concatenate_lta -invert1 tmp.lta identity.nofile inverttmp.lta >> ${rootdir}/output_reading_deface
     mri_convert -at inverttmp.lta ${tools}/defacemask.nii invertmask.nii >> ${rootdir}/output_reading_deface
     python multiply_by_mask.py ${n} 2
   fi  
     echo "completed subject ${n}!"
done

cd ${rootdir}
echo "All Done!"

