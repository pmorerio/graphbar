# graphBAR

## Setting up the environment
```
conda create -n pose_selector python=3.8
conda activate pose_selector
``` 
Install requirements
```
pip install -r requirements.txt
conda install -c openbabel openbabel=2.4.1
```


## Protocols

1. Retrive the PDBbind database ver.2016 from http://www.pdbbind.org.cn/ and extract the files into folder "database/" 
(database/general-set-except-refined, database/refined-set)

2. Prepare pockets with UCSF Chimera.
```
bash chimera_process.sh
```

3. Prepare PDBbind2016 general-set, refined-set, core-set and PDBbind2013 core-set. Prepared database will be saved in "data/" directory. 
("general_adj1.npy" for general-set adjacency matrix data for 1 adjacency matrix model, ..., "general_feat.npy" for general-set feature matrix data, "general_label.npy" for general-set true-label data)
```
python pdbbind_data.py
```

4. Docking results are compressed and splited in "data/" directory. You should join files to one tar.gz file and extract it.
```
cd data/
cat docking.parta* > docking.tar.gz
tar -xzvf docking.tar.gz
cd ..
```
If you prepared your own docking results, replace them into "data/docking/" directory, and split the result into multiple single pdbqt file for each structure in its pdb-name-directory(ex. "docking/8gpb/8gpb_0.pdbqt", "docking/8gpb/8gpb_1.pdbqt", ...). If you use "split_output.py" in "data/docking/" directory, it will make "docking_dict.pickle" file(docking results which passed filtering). Move the file to main directory for dataset2 and dataset4.

5. Build dataset using "split_dataset1.py", "split_dataset2.py", "split_dataset3.py", and "split_dataset4.py". This process will generate datasets from PDBbind general-set and refined-set. The 'NUMBER_OF_VALIDATION_SET' should be aranged based on PDBbind data without docking data augmentation.
```
python split_dataset1.py -i INPUT_PATH -o OUTPUT_PATH -s NUMBER_OF_VALIDATION_SET
python split_dataset2.py -i INPUT_PATH -o OUTPUT_PATH -s NUMBER_OF_VALIDATION_SET
python split_dataset3.py -i INPUT_PATH -o OUTPUT_PATH -s NUMBER_OF_VALIDATION_SET
python split_dataset4.py -i INPUT_PATH -o OUTPUT_PATH -s NUMBER_OF_VALIDATION_SET
```

Example:
```
mkdir data/set1
python split_dataset1.py -i data -o data/set1 -s 369
```

6. Training and test the data.
```
python training.py -s DATA_PATH(output path of split_dataset file) -at ADJ_TYPE(float, 1, 2, 4, 8) -o OUTPUT_PATH -t TESTSET(core, core2013) -gpu CUDA_VISIBLE_DEVICES
```

Example:
```
python training.py -s data/set1 -at 2 -gpu 0 -o results/set1/adj2 -t core
```

7. You can analyse the outputs.
```
python analysis.py OUTPUT_PATH ADJ_TYPE TESTSET
```
Example:
```
python analysis.py results/set1/adj2 2 core
```

Time analysis
```
python3 time_analysis.py OUTPUT_PATH ADJ_TYPE TESTSET
```

Example:
```
python time_analysis.py results/set1/adj2 2 core
```

8. (optional) If you want to analyse original data of paper, you can use "analysis_set.py" or "time_analysis_set.py".
```
python analysis_set.py DATASET(set1, set2, set3, set4) MODEL_NAME(adjfloat_01, ..., adj8_05) RESULT_NAME
```
Example:
```
python analysis_set.py set4 adj2_05 set4-2-core
```

Time analysis
```
python3 time_analysis.set.py DATASET(set1, set2, set3, set4) MODEL_NAME(adjfloat_01, ..., adj8_05) RESULT_NAME
```

Example:
```
python time_analysis_set.py set4 adj2_05 set4-2-core
```

If you have any problem to process, please contact json@kaist.ac.kr.
