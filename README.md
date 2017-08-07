ONI Wrapper
===

This project is meant to centralize all the elements needed to run ONI for UO's Oregon News site:

- The main ONI repository
- Various plugins
- Oregon-specific theming / HTML overrides
- Various configuration files
- Scripts to pull and glue everything together

To get a usable Oregon News setup:

    git clone git@github.com:uoregon-libraries/oni-wrapper.git
    cd oni-wrapper
    ./checkout.sh
    ./configure.sh

You'll now have an `oni` directory with all the plugins and settings needed to
run the site in production or development.

General info
---

For some reason our old batches were coming in without the expected "_ver01"
suffix on the directory, and they were missing the "data" subdirectory.  On the
previous chronam-based site, we had a large shell script to handle this.  This
time around, however, I've devised a much simpler approach to faking the
structure we need:

```bash
for batch in $old_format_batches; do
  fakedir="/opt/old-batches/${batch}_ver01"
  batchsrc=/mnt/blah
  mkdir -p $fakedir
  ln -s $batchsrc/$batch $fakedir/data
  /opt/openoni/manage.py load_batch $fakedir
done
```
