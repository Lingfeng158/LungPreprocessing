# LungPreprocess
A series of operations on raw lung data ensuring data quality.   
Created by Lingfeng Li  
Email: lingfeng.li@vanderbilt.edu  
Last edit:  31/07/2019.

## Step 1
If data come in as DICOM format, ensure that DICOM files are complete and data is valid (containing a full lung). Then convert DICOM data to Nifti. Initial QA tool is created by Riqiang Gao, link is [HERE](https://github.com/MASILab/QA_tool). A composite tool developed based on Riqiang's QA tool is included, and it needs to be used in conjunction with the original tool. For fast processing, the composite tool can be wrapped differently to accommodate different data structure. 

## Step 2
Segment lung from initial lung data.   
Accept Nifti files and process them to only includes lung for machine learning. Initial code is developed by Fangzhi Liao [HERE](https://github.com/lfz/DSB2017). An optimized version is included in DSBM folder and [HERE](https://github.com/MASILab/DSB2017), with bug fixes allowing higher success rate with uninterrupted processing even after encountered error. Dependency requirements are the same as original LFZ's DSB code. DSBBatch.py is a wrapper around DSBM, and allow for more convenient data processing with more complex data structure. It can be easily modified to suit different structures.

### NOTICE
At ```binarize_per_slice``` function of DSB at ```/preprocessing/step1.py```, change intensity threshold to achieve desired behavior for different lung images. The threshold should not exceed -200, as such value will lead to bad image quality and should not be lower than -800, for such value whil give too much details for creating masks. Higher value (-300 - -600) helps ignore artifact, thus is recommended.

## Step 2 Alternative
Register one subject's lung data longitudinally with reference data (usually with high resolution and uses as benchmark).  
Two options:  
* FLIRT: set up FSL environment and use FLIRT tool.   
Command example:
```
flirt -in invol -ref refvol -out outvol -dof 6
```
* ANTs: set up ANTs environment and use SyNQuick. Read this [artical](https://github.com/ANTsX/ANTs/wiki/Anatomy-of-an-antsRegistration-call) for full command explanation.   
Read ```antsRegisterationSynQuick.sh``` and set "initial-moving-transform" to 0 for IMRT data. For other siturations, try different options under "initial-moving-transform" for desired results.  
For faster registeration add```-t a```or ```-t r```after the command.  
Command example:
```
antsRegistrationSyNQuick.sh -d 3 -f path-to-ref -m path-to-mov -o output-prefix
```
