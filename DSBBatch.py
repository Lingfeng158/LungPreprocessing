#path to unprocessed data structure
rootpath='/home/local/VANDERBILT/lil18/Desktop/QA_tool/output2'
#path of desired output directory
output='/home/local/VANDERBILT/lil18/Desktop/out'
"""
Original DSB code works with a root data path with flat subfolders that contains nifti files.
This is a wrapper that allows more complex data structures.
It is currently set to process multiple "root data paths" at the same time.
Can be modified easily to accommodate different data structures.
"""


import os
import nibabel as nib
import sys
#modify to path of DSB folder w.r.t this file
#or use hard path from root
sys.path.insert(0, './DSBM')
from preprocessing import full_prep

import torch
from torch.nn import DataParallel
from torch.backends import cudnn
from torch.utils.data import DataLoader
from torch import optim
from torch.autograd import Variable

from layers import acc
from data_detector import DataBowl3Detector,collate
from data_classifier import DataBowl3Classifier

from utils import *
from split_combine import SplitComb
from test_detect import test_detect
from importlib import import_module
import pandas

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
def QAPreprocess(datapath, preprocess_result_path, bbox_result_path):
    outputfile='prediction.csv'

    detector_model= 'net_detector'
    detector_param='DSBM/model/detector.ckpt'
    classifier_model='net_classifier'
    classifier_param= 'DSBM/model/classifier.ckpt'
    n_gpu= 1
    n_worker_preprocessing= 8
    use_exsiting_preprocessing= False
    skip_preprocessing= False
    skip_detect= True
    datapath = datapath
    prep_result_path = preprocess_result_path
    skip_prep = skip_preprocessing
    skip_detect = skip_detect

    if not skip_prep:
        #print ('the prep index from ', config_submit['prep_min'], ' to ', config_submit['prep_max'])
        testsplit = full_prep(datapath,prep_result_path, 
                              n_worker = n_worker_preprocessing,
                              use_existing=use_exsiting_preprocessing)
    else:
        testsplit = os.listdir(datapath)
    """
    #print type(detector_param)
    nodmodel = import_module(detector_model.split('.py')[0])
    config1, nod_net, loss, get_pbb = nodmodel.get_model()
    checkpoint = torch.load(detector_param)
    nod_net.load_state_dict(checkpoint['state_dict'])

    torch.cuda.set_device(0)
    nod_net = nod_net.cuda()
    cudnn.benchmark = True
    nod_net = DataParallel(nod_net)

    bbox_result_path = bbox_result_path
    if not os.path.exists(bbox_result_path):
        os.mkdir(bbox_result_path)
    if not skip_detect:
        margin = 32
        sidelen = 144
        config1['datadir'] = prep_result_path
        split_comber = SplitComb(sidelen,config1['max_stride'],config1['stride'],margin,pad_value= config1['pad_value'])

        dataset = DataBowl3Detector(testsplit,config1,phase='test',split_comber=split_comber)
        test_loader = DataLoader(dataset,batch_size = 1,
            shuffle = False,num_workers = 2,pin_memory=False,collate_fn =collate)

        test_detect(test_loader, nod_net, get_pbb, bbox_result_path,config1,n_gpu=n_gpu)
    #testsplit = [f.split('_clean')[0] for f in os.listdir(prep_result_path) if '_clean' in f]
    """


mkdir(output)
dirlist=os.listdir(rootpath)   
for i in dirlist:
    #Selection rule
    if True:
        dirPath=os.path.join(rootpath,i)
	#create output path for each folder as well for organization
        outputPath=os.path.join(output,i)
        mkdir(outputPath)
        #dirPath=os.path.join(dirPath,os.listdir(dirPath)[0])
        #outputPath=os.path.join(outputPath,os.listdir(dirPath)[0])
        #mkdir(outputPath)
        #currently dirPath is the input path for Kaggle's preprocessing
        datapath=dirPath
        print (outputPath)
        preprocess_result_path=outputPath
        bbox_result_path=outputPath
        QAPreprocess(datapath, preprocess_result_path, bbox_result_path)
