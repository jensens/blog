---
blogpost: true
date: Dec 05, 2023
author: Jens W. Klein
location: Austria
category: Python, Plone, Search
language: en
---

# CMS married OpenSearch/ Elasticsearch: collective.elastic.plone

After about four years of engagement: Marriage came with version 2.0.0 in tandem with collective.elastic.ingest.

Plone as an enterprise CMS come with a basic full-text search. The shiny version 2 of both, [collective.elastic.plone](https://pypi.org/project/collective.elastic.plone/) and [collective.elastic.ingest](https://pypi.org/project/collective.elastic.ingest/), bridges with the world of enterprise search, supporting OpenSearch and Elasticsearch.

## 🙈TL;DR

`collective.elastic.plone` is an addon for Plone.
On indexing time it queues an task in a task queue to be processed later by a worker.
It offers an drop-in replacement for any index in Plone's catalog, like the SearchableText index.
The index is configured to query Elastic-/ OpenSearch and the result is then passed opaque to the catalog.
It provides a specialized schema RestAPI endpoint, as well as an search endpoint tailored for a Volto addon.

`collective.elastic.ingest` is the Celery task worker.
It consumes a task from the queue, fetches the content to index using Plone's official RestAPI endpoint, and gets the schema using the custom RestAPI endpoint.
Next it pre-processes the schema and data (cleanup, move, remove, rename, enhance, ...).
On the first call it creates the index, configures it, including  language analyzers, creates the mapping derived from the Plone schema and also sets up ingest pipelines, i.e. to extract binary data.
Then it writes the data to the index server.
It also supports removal of data.

## 🔎 Plone and Searching

Plone has a central component - the ZCatalog - used all over the code to find content based on several vectors, like path, keywords, language, workflow state, ... it sorts the results based on start- or creation date, by order in a folder, or whatever is sortable.

There are disadvantages of having the catalog in the database:
Database caching gets more complex, write conflicts are more probable and some more.

The ZCatalog offers a ZCTextIndex which provides basic full-text search and is capable enough for many use cases.
But is lacks prioritizing fields and has no multilingual support.

For along time there was an drop-in alternative, TextIndexNG, which was meanwhile discontinued.

SOLR with *collective.solr* was (and still is) very popular as an alternative search backend for more than a decade.
SOLR shares the same foundations with Elastic-/ OpenSearch: Both are built on top of Apache Lucene.
Downside: The add-on and setup of SOLR is very complex.
Once one figured it out it is a very powerful tool.

There is another alternative to integrate ElasticSearch: *collective.elasticsearch*.
It follows a different approach: the all-in-one all-in-Plone.
In my biased opinion our approach is way more flexible and faster.
Also, it monkey-patches the Catalog which may lead to ugly side effects.
OTOH it is easier to configure and has an OOTB feeling our integration does not deliver.

Further there are other integrations available, like AI-powered Nuclia, or TypeSense.

## 📜 How did this package evolve?

I wrote the pair of modules about 4 years ago for Peter Holzer, but even if I released them as 1.0 - I never were proud enough to announce them loudly.

Some folks, like Katja Süss, took the packages and used them. Chapeau, you got it running! With lack of documentation and some magic concepts in it this was probably a PITA. My apologies. And Katja, you  even extended the package and made it work with Volto! And not only this, you made it work with OpenSearch too. Thanks so much!

I gathered some experience with ElasticSearch in different projects over the last decade.

Peter and I created a [media repository search for Academy of Fine Arts Vienna](https://repository.akbild.ac.at/) with ElasticSearch behind a Pyramid RestAPI and an Angular frontend.

Before the "collective.elastic.\*", Peter and I experimented with an slightly similar approach to get Plone integration, but run into a dead end, then discontinued *collective.es.* packages.

The base idea was already the same: Plone queues a indexing request and a queue worker in its own process asynchronously indexes the data in ElasticSearch. This worked, just the amount of data to put into the queue was huge, the queuing was slow and the code base was more complex than necessary. Dealing with the mapping of Plone schema to ElasticSearch schemas (confusingly called a "mapping" there) was an monster on its own.

We started over with a new namespace.

## 🥳 Now: Using the Plone RestAPI FTW!

Instead of queuing large amounts of data, a path is enough.
Then a worker thread on a different machine (or container) consumes the task and fetches the data to index.
Plone RestAPI already provides all we need: the full content and a pluggable system to enhance the output with additional information.
The additional information is primary the catalog RID (the internal ID of an indexed item in Plone's catalog), the *allowedRolesAndUsers*, and the timestamp when queued, to ensure to not index over newer content. Important full-text information otherwise not available like *blocks_plaintext* from Volto is added too.

## 🧬 A Schema for the Index Server

One complex problem is to provide the index server with a *mapping* (schema).
In Plone we know our possible fields.
They are either provided by behaviors or as content schemas.
Each field in there has a field class associated.
Lists of values may have a value type.
This is exposed by a new endpoint *@cesp-schema* and read by the ingest-worker.

Should be simple to map?
Well, yes, if there weren't exceptions:
the possibility to have the same field-name in different behaviors with different field types, specific fields that behave different despite the same field type, injected fields in the RestAPI output, and more.

I decided to solve this with configuration: A *mappings.json* file allows to define which distinct field, or if not defined which field type, maps to which Elastic-/ OpenSearch definition. Here it is possible to define ingestion-pipelines as well as well, together with expansion postprocessing instructions (to get binary data not contained in the initial RestAPI call).

An essential part here is to define language specific analyzers per field.
We can use pre-configured analyzers (those are provided for many languages by Lucene) or use custom analyzers (those are configured centralized in configuration file *analyzers.json*).

## 🛀 Cleanup incoming data

Another problem was to cleanup and reorganize the incoming data.
Preprocessing was invented.
Preprocessing gets a list of instructions as configuration and then runs each instruction with its parameters against the schema and the data.

Thus we are now able to move the RID information from deep in *@components/collectiveelastic/rid* to the root, rename *@type* to *portal_type* or drop the whole batching information.
We can not only move the *block_plaintext* information to the root, but add an additional schema hint for the field with language analyzers configured - all in the JSON.

A preprocessing step can be used to remove a field, a field with it's mapping or a whole type or behavior with all it's fields from data and mapping.
It helps to not clutter the index with data you will never query.

## ✍🏽 Writing to the Index server

Finally we have a configured index server and cleaned up data.
The data got now written to the index server and binary data it put to the index servers pipelines to be processed.

## 🐇And how do we search?

### Catalog Index Replacement

When the package is installed in the Plone Control Panel for Add-ons, the *SearchableText* index is replaced by a new *ESProxyIndex*.
It is configured with only a basic query.
To configure the query the query can be either provided as an GenericSetup step or in the ZMI under the index tab of portal_catalog, then selecting SearchableText.

A huge advantage now is the possible boosting of a field in a full-text query.
While ZCTextIndex was not able to give the result a better rank if the title contains a term rather than in the text field or the attached PDF, the new search can boost terms, correct typos and more.

At the Academy of Fine Arts site the employees vcards were not found, but thousands of pages, events and PDFs where the person was involved.
With the new search we now can boost the *last_name* field, so now the employee record with the name comes first.

We have other optimizations as well, like a hidden search terms field with a boost.
For some important pages the editors put some words in there, including synonyms.
This brings up central information pages to at least the top 3.

Thinking this further we could have two full-text indexes, both pointing to the same index server.
Both are configured with different fields in focus, maybe for different parts of the page.

The Query DSL is very powerful, so there are lots of possibilities.

## (Almost) Direct Index Server Queries

While this all works with Volto too, there is a dedicated addon written by Katja, [volto-searchkit-block](https://github.com/rohberg/volto-searchkit-block/).
It bypasses the whole catalog and queries an endpoint *@kitsearch*.
This endpoint takes a query in the OpenSearch or ElasticSearch Query DSL and passes it further to the index server.
But not before permission filters are applied.
It takes the current users roles and adds a new search term to the query before its passed further.
Thus the results are filtered in a similar way as the ZCatalog does.
Only allowed content will be found.

## 🛠️ In Use

The work done now for 2.0 is for the [Academy of Fine Arts main website](https://akbild.ac.at).
It is a Plone 6 ClassicUI with tons of customizations.

Another project with Katja's Volto add-on is the new [GeoSphere Austria website](https://www.geosphere.at).
It is currently evolving and developed in-house with some help of us.
A special feature here: The index contains additional records from the old ZAMG.ac.at and Geologie.ac.at websites.
Both will be replaced at some point in the future by geosphere.at. This will take a while, a multi-site/multi-CMS (Plone 4.3/Typo 3) search was required.

## 🌯 Wrap Up

The two packages *collective.elastic.plone* and *collective.elastic.ingest* are powerful way to enhance the search experience in Plone.

Thats said both are not easy to configure.
Using them requires a good understanding the core concepts of OpenSearch or ElasticSearch.
Primary: Mappings, language analyzers, and the Query DSL.
Additional it helps to now the basics about schemas in Plone.

If you want to try it: Both packages are released as version 2 on the Python Package Index (PyPI).
The README file contains instructions how to run the ingest service together with redis and OpenSearch or ElasticSearch in a local docker environment.