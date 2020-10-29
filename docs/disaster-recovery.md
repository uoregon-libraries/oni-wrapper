# Disaster Recovery

All batches we've ever ingested for OregonNews are stored in our dark archive.
Reingesting would be very straightforward but for "batch patches" we've had to
create along the way.

This document should be enough for anybody with system access to recover from a
complete system failure.

## Application Setup

Set up ONI on a staging server.  This requires first setting up a server that
can run ONI.  See https://github.com/open-oni/open-oni for those details.

Then clone and set up this repository in order to get all the customizations,
plugins, etc.  The top-level README.md should suffice to explain this process.

## Find / copy batches

**Batches must be copied, but they must not be ingested in this phase!**

Pull *all batches* from the dark archive.  These will live on our dark archive
server in a second-level directory - something like
`/ArchivedProjects/newspapersX/YYYY-MM-DD/batch_...`.

- The "X" in "newspapersX" is (currently) a single digit, so we have for
  instance `/ArchivedProjects/newspapers1` and `/ArchivedProjects/newspapers2`.
- The "YYYY-MM-DD" piece is obviously a date, but what it means is when the
  enclosed batches were archived.  It isn't relevant to anything beyond our
  internal information.

When pulling batches, they need to be put somewhere the staging and production
servers can read at all times.  Anybody can directly request any of the PDF,
XML, or JP2 files at any time, and the JP2s are read constantly for the
newspaper display (OpenSeadragon and RAIS).  The files in the dark archive are
not suitable for the web.  They may not be on a fast network mount and may not
have the uptime necessary for the site to function.

Everything in a batch should be copied to the staging/production mount *except
TIFF files*.  TIFF files use too much space to be put in an "always on" storage
volume.

**AGAIN: batches must be copied, but they must not be ingested yet!**

## Fix batches

In the dark archive we have a set of "batch patches".  These live at their own
level in the directory hierarchy, e.g.,
`/ArchivedProjects/newspapers2/batch-patch`.  The rest of the directory
structure is much the same as other newspapers, with a directory for each date
patches were archived, e.g., `ArchivedProjects/newspapers2/batch-patch/2019-11-26`

On the NCA server, we put this into `/mnt/news/data/batch-patch` when creating
them, so it's possible some will reside there that haven't yet been put into
the dark archive.  Make sure all patches are found!

Each patch directory has the format of `<original batch name>_patch_<patch
version>`.  For instance, `batch_oru_hufnagel_patch_001` refers to the original
dark-archive batch in the directory `batch_oru_hufnagel`.  The number `001`
means that this is the first patch for that batch.  If we found new errors from
that batch, we'd have to create a new patch with `002`.  **Patches must be
applied in their numeric order**.

Within each directory, there will be a README of some kind to explain the
process for applying the patch.  Some patches have bash scripts which copy
fixed derivative files, some run larger Go applications to replace metadata for
bad LCCNs or even issue removal, and some are just odd one-offs.  The README
will explain precisely what the patch does and how to use it.  In cases where
the original batch is going to be altered (beyond non-intrusive fixes like
replacing derivatives), a new batch is usually meant to be created with a
higher version than the prior one, and the old batch isn't meant to stay on the
live mount.  This helps ensure fixes can be applied without causing problems
when the data had already been ingested.

## Fix older batch directory structures

Batches with a name like `batch_oru_hufnagel` (note the lack of `_ver01`) need
to be converted before they can be ingested.  These are older batches from a
vendor which didn't fully comply with the NDNP specifications.  They're easy to
identify due to the lack of version, and beyond the name not following the
necessary conventions, they also lack the `data` subdirectory, which will cause
ONI to fail to ingest them.

Identify all "old-style" batches and create symlinks for them.  They are easy
to identify as the batch location should only have directories named
`batch_XYZ` or `batch_XYZ_verNN`.  Listing everything and filtering out all
directories matching `_ver[0-9][0-9]$` will get all the ones which need
remediation.

Once you have that list:

```bash
for batch in $old_format_batches; do
  fakedir="/opt/old-batches/${batch}_ver01"
  batchsrc=<path to the batches, such as /mnt/lib-batches>
  mkdir -p $fakedir
  ln -s $batchsrc/$batch $fakedir/data
done
```

## Ingest all batches

Start with the converted "old-sytle" batches, then ingest everything newer.

```bash
source /opt/openoni/ENV/bin/activate

for batch in $(find /opt/old-batches -mindepth 1 -maxdepth 1 -type d); do
  /opt/openoni/manage.py load_batch $batch
done

for batch in $(find /mnt/lib-batches -mindepth 1 -maxdepth 1 -type d -name "*_ver[0-9][0-9]"); do
  /opt/openoni/manage.py load_batch $batch
done
```

Obviously replace directories like `/opt/old-batches` and `/mnt/lib-batches`
with the correct paths.

Note that we have a lot of content (roughly 1.3 million pages as of
2020-10-29).  The ingest can take a very long time.  Plan for roughly an hour
per 100k pages.
