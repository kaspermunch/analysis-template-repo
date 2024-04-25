
"""Tiny example workflow for submodule B"""

import os.path
import os
from collections import defaultdict
from gwf import Workflow


def submodule_b_workflow(working_dir=os.getcwd(), 
                         input_files=None,
                         output_dir=None, 
                         summarize=True):
    """Workflow B"""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # dict of targets as info for other workflows
    sub_targets = defaultdict(list)

    sub_gwf = Workflow(working_dir=working_dir)

    work_output = os.path.join(output_dir, 'B_output1.txt')
    target = sub_gwf.target(
        name='B_work',
        inputs=input_files,
        outputs=[work_output],
    ) << f"""
    touch {work_output}
    """
    sub_targets['work'].append(target)

    if summarize:
        summary_output = os.path.join(output_dir, 'B_output2.txt')
        target = gwf.target(
            name='B_summary',
            inputs=[work_output],
            outputs=[summary_output]
        ) << f"""
        touch {summary_output}
        """
        sub_targets['summary'].append(target)

    return sub_gwf, sub_targets

# we need to assign the workflow to the gwf variable to allow the workflow to be
# run separetely with 'gwf run' in the submoduleB dir
gwf, targets = submodule_b_workflow(input_files=['./input.txt'], output_dir='./B_outputs')
