from setuptools import find_packages, setup

with open('README.md') as f:
  readme = f.read()

setup(
  name='krpsim',
  version='0.1',
  description=readme,
  author='kcosta & mtrazzi',
  url='https://github.com/kcosta42/KrpSim',
  package_dir={'': 'sources'},
  packages=find_packages('sources', exclude=('tests', 'docs'))
)
