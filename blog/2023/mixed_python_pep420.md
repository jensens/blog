---
blogpost: true
date: Nov 27, 2023
author: Jens W. Klein
location: Austria
category: Python
language: en
---

# Mix PEP 420 Python Packages With Old Style Packages

Python 3.3 (!) introduced [PEP 420 Implicit Namespace Packages](https://www.python.org/dev/peps/pep-0420/). Prior to this format one had to put an `__init__py` file into each directory to make it a package.

But mixing the two styles is not easy, and the documentation is not very clear about it.
What problems can arise, and how to solve them?

But first a quick recap of the two styles.

## &#128014; Old Style Packages

The old, now outdated package structure was:

- `setup.py` with

   ```python
    from setuptools import find_packages
    from setuptools import setup

    setup(
        # ...
        packages=find_packages("src"),
        package_dir={"": "src"},
        namespace_packages=["firstns", "firstns.secondns"],
        # ...
    )
    ```
- `src/firstns/__init__.py` with

   ```python
    __import__("pkg_resources").declare_namespace(__name__)
    ```
- `src/firstns/secondns/__init__.py` with

   ```python
    __import__("pkg_resources").declare_namespace(__name__)
    ```

- an empty `src/firstns/secondns/thirdactualpackage/__init__.py`
- in `src/firstns/secondns/thirdactualpackage/` the actual Python files with code reside.

This is a lot of boilerplate code, and it is not easy to understand.
There are variations of this, but this is the most common one.


## &#128640; New Style Packages

The new style is much simpler.

- First we do not have any `setup.*` files, but a `pyproject.toml`.
  It needs to have a build-system declared, I use `setuptools` here.
  ```ini
  # ...
  [build-system]
  requires = ["setuptools>=61"]
  build-backend = "setuptools.build_meta"

  [tool.setuptools.packages.find]
  where = ["src"]
  ```
- I create the directories and files needed like so:
  ```bash
  mkdir -p src/firstns/secondns/thirdactualpackage
  touch src/firstns/secondns/thirdactualpackage/__init__.py
  ```

That is all. No more boilerplate code than an empty `__init__.py` file.

## &#128271; Mixing the two styles

If it comes to production environment with wheels, there are no problems at all.

If the packages are installed in editable mode, there are some serious problems.

> **You shall not mix old and new style editable packages of one namespace** in one Python (virtual) environment. The new style package wont work.

&#10060; Failing example:
```bash
pip install -e sources/firstns.oldpackage
pip install -e sources/firstns.newpackage
```
`firstns.oldpackage` and `firstns.newpackage` are both editable packages in the same Python environment. `firstns.oldpackage` will work, but `firstns.newpackage` will not work.
The same is valid for sub-namespaces. `mainns.subns.oldpackage` and `mainns.subns.newpackage` will not work together.
Even if its done with different sub-namespaces in the same main-namespace it will fail to work.

One can mix old and new style packages of **different** namespaces in one Python environment.

&#9989; Working example:
```bash
pip install -e sources/firstns.oldpackage
pip install -e sources/secondns.newpackage
```
`firstns.oldpackage` and `secondns.newpackage` are both editable packages in the same Python environment. Both will work.

&#128161; So what to do?

Do not use editable old style packages together with editable new style packages in one namespace!

Anyway, if you have to touch the source of an old style package, it might be a good idea to convert it to the new style.
Thus you avoid the problem.

I hope this helps to understand the problem and how to solve it.