---
blogpost: true
date: Nov 15, 2023
author: Jens W. Klein
location: Austria
category: Container, CI/CD
language: en
---

# Using Kaniko instead of Dockers Buildx in GitlabCI

Dockers `buildx` with `docker:dind` takes a lot of time - about 2 minutes - to run in GitlabCI.

First I planned to use Buildah, since I had good experience on my local machine.
Anyway, it is not very GitlabCI Docker-Runner friendly.
I got `Error during unshare(CLONE_NEWUSER): Operation not permitted` and this lead me into a rabbit hole of configuration of my GitlabCI runner, which I did not want to do, and on customers runners I am not able to do.

So back to the world of alternatives and I found [Googles Kaniko](https://github.com/GoogleContainerTools/kaniko).
First, the documentation is very confusing.
But after looking at some examples, I got it working.
And its stunning simple.

The whole Gitlab CI YAML file to get an OpenSearch container using the [Dockerfile from my other blog post](opensearch-ingest-attachment) with the attachment plugin installed looks like this:

```yaml
stages:
  - build

build-image:
  stage: build
  image:
    name: gcr.io/kaniko-project/executor:v1.9.2-debug
    entrypoint: [""]
  script:
    # build and push the image to GitlabCI registry
    - /kaniko/executor
        --context "${CI_PROJECT_DIR}"
        --dockerfile "${CI_PROJECT_DIR}/Dockerfile"
        --destination "${CI_REGISTRY_IMAGE}:${CI_COMMIT_TAG}"
```

It takes only 35 seconds to finish!
