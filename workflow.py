# %% [markdown]
# ---
# title: GWF workflow
# execute:
#   eval: false
# ---
"""

Example workflow using mapping between intput and output of each target. 
It is made to show all the ways information may be passed through an workflow.

```plaintext
                        input_file1.txt                        input_file2.txt
                                                                                                                
file label:             'raw_path'                              'raw_path'                                
                            |                                       |                                  
                            |                                       |                         
template:               uppercase_names                         uppercase_names                         
                            |                                       |                          
                            |                                       |                         
file label:            'uppercased_path'                       'uppercased_path'                         
                            |                                       |                          
                            |                                       |                         
template:                divide_names                            divide_names                         
                         /          \                            /          \                          
                        /            \                          /            \                         
file label:    'filt_me_path'  'filt_other_path'      'filt_me_path'  'filt_other_path'                         
                        \           /                           \           /                         
                         \         /                             \         /                         
template:                 unique_names                            unique_names                         
                           |      |                                |      |  
                           |      |                                |      |  
file label:      'uniq_me_path'  'uniq_other_path'       'uniq_me_path'  'uniq_other_path'
                            \            \                        /           /
                             \            - - - - - - - - - - - / - - -     /  
                              \  / - - - - - - - -- - - - - - -         \  /
                               |                                          |                          
file label:     (collected) 'uniq_me_paths'              (collected) 'uniq_other_paths'                         
                               |                                          |
                               |                                          |
template:                   merge_names                                merge_names
                               |                                          |                          
                               |                                          |                          
file label:                'output_path'                              'output_path'                         
```

"""

###############################################################################

# %% [markdown]
"""
## Imports and utility functions:
"""

# %%
import os, re
from collections import defaultdict
from pathlib import Path
import pandas as pd

from gwf import Workflow, AnonymousTarget
from gwf.workflow import collect

# utility function
def modify_path(path, **kwargs):
    """
    Utility function for modifying file paths substituting
    the directory (dir), base name (base), or file suffix (suffix).
    """
    for key in ['dir', 'base', 'suffix']:
        kwargs.setdefault(key, None)
    assert len(kwargs) == 3

    par, name = os.path.split(path)
    name_no_suffix, suf = os.path.splitext(name)
    if type(kwargs['suffix']) is str:
        suf = kwargs['suffix']
    if kwargs['dir'] is not None:
        par = kwargs['dir']
    if kwargs['base'] is not None:
        name_no_suffix = kwargs['base']

    new_path = os.path.join(par, name_no_suffix + suf)
    if type(kwargs['suffix']) is tuple:
        assert len(kwargs['suffix']) == 2
        new_path, nsubs = re.subn(r'{}$'.format(kwargs['suffix'][0]), kwargs['suffix'][1], new_path)
        assert nsubs == 1, nsubs
    return new_path


###############################################################################
# %% [markdown]
"""
## Template functions:
"""
# %%

# task template function
def uppercase_names(raw_path): 
    """
    Formats names to uppercase.
    """
    # dir for files produces by task
    output_dir = 'steps/upper_cased'
    # path of output file
    uppercased_path = modify_path(raw_path, dir=output_dir, suffix='_uppercased.txt')

    # input specification
    inputs = [raw_path]
    # output specification mapping a label to each file
    outputs = {'uppercased_path': uppercased_path}
    # resource specification
    options = {'memory': '8g', 'walltime': '00:10:00'} 

    # tmporary output file path
    tmp_uppercased_path = modify_path(raw_path, dir='/tmp')

    # commands to run in task (bash script)
    # we write to a tmp file and move that to the output directory 
    # only if the command succeds (the && takes care of that)
    spec = f"""
    mkdir -p {output_dir}
    cat {raw_path} | tr [:lower:] [:upper:] > {tmp_uppercased_path} &&
        mv {tmp_uppercased_path} {uppercased_path}
    """
    # return target
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


# task template function
def divide_names(uppercased_path, me=None):
    """
    Splits names into two files. One with my name and one with other names.
    """
    # uppercased version of the me argument
    uppercased_me = me.upper()

    # dir for files produces by task
    output_dir = 'steps/filtered_names'
    # path of output file with names matching me
    filt_me_path = modify_path(uppercased_path, dir=output_dir, suffix=f'_{me}.txt')
    # path of output file with other names
    filt_other_path = modify_path(uppercased_path, dir=output_dir, suffix=f'_not_{me}.txt')

    # input specification
    inputs = [uppercased_path]
    # output specification mapping a label to each file
    outputs = {'filt_me_path': filt_me_path, 'filt_other_path': filt_other_path}
    # resource specification
    options = {'memory': '8g', 'walltime': '00:10:00'} 

    # tmporary output file paths
    tmp_filt_me_path = modify_path(filt_me_path, dir='/tmp')
    tmp_filt_other_path = modify_path(filt_other_path, dir='/tmp')

    # commands to run in task (bash script)
    # we write to tmp files and move them to the output directory 
    # only if the command succeds (the && takes care of that)
    spec = f"""
    mkdir -p {output_dir}    
    grep {uppercased_me} {uppercased_path} > {tmp_filt_me_path} &&  
        grep -v {uppercased_me} {uppercased_path} > {tmp_filt_other_path} &&  
        mv {tmp_filt_me_path} {filt_me_path} &&  
        mv {tmp_filt_other_path} {filt_other_path}
    """
    # return target
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


# task template function
def unique_names(filt_me_path, filt_other_path): 
    """
    Extracts unique names from a file.
    """
    # dir for files produces by task
    output_dir = 'steps/unique_names'
    # path of output file with unique names matching me
    uniq_me_path = modify_path(filt_me_path, dir=output_dir, suffix='_unique.txt')
    # path of output file with unique other names
    uniq_other_path = modify_path(filt_other_path, dir=output_dir, suffix='_unique.txt')

    # input specification
    inputs = [filt_me_path, filt_other_path]
    # output specification mapping a label to each file
    outputs = {'unique_me_path': uniq_me_path, 'unique_other_path': uniq_other_path}
    # resource specification
    options = {'memory': '8g', 'walltime': '00:10:00'} 

    # tmporary output file paths
    tmp_uniq_me_path = modify_path(uniq_me_path, dir='/tmp')
    tmp_uniq_other_path = modify_path(uniq_other_path, dir='/tmp')

    # commands to run in task (bash script)
    # we write to tmp files and move them to the output directory 
    # only if the command succeds (the && takes care of that)
    spec = f"""
    mkdir -p {output_dir}    
    sort {filt_me_path} | uniq > {tmp_uniq_me_path} && 
        sort {filt_other_path} | uniq > {tmp_uniq_other_path} && 
        mv {tmp_uniq_me_path} {uniq_me_path} && 
        mv {tmp_uniq_other_path} {uniq_other_path}
    """
    # return target
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


# task template function
def merge_names(paths, output_path): 
    """
    Merges names from many files.
    """
    # dir for files produces by task
    output_dir = modify_path(output_path, base='', suffix='')

    # input specification
    inputs = [paths]
    # output specification mapping a label to the file
    outputs = {'path': output_path}

    # tmporary output file path
    tmp_output_path =  modify_path(output_path, dir='/tmp')

    # resource specification
    options = {'memory': '8g', 'walltime': '00:10:00'} 

    # commands to run in task (bash script)
    # we write to tmp files and move them to the output directory 
    # only if the command succeds (the && takes care of that)
    spec = f"""
    mkdir -p {output_dir}
    cat {' '.join(paths)} > {tmp_output_path} && 
        mv {tmp_output_path} {output_path}
    """
    # return target
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


###############################################################################
# %% [markdown]
"""
## Workflow:
"""

# %%

# instantiate the workflow
gwf = Workflow(defaults={'account': 'ari-intern'})

# input files for workflow
input_file_names = ['data/input_file1.txt', 'data/input_file2.txt']

# workflow parameter
myname = 'Kasper'

# run an uppercase_names task for each input file
uppercase_names_targets = gwf.map(uppercase_names, input_file_names)

# run an divide_names task for each output file from uppercase_names
filter_names_targets = gwf.map(divide_names, uppercase_names_targets.outputs, extra=dict(me=myname))

# run an unique_names task for each output file from divide_names
unique_names_targets = gwf.map(unique_names, filter_names_targets.outputs)

# collect the outputs labelled 'unique_me_path' from all the outputs of unique_names 
collected_outputs = collect(unique_names_targets.outputs, ['unique_me_path'])

# create a single task to merge all those files into one
merge_me_target = gwf.target_from_template(
    'merge_not_me_name_files',
    merge_names(collected_outputs['unique_me_paths'], "results/merged_me_names.txt")
    )

# collect the outputs labelled 'unique_other_path' from all the outputs of unique_names 
collected_outputs = collect(unique_names_targets.outputs, ['unique_other_path'])

# create a single task to merge all those files into one
merge_other_target = gwf.target_from_template(
    'merge_me_name_files',
    merge_names(collected_outputs['unique_other_paths'], "results/merged_not_me_names.txt")
    )

