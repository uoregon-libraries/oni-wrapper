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
