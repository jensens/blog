---
blogpost: true
date: Jan 15, 2024
author: Jens W. Klein
location: Austria
category: Plone, Zope, Postgresql
language: en
---


# Fix broken zodbpack on Zope with RelStorage

For some (unknown) reason the pack table in the RelStorage database got into a broken state, which prevented the zodbpack script from running.

The whole failure after running `docker exec plone-service.IDENTIFIER /plone/buildout/bin/zodbpack /plone/buildout/relstorage-pack.cfg` is:

```bash
Traceback (most recent call last):
  File "./bin/zodbpack", line 272, in <module>
    sys.exit(relstorage.zodbpack.main())
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/zodbpack.py", line 106, in main
    storage.pack(t, ZODB.serialize.referencesf)
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/storage/__init__.py", line 924, in pack
    result = pack.pack(t, referencesf, prepack_only, skip_prepack)
  File "src/perfmetrics/metric.py", line 72, in perfmetrics._metric._AbstractMetricImpl.__call__
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/storage/pack.py", line 208, in pack
    tid_int = self.__pre_pack(t, referencesf)
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/storage/pack.py", line 135, in __pre_pack
    self.packundo.pre_pack(tid_int, get_references)
  File "src/perfmetrics/metric.py", line 72, in perfmetrics._metric._AbstractMetricImpl.__call__
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/adapters/packundo.py", line 1445, in pre_pack
    self._pre_pack_main(load_connection, store_connection,
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/adapters/packundo.py", line 1524, in _pre_pack_main
    self.fill_object_refs(load_connection, store_connection, get_references)
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/adapters/packundo.py", line 1325, in fill_object_refs
    refs_found = self._add_refs_for_oids(load_batcher, store_batcher,
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/adapters/packundo.py", line 1382, in _add_refs_for_oids
    store_batcher.insert_into(
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/adapters/batch.py", line 149, in insert_into
    self._flush_if_needed()
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/adapters/batch.py", line 100, in _flush_if_needed
    return self.flush()
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/adapters/batch.py", line 273, in flush
    count += self._do_inserts()
  File "/home/plone/.buildout/shared-eggs/RelStorage-3.5.0-py3.8-linux-x86_64.egg/relstorage/adapters/batch.py", line 364, in _do_inserts
    self.cursor.execute(stmt, params)
psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "object_refs_added_pkey"
DETAIL:  Key (zoid)=(738500) already exists.
```

This could be caused by an upgrade of RelStorage, but I can not say for sure.

The `object_refs_added_pkey` is an primary key index on the column `zoid` in the table `object_refs_added`.

What it tells me: The `object_refs_added` table is not consistent, because the zoid 738500 is already in the table, but should not be there.
Since the table is not used for anything else and will be rebuild on the next pack, I can truncate the whole table (remove all data) and start over.

```bash
docker exec plone-db.IDENTIFIER psql -U plone -d plone -c "TRUNCATE object_refs_added;"
```

Now, the zodbpack runs again and the database got rid of it's old transactions.
