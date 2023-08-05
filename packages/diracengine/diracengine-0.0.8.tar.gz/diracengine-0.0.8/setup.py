from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.8'
DESCRIPTION = 'The Dirac Quantum Engine'
LONG_DESCRIPTION = 'The Dirac engine is a physics engine which simulates quantum phenomena.'

setup(
    name="diracengine",
    version=VERSION,
    author="Nikola Kostadinov",
    author_email="<nikolakostadinov@protonmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['matplotlib', 'wheel'],
    keywords=['python', 'quantum', 'spin', 'ket', 'bra', 'superposition', 'psi', 'dirac', 'engine', 'schrodinger', 'pauli', 'bohr'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)