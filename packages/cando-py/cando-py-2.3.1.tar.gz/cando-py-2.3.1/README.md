
[![Build Status](https://travis-ci.com/ram-compbio/CANDO.svg?branch=master)](https://travis-ci.com/ram-compbio/CANDO)
[![codecov](https://codecov.io/gh/ram-compbio/CANDO/branch/master/graph/badge.svg)](https://codecov.io/gh/ram-compbio/CANDO)
[![Anaconda-Server Badge](https://anaconda.org/ram-compbio/cando/badges/version.svg)](https://anaconda.org/ram-compbio/cando)
[![Anaconda-Server Badge](https://anaconda.org/ram-compbio/cando/badges/license.svg)](https://anaconda.org/ram-compbio/cando)
[![Anaconda-Server Badge](https://anaconda.org/ram-compbio/cando/badges/downloads.svg)](https://anaconda.org/ram-compbio/cando)

# CANDO

Computational Analysis of Novel Drug Opportunities

---

## Background

CANDO is a unique computational drug discovery, design, and repurposing platform that analyses drug interactions on a proteomic scale, adhering to the multitarget drug theory, for the purposes of shotgun drug discovery and repurposing, i.e., to evaluate every drug for every disease. [1-13]

The platform relates small molecules based on their computed interactions with all protein structures, known as an interaction signature with the hypothesis being drugs with similar interaction signatures will have similar behavior in biological systems and will therefore be useful against the same indications.


## Install

You may download the source code via the releases or cloning the git repository. However, we suggest using pip or anaconda to install the CANDO package, as this is the easiest and quickest way to start using our platform! 


### Pip

`pip install cando-py`


### Anaconda

The CANDO package relies on multiple "conda-forge" dependencies. Therefore, we require that you add "conda-forge" to your anaconda channels: 

`conda config --add channels conda-forge`

Create a new conda environment if one for does not already exist for CANDO:

`conda create -n cando python==3.7 `

Activate the new environment:

`conda activate cando`

Then you can install CANDO using the following command:

`conda install -c ram-compbio cando`


## Tutorial

There is a CANDO tutorial available as a Jupyter notebook.
This notebook can be found [here](https://github.com/ram-compbio/CANDO/blob/master/CANDO_tutorial.ipynb) in this repo.

It can also be downloaded from anaconda:

`anaconda download ram-compbio/CANDO_tutorial`


## Documentation

CANDO API can be found [here](https://github.com/ram-compbio/CANDO/blob/master/docs)


## Test

You can test your install by running our script:

[run_test.py](https://github.com/ram-compbio/CANDO/blob/master/run_test.py)


## References
1. Mangione W, Falls Z, Chopra G, Samudrala R. (2020) cando.py: Open Source Software for Predictive Bioanalytics of Large Scale Drug-Protein-Disease Data. Journal of chemical information and modeling (Sep), 60(9): 4131-4136. doi:10.1021/acs.jcim.0c00110
2. Mangione W, Falls Z, Melendy T, Chopra G, Samudrala R. (2020) Shotgun drug repurposing biotechnology to tackle epidemics and pandemics. Drug discovery today (Jul), 25(7): 1126-1128. doi:10.1016/j.drudis.2020.05.002
3. Schuler J, Falls Z, Mangione W, Hudson ML, Bruggemann L, Samudrala R. (2022) Evaluating the performance of drug-repurposing technologies. Drug discovery today (Jan), 27(1): 49-64.
4. Overhoff B, Falls Z, Mangione W, Samudrala R. (2021) A Deep-Learning Proteomic-Scale Approach for Drug Design. Pharmaceuticals (Basel, Switzerland) (Dec), 14(12). doi:10.3390/ph14121277
5. Fine J, Lackner R, Samudrala R, Chopra G. Computational chemoproteomics to understand the role of selected psychoactives in treating mental health indications. Scientific Reports 9, 1315, 2019.
6. Schuler J, Samudrala R. Fingerprinting CANDO: Increased accuracy with structure and ligand based shotgun drug repurposing. ACS Omega 4: 17393-17403, 2019.
7. Falls Z, Mangione W, Schuler J, Samudrala R. Exploration of interaction scoring criteria in the CANDO platform. BMC Research Notes 12: 318, 2019.
8. Mangione W, Samudrala R. Identifying protein features responsible for improved drug repurposing accuracies using the CANDO platform: Implications for drug design. Molecules 24: 167, 2019.
9. Chopra G, Samudrala R. Exploring polypharmacology in drug discovery and repurposing using the CANDO platform. Current Pharmaceutical Design 22: 3109-3123 2016.
10. Sethi G, Chopra G, Samudrala R. Multiscale modelling of relationships between protein classes and drug behavior across all diseases using the CANDO platform. Mini Reviews in Medicinal Chemistry 15: 705-717, 2015.
11. Minie M, Chopra G, Sethi G, Horst J, White G, Roy A, Hatti K, Samudrala R. CANDO and the infinite drug discovery frontier. Drug Discovery Today 19: 1353-1363, 2014.
12. Horst JA, Laurenzi A, Bernard B, Samudrala R. Computational multitarget drug discovery. Polypharmacology 263-301, 2012.
13. Jenwitheesuk E, Horst JA, Rivas K, Van Voorhis WC, Samudrala R. Novel paradigms for drug discovery: Computational multitarget screening. Trends in Pharmacological Sciences 29: 62-71, 2008.
