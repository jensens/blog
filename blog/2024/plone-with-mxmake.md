---
blogpost: true
date: Apr 24, 2024
author: Jens W. Klein
location: Austria
category: Plone
language: en
---

# Bootstrap a Plone backend with mxmake

mxmake simplifies the setup of a Plone backend.

# Preconditions

You need Python 3.9+, [make](https://www.gnu.org/software/make/) and [pipx](https://pipx.pypa.io/stable/) installed.

# Generate the Makefile

Create a new directory for your project and inside run:

```bash
pipx run mxmake init
```

Use arrow keys and space to select topics `core` and `applications`.
If you plan to develop and addon, select `qa` as well.
Press `Enter` to confirm.

In the next step, if `qa` was selcted, select domains you like to use.
If in doubt, select `black`, `isort`, `test` and `zpretty`.
Press `Enter` to confirm.

From topic core select all domains.
Press `Enter` to confirm.

From topic applications select `cookiecutter` and `zope`.
If you plan to develop a addon and release it to pypi, select `zest.releaser` as well.
Press `Enter` to confirm.

Now confirm all questions with their default selection by pressing enter several times.

Now you have a `Makefile` in your project directory.
Additional an `mx.ini` was created.

# Create the basic Plone setup files:

```shell
echo "-c https://dist.plone.org/release/6.0.10.1/constraints.txt" > constraints.txt
echo "Plone
# the next line is a quick fix and should be removed when the next Plone release is out and used
lxml[html_clean]
" > requirements.txt
echo "
default_context:
    initial_user_password: admin
    debug_mode: true
> instance.yaml"
```

# Modifications to the Makefile

The Makefile contains a header with some variables.
Only change the variables in the header and do not touch the Makefile below the header.

In the case you need custom targets or variables, use a include.mk file.
For now, we don't.

Open the file in an editor and change variables:

Since plone 6.10 needs Python 3.9 at least, set the PYTHON_VERSION to 3.9:

```make
PYTHON_MIN_VERSION?=3.9
```

If you plan to develop an addon, you need to allow pre-releases.
Edit the `Makefile` and change the PACKAGES_ALLOW_PRERELEASES to true:

```make
PACKAGES_ALLOW_PRERELEASES?=true
```

It is highly satisfying to have a fast installation process.
pip is slow, but now there is the fast drop-in replacement [uv].
To use it (optional), set PYTHON_PACKAGE_INSTALLER to uv:

```make
PYTHON_PACKAGE_INSTALLER?=uv
```

For now that is enough.

# Install and start zope.

Now run:

```shell
make zope-start
```

Go to http://localhost:8080 and login with `admin` and the password `admin`.
Create a Plone Site.
Enjoy.

