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

In my opinion it is a bit cumbersome, but it works.
Better would be to have a generic Docker image with the plugin already installed, or ready to be activated using a environment variable.
