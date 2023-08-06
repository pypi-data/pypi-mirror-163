# SolvBERT

#### Description
This is the code for "SolvBERT for solvation free energy and solubility prediction: a demonstration of an NLP model for predicting the properties of molecular complexes" paper. The preprint of this paper can be found in ChemRxiv with https://doi.org/10.26434/chemrxiv-2022-0hl5p

#### Installation

1.  python 3.7.12
2.  transformers 2.11.0
3.  wandb 0.12.15
4.  tokenizers 0.7.0

use　`pip install solv-bert==0.0.3` install this package
#### Dataset

Solvation-QM. The Solvation-QM dataset originally came from a study by Vermeire et al. who computed the dataset using a commercial software called COSMOtherm. The dataset consists of 1 million data points randomly selected from all possible combinations of 284 commonly used solvents and 11,02914 solutes. 
Solvation-Exp. experimental solvent free energy data for 8,780 different solute and solvents combinations from Vermeire et al. 
Solubility. The Solubility dataset was originally from Boobier et al. It was curated from the Open Notebook Science Challenges water solubility dataset and the Reaxys database. This dataset includes ethanol with 695 solutes, benzene with 464 solutes, acetone with 452 solutes, and water with 900 solutes, for a total of 2,511 different combinations, with solubility expressed as log S.

#### Train

Model use the SMILES language model.py to train and the finetune.py to fine-tune.

#### Test

Model use the predict and evaluate.py to shart testing.


