 

Replace `package_name` with actual package name below:

In docs run:

    sphinx-quickstart

In the conf.py file, uncomment and edit the three lines as follows:
```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

Run this to explore the module looking for docstring and genrated a document file (rst format by default).

    sphinx-apidoc -f -o . ../package_name

Modify the _doc/source/index.rst to add the module to the index:
```rst
Contents:

.. toctree::
   :maxdepth: 2
   modules
   MyClass
```

Generate the documentation

    make html # or pdf or epub or ...
