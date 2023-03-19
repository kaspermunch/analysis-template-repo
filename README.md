## Repo structure

Either use as library repo with with `<package_name>` and `docs` (and maybe `notebook`) dirs. Or as data analysis repo with `scripts`, `notebooks`, `data`, `steps`, `results`, `figures`dirs.

## Conda environment

Create empty environment:

```
conda create -n <name>
```

Activate environment
```
conda activate <name>
```

Add channels first to make the appear in the exported environment:
Add any channels first to make the appear in the exported environment (you can always add more later):
```
conda config --env --append channels conda-forge
conda config --env --append channels bioconda
conda config --env --append channels etetoolkit
conda config --env --append channels gwforg
conda config --env --append channels kaspermunch
```

Install a subset of packages:
```
conda install jupyterlab pandas seaborn ...
conda install gwf jupyterlab pandas seaborn ipympl statsmodels bioconda pyfaidx tskit ete3 scikit-allel samtools bamtools vcftools
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

# Using submodules with Git

Read on [here](https://gist.github.com/kaspermunch/1131f20216648bd55bb20f6b35e69252)