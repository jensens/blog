---
blogpost: true
date: Mar 28, 2024
author: Jens W. Klein
location: Austria
category: Volto, Javascript, Plone
language: en
---

# Generating a Volto 18 alpha project

It's just Yeomen, but it has its quirks. This is for 18.0.0-alpha.25, but should work for other 18 alpha versions as well.

## Preparation

We need a Node.js environment. I use `nvm` to manage my Node.js versions. I have Node.js 20 (current) installed.

```bash
nvm install --lts
nvm use --lts
```

Additionally we need to enable `corepack`.

```bash
corepack enable
```

## Installing Yeoman

Ok, I do not want to install Yeoman globally, so I use an empty package JSON to trick npm to install Yeoman locally.
Long time ago I put `./node_modules/.bin` into my PATH, so I can run local binaries.

```bash
mkdir PATH/TO/PROJECT_BASE
cd PATH/TO/PROJECT_BASE
echo "{}" > package.json
yarn add yo
```

Note: this installs the generating node modules into `node_modules` in the current directory `PATH/TO/PROJECT_BASE`.
Further on I will use `PATH/TO/PROJECT_BASE/frontend` as the directory for the volto-project itself.

## Installing the Volto generator

Here I install the Volto generator `@plone/generator-volto`.
Since I want to use the alpha of Volto 18, I need to be specific about the version.
This needs the 9-alpha of the Volto generator.

```bash
yarn add @plone/generator-volto@9.0.0-alpha.14
```

<!-- Note: I had a strange effect first, I got `Error: Cannot find module 'libnpx' ` on generation.
Well, no idea what's wrong here, but a `npm -i libnpx` fixed it. -->

## Generating the project

Finally we can generate the project. We need to pass the exact version of Volto we want to use.

Yoemen is located in the parent directory, so we need to use the path to the binary.

```bash
yo @plone/volto PROJECT-frontend --volto=18.0.0-alpha.25
```

The Volto generator will ask you some questions.
Answer them and the project will be generated.

```bash
cd PROJECT-frontend
```

## Building the project

A Makefile is generated.
It's broken, so ignore it for now.



```bash
yarn install
```

The project is ready to be started:

```bash
yarn start
```


