# The Dirac Engine: a tribute to a legend

## Contents

0. [A Tribute to a Legend](#a-tribute-to-a-legend)
1. [Let's Get Started](#lets-get-started)
    * [Requirements](#requirements)
    * [Installation](#installation)
    * [Importing the engine](#importing-the-engine)
2. [Hello Quantum World](#hello-quantum-world)

## A Tribute to a Legend

The **Dirac engine** is a *Pyhon physics engine* which simulates quantum phenomena. This includes basic quantum and wave mechanics, [spin 1/2 particles](https://en.wikipedia.org/wiki/Spin-1/2) and their antimatter partners.

In 1928 [**Paul Dirac**](https://en.wikipedia.org/wiki/Paul_Dirac), an english physicist, was working on a relativistic theory of quantum mechanics. The result is a beautiful equation:

[$$ i \hbar \gamma^\mu \partial_\mu \ket\psi - m c \ket\psi = 0 $$](https://en.wikipedia.org/wiki/Dirac_equation)

This equation predicts electron spin, the periodic table, antimatter and the **g** factor. It is also the first building block of [**quantum field theory**](https://en.wikipedia.org/wiki/Quantum_field_theory): оur best description of reality (yet).

This equation is the core of the **Dirac engine**. This is why this name has been chosen for the project. The engine is *a tribute to a legend*: **Paul Dirac**, one of the geniuses of the 20th century.

[<p align="center"><image src="./assets/paul_dirac.png" width=30% /></p>](https://en.wikipedia.org/wiki/Paul_Dirac)

Quantum field theory is hard. It requires years of studying just for the basics. But that is not the main problem. Calculations in quantum field theory are beyond the performance limits of modern computers. So, how could we simulate the quantum realm?

Fortunately, quantum field theory's predecessor: [**quantum mechanics**](https://en.wikipedia.org/wiki/Quantum_mechanics), is easier. It does not require you to build a cluster of supercomputers. You can simulate basic quantum phenomena on your own computer.

---

## Let's Get Started

### Requirements:

Let's get started with the engine. Firstly: the **requirement**. Using this engine is not for everyone. But if you have passed the requirements you will not have any problems when coding. Here are they:

* Python: *it is obvious*

* basic quantum mechanics: *don't worry, I have provided an [introduction guide to quantum mechanics]()*

* linear algebra: *this is Python so you should be good*

* hamiltonian mechanics: *if you know this, you can skip the other*

* multivariable calculus: *just the basics*

* basic physics: *this is a must*

### Installation:

If you are comfortable with most of the requirements, you can proceed to the **installation**. You can install it like any other PIP package. Just open your terminal and paste this command:

```console
pip install dirac
```

Congratulations! You have installed the **Dirac engine**.

### Importing the engine:

Now let's import the package in Python. Open a new .py flie and write:

```python
import dirac
```

This is it. You are ready to use the **Dirac engine**.

## Hello Quantum World

In this "chapter" we will show you how to code your first simulations...