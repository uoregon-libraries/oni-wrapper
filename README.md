ONI Wrapper
===

This project is meant to centralize all the elements needed to run ONI for UO's Oregon News site:

- The main ONI repository
- Various plugins
- Oregon-specific theming / HTML overrides
- Various configuration files
- Scripts to pull and glue everything together
- [General documentation](docs/README.md) for the ODNP (Oregon Digital Newspaper Project) as a whole
- The [search test script](search-test) which is invoked regularly to
  verify the site's most complex task is functioning

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

Modern ONI (0.11 and later) requires sensitive settings to be specified in the
environment.  We don't do this in production since it's a bare-metal install -
it's just easier to hack up the settings file directly to put in those values.
Our internal deploy scripts (generally in `/opt`) handle preserving the
settings file when one already exists.

For docker, the various settings will need to be set, but these are already
pre-set since most of the "secrets" are hard-coded anyway.  ONI's
docker-compose is set up to work well for development.

MARC
---

The subdirectory `marc` contains XML that can be loaded into an ONI site via
the `load_titles` command.  This isn't automated, so it needs to be run
manually when necessary.

Some of these files are housed here because they don't exist on the Library of
Congress Chronicling America site.  Others have minor hacks to offer a better
presentation to users.

In a disaster recovery scenario, these would need to be loaded into our ONI
instance before batches load.

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
in your `docker-compose.override.yml`.  A helpful override is copied into
`docker-comopse.override.yml-development` during the setup scripts; copying and
modifying this may be more helpful than crafting one by hand.

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
