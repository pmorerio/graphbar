from ast import Raise
import csv
import os
import pybel

dataset_dir = '/home/pmorerio/datasets/dompe_pose_selection'
data = []
labels = []

with open(os.path.join(dataset_dir,'POSESdataset_descr.csv'), 'r') as csvfile:
    csv_data = csv.DictReader(csvfile) 
    print(csv_data.fieldnames)
    for i, row in enumerate(csv_data): # row is an OrderdDict
        if row['split'] == 'dup': pass

        folder = row['rowID'].split('_')[0]+'_'+row['rowID'].split('_')[1]
        folder = os.path.join(dataset_dir,"poses",folder)
        
        try:
            # read each pose in the ALLposes.mol2 file
            pose_ligand = next(pybel.readfile('mol2',os.path.join(folder,'DSCORE_new','ALLposes.mol2')))
        except StopIteration as err:
            continue
        
        labels.append(row['rmsd'])

        ## prepare data
        # ....
        data.append(pose_ligand)
        print(row['rowID'])
        

        if len(labels) == 1060: break

assert len(data) == len(labels)


# import or adapt?
# adapt from utils.py
def get_atoms(ligand, pocket):
    p_atoms = [[atom.atomicnum, atom.coords, atom.hyb, atom.heavyvalence, atom.heterovalence, atom.partialcharge, 1] for atom in pocket if not atom.OBAtom.GetAtomicNum()==1]
    l_atoms = [[atom.atomicnum, atom.coords, atom.hyb, atom.heavyvalence, atom.heterovalence, atom.partialcharge, 0] for atom in ligand if not atom.OBAtom.GetAtomicNum()==1]
    c_atoms = [l_atom for l_atom in l_atoms]
    for p_atom in p_atoms:
        for l_atom in l_atoms:
            distance = math.sqrt((p_atom[1][0]-l_atom[1][0])**2 + (p_atom[1][1]-l_atom[1][1])**2 + (p_atom[1][2]-l_atom[1][2])**2)
            if distance <= 4:
                # pocket atoms within 4A from ligand
                c_atoms.append(p_atom)
                break
    return c_atoms