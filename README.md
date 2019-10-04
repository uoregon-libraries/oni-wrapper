ONI Wrapper
===

This project is meant to centralize all the elements needed to run ONI for UO's Oregon News site:

- The main ONI repository
- Various plugins
- Oregon-specific theming / HTML overrides
- Various configuration files
- Scripts to pull and glue everything together

Setup
---

To get a usable Oregon News setup:

```bash
git clone git@github.com:uoregon-libraries/oni-wrapper.git
cd oni-wrapper
./checkout.sh
```

You'll now have an `open-oni` directory with all the plugins and settings needed to
run the site in production or development.

Environment
---

In the ONI 0.11 version of Historic Oregon Newspapers, we have to set
environment variables for sensitive configuration rather than using
`/etc/openoni.ini`.  The following values *must* be set:

- `ONI_BASE_URL`: **Required**, set to the base URL for ONI, such as `https://oregonnews.uoregon.edu`
- `ONI_DB_ENGINE`: **Required**, generally set to `django.db.backends.mysql`
- `ONI_DB_HOST`: **Required**, must be set to the database hostname, such as `localhost`
- `ONI_DB_PORT`: **Required**, generally set to `3306`
- `ONI_DB_NAME`: **Required**, must be set to the database name, e.g., `openoni`
- `ONI_DB_USER`: **Required**, must be set to the database user, e.g., `openoni`
- `ONI_DB_PASSWORD`: **Required**, must be set to the database password, e.g., `p@ssw0rdS3cur3d`
- `ONI_SOLR_URL`: **Required**, must be set to the full URL to solr, e.g., `http://localhost:8983/solr/openoni`
- `ONI_SECRET_KEY`: **Required**, must be set to a random key for things like cookie encryption

You may also choose to set `ONI_DEBUG`, but *never* in a production
environment: ONI errors will result in lots of sensitive information being
displayed in the web browser.

In a docker-compose world, you might set these up in `docker-compose.override.yml` like so:

```
version: '2'
services:
  web:
    environment:
      - ONI_DEBUG=1
      - ONI_BASE_URL=http://192.168.0.100
      - ONI_DB_ENGINE=django.db.backends.mysql
      - ONI_DB_HOST=rdbms
      - ONI_DB_PORT=3306
      - ONI_DB_NAME=openoni
      - ONI_DB_USER=openoni
      - ONI_DB_PASSWORD=openoni
      - ONI_SOLR_URL=http://solr:8983/solr/openoni
      - ONI_SECRET_KEY=foo
```

Customize Branches
---

Each sub-project has a branch or tag name in `checkout.sh`, but they can be
overridden via environment variables.  e.g.:

    $ plugin_calendar_checkout=master ./checkout.sh

    * Getting open-oni/open-oni cloned and checked out
      Cloning open-oni/open-oni.git: Success
      Checking out open-oni @ v0.10.0: Success

    * Getting open-oni/plugin_featured_content cloned and checked out
      Cloning open-oni/plugin_featured_content.git: Success
      Checking out plugin_featured_content @ v0.3.0: Success

    * Getting open-oni/plugin_map cloned and checked out
      Cloning open-oni/plugin_map.git: Success
      Checking out plugin_map @ v0.1.0: Success

    * Getting open-oni/plugin_staticpages cloned and checked out
      Cloning open-oni/plugin_staticpages.git: Success
      Checking out plugin_staticpages @ v2.0.2: Success

    * Getting open-oni/plugin_calendar cloned and checked out
      Cloning open-oni/plugin_calendar.git: Success
      Checking out plugin_calendar @ master: Success

    * Getting open-oni/plugin_title_locations cloned and checked out
      Cloning open-oni/plugin_title_locations.git: Success
      Checking out plugin_title_locations @ v0.1.0: Success

    * Getting uoregon-libraries/oregon-oni cloned and checked out
      Cloning uoregon-libraries/oregon-oni.git: Success
      Checking out oregon-oni @ master: Success

This is particularly useful for testing a release branch prior to deployment.

Development
---

### Checkout branches!

If you want to do development, whether on ONI core, the Oregon theme, or any of
the plugins, make sure you check out the appropriate branch first!  This
wrapper checks out specific tags to ensure consistency, but you can't develop
against a tag without creating a branch.

You can use the information provided in the "Customize Branches" section, but
it may be safer to explicitly check out a branch just on the relevant
sub-project(s).

e.g.:

```bash
git clone git@github.com:uoregon-libraries/oni-wrapper.git
cd oni-wrapper
./checkout.sh
./configure.sh

# Work on the theme
cd open-oni/themes/oregon/
git checkout master
```

### Running via Docker

Setup
---

Running the stack is fairly easy; just get your branches set up however you
want, then `cd open-oni` and start docker normally (`docker-compose up -d web`,
for instance).  Make sure you **set the environment variables specified above**
in your `docker-compose.override.yml`!

General info
---

For some reason our old batches were coming in without the expected `_ver01`
suffix on the directory, and they were missing the `data` subdirectory.  On the
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
