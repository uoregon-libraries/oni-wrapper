#!/usr/bin/env bash
#
# Clones the repositories we need to run ONI and checks out a configured
# tag/sha/branch for each repository
set -eu

# Repo checkout SHAs / tags - avoid using branch names except when
# experimenting, otherwise we risk creating an unstable codebase for
# production.  Note that an env variable can be used for development work,
# rather than editing this file.
openoni_checkout=${openoni_checkout:-v0.4.0}
plugin_featured_content_checkout=${plugin_featured_content_checkout:-v0.3.0}
plugin_map_checkout=${plugin_map_checkout:-v0.1.0}
plugin_staticpages_checkout=${plugin_staticpages_checkout:-v2.0.2}
plugin_calendar_checkout=${plugin_calendar_checkout:-v0.1.1}
plugin_title_locations_checkout=${plugin_title_locations_checkout:-v0.1.0}
oregononi_checkout=${oregononi_checkout:-v1.1.0}

force=0
if [[ ${1:-} == "--force" ]]; then
  force=1
fi

# Runs a command with an attempt at more graceful error handling than we'd get
# otherwise; git spews all its output to STDERR even when everything is
# successful.
run_git_command() {
  local cmd=$@

  ok=1
  # Make sure captured output retains newlines
  IFS=' '
  output=$(git $cmd 2>&1) || ok=0
  unset IFS
  if [[ $ok == 0 ]]; then
    echo "[31;1mError[0m"
    echo
    echo $output
    exit 1
  fi
  echo "Success"
}

checkout() {
  group=$1
  project=$2
  destination=$3

  echo
  echo "* Getting $group/$project cloned and checked out"

  slug=$(echo $project | tr -cd '[[:alnum:]]_')
  checkoutvar="${slug}_checkout"

  # Allow undeclared vars here just so we can produce a useful message
  set +u
  checkout_value="${!checkoutvar}"
  set -u
  if [[ $checkout_value == "" ]]; then
    echo "Unable to check out project $project: there is no \$$checkoutvar setting"
    return
  fi

  if [[ ! -d $destination ]]; then
    # Destination doesn't exist; just clone it
    echo -n "  Cloning $group/$project.git: "
    # If servername is oregonnews*, don't try to clone as a privileged user
    proto="git@github.com:"
    hn=$(hostname)
    if [[ ${hn:0:10} == "oregonnews" ]]; then
      proto="https://github.com/"
    fi
    run_git_command clone $proto$group/$project.git $destination
  else
    # Destination exists; behavior depends on $force value
    if [[ $force == 1 ]]; then
      # Force: fetch just in case the sha/tag/branch is new
      pushd . >/dev/null
      echo -n "  Fetching repository for forced sync: "
      cd $destination
      run_git_command fetch --prune
      popd >/dev/null
    else
      # Don't force: let user know we aren't modifying the contents of $destination
      echo "  Cowardly refusing to modify existing directory; use --force if you really want this"
      return
    fi
  fi

  pushd . >/dev/null
  cd $destination
  echo -n "  Checking out $project @ $checkout_value: "
  run_git_command checkout $checkout_value
  popd >/dev/null
}

get_oni_plugin() {
  plugin=$1
  checkout open-oni plugin_$plugin $plugin
}

checkout open-oni open-oni open-oni

pushd . >/dev/null
cd open-oni/onisite/plugins
get_oni_plugin featured_content
get_oni_plugin map
get_oni_plugin staticpages
get_oni_plugin calendar
get_oni_plugin title_locations
popd >/dev/null

pushd . >/dev/null
cd open-oni/themes
checkout uoregon-libraries oregon-oni oregon
popd >/dev/null
