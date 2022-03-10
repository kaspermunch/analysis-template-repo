
## Conda environment

Add channels first to make the appear in the exported environment:
Add any channels first to make the appear in the exported environment (you can always add more later):
```
conda config --env --append channels conda-forge
conda config --env --append channels bioconda
conda config --env --append channels etetoolkit
conda config --env --append channels gwforg
conda config --env --append channels kaspermunch
```

Create environment:
Create environment with subset of packages:
```
conda create -n <name> jupyterlab pandas seaborn ...
conda create -n <name> gwf jupyterlab pandas seaborn ipympl statsmodels bioconda pyfaidx tskit ete3 scikit-allel samtools bamtools vcftools
```

Export it to the binder folder:
```
conda env export --from-history > binder/environment.yml
```

List revisions to envirionment:
```
conda list --revisions
```

Restore a past revision:
```
conda install --revision 2
```

Once you land on stable environment this can make it more stable:

```
conda env export --from-history > binder/environment.yml
conda deactivate <name>
conda env remove -n <name>
conda env create -n <name> -f binder/environment.yml
```

## Create PyPi and Conda packages

```
conda install conda-build twine anaconda-client
```

```
bash pypi.sh
```

```
bash conda.sh [-c channel -c channel ...]
```