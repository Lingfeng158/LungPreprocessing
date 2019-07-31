# LungPreprocess
A series of operation on raw lung data ensuring data quality.

## Step 1
If data come in as DICOM format, ensure that DICOM files are complete and data is valid (containing a full lung). Then convert DICOM data to Nifti. Initial QA tool is created by Riqiang, link is [HERE](https://github.com/MASILab/QA_tool). A composite tool developed based on Riqiang's QA tool is included. For fast processing, the composite tool can be wrapped differently to accommodate different data structure. 

## Step 2
Segment lung from initial lung data.   
Accept Nifti files and process them to only includes lung for machine learning. Initial code is developed by Fangzhi Liao [HERE](https://github.com/lfz/DSB2017). An optimized version is included [HERE](https://github.com/MASILab/DSB2017), allowing higher success rate with uninterrupted processing even after encountered error. 

## Step 2 Alternative
Register one subject's lung data longitudinally with reference data (usually with high resolution and uses as benchmark).  
Two options:  
* FLIRT: set up FSL environment and use FLIRT tool.   
Command example:
'''
flirt -in invol -ref refvol -out outvol -dof 6
'''
* ANTs: set up ANTs environment and use SyNQuick. Read antsReisterationSynQuick.sh and this [artical](https://github.com/ANTsX/ANTs/wiki/Anatomy-of-an-antsRegistration-call) for full command explanation.   
Set "initial-moving-transform" to 0 for IMRT data; try different options under "initial-moving-transform" for desired results.  
For faster registeration add
'''
-t a
'''
or 
'''
-t r
'''
after the command.  
Command example:
'''
antsRegistrationSyNQuick.sh -d 3 -f path-to-ref -m path-to-mov -o output-prefix
'''
