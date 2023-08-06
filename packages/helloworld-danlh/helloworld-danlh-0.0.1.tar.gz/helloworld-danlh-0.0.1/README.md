Practice creating Packages

Steps:
- Create 'script'.py, put in src dir inside project directory
- Create setup.py in project dir.
- run: python 'script'.py bdist_wheel (Create package from script.py using setup.py as config)
- run: pip install -e .   (Install package in current directory)
- test script: from 'script' import 'funcname' ... call function
- Choose a license https://choosealicense.com/ and create LICENSE.txt file
- Add classifiers to setup.py file https://pypi.org/classifiers/
- Add a README.md describing project, how to install (with reqs), usage
- Add README to setup.py file as long_description
- Add library dependencies to setup.py as install_requires, and developer dependencies as extras_require  (requirements.txt is an alternative to this, but setup.py recommended)
- Test files in test directory, run pytest
- Optional: url and author in setup.py
- run py setup.py sdist  (For source distribution)
- Publish package: py setup.py bdist_wheel sdist
- Push to PyPI: twine upload dist/*