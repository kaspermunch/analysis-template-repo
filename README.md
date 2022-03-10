# Template repository


# Conda environment

Add channels first to make the appear in the exported environment:
```
conda config --env --append channels conda-forge
conda config --env --append channels bioconda
conda config --env --append channels kaspermunch
```

Create environment:
```
conda create -n <name> jupyterlab pandas seaborn ...
```

Export it to the binder folder:
```
conda env export > binder/environment.yml
```


## pypi and conda

```
bash pypi.sh
```

```
bash conda.sh [-c channel -c channel ...]
```
