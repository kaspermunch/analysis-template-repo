
import os.path
import os
from collections import defaultdict
from gwf import Workflow

def submoduleB_workflow(working_dir=os.getcwd(), input_files=None, output_dir=None, summarize=True):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # dict of targets as info for other workflows
    targets = defaultdict(list)

    gwf = Workflow(working_dir=working_dir)

    work_output = os.path.join(output_dir, 'B_output1.txt')
    target = gwf.target(
        name='B_work',
        inputs=input_files,
        outputs=[work_output],
    ) << f"""
    touch {work_output}
    """
    targets['work'].append(target)

    if summarize:
        summary_output = os.path.join(output_dir, 'B_output2.txt')
        target = gwf.target(
            name='B_summary',
            inputs=[work_output],
            outputs=[summary_output]
        ) << f"""
        touch {summary_output}
        """
        targets['summary'].append(target)

    return gwf, targets

# we need to assign the workflow to the gwf variable to allow the workflow to be
# run separetely with 'gwf run' in the submoduleB dir
gwf, targets = submoduleB_workflow(input_files=['./input.txt'], output_dir='./B_outputs')