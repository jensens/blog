---
blogpost: true
date: Nov 13, 2023
author: Jens W. Klein
location: Austria
category: Search, Docker
language: en
---

# OpenSearch Docker Ingest Attachment Plugin to index Plone content

How to get a Docker image with the OpenSearch ingest-attachment plugin.

[OpenSearch](https://opensearch.org/), the 2021 fork of the Elasticsearch and Kibana by Amazon, is now established as a community project.

We use it to index Plone content with the [collective.elastic.plone](https://github.com/collective/collective.elastic.plone) and [collective.elastic.ingest](https://github.com/collective/collective.elastic.ingest) packages.
First one is a [Plone](https://plone.org) add-on with an proxy index to the index server, second one is a [Celery]() based Python package based to asynchronous index content and also create and manage the index schemas and ingest pipelines.

However, in order to get OpenSearch up and running in a Docker container, we had to create our own Docker image.
This is because the official OpenSearch Docker image does not contain the [ingest-attachment plugin](), which we need to extract data from a variety of binary formats, like PDF, Word, ... and index them.

The process is documented at the [working with plugins section](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/#working-with-plugins) of the OpenSearch documentation.

First create ``Dockerfile``

```Dockerfile
FROM opensearchproject/opensearch:latest
RUN /usr/share/opensearch/bin/opensearch-plugin install --batch ingest-attachment
```

Next prepare and execute the build:

```bash
docker buildx use default
docker buildx build --tag opensearch-ingest-attachment:latest Dockerfile
```

The image is ready to be used on your local machine (you may want to push it to your trusted Docker registry).

I used the [example docker compose file](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/#sample-docker-composeyml) provided in the documentation.
The lines with the image name `image: opensearchproject/opensearch:latest` are to be changed to the new name `image: opensearch-ingest-attachment:latest`.

With `docker compose up` the container is started and the ingest-attachment plugin is ready for use.

In my opinion it is a bit cumbersome, but it works.
Better would be to have a generic Docker image with the plugin already installed, or ready to be activated using a environment variable.
