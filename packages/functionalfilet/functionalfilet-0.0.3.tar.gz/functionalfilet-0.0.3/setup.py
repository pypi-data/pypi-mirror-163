# 20220810 fabienfrfr
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Evolutionnary Neural Network Model with PyTorch'
LONG_DESCRIPTION = 'A package based on the article : An Artificial Neural Network Functionalized by Evolution'

# Setting up
setup(
    name="functionalfilet",
    version=VERSION,
    author="FabienFrfr (Fabien Furfaro)",
    author_email="<fabien.furfaro@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'torch', 'torchvision', 'networkx', 'tqdm'],
    keywords=['python', 'pytorch', 'graph', 'machine learning', 'evolution'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
