#!/usr/bin/env bash
#
# Clones the repositories we need to run ONI and checks out a configured
# tag/sha/branch for each repository
set -eu

# Repo checkout SHAs / tags - avoid using branch names except when
# experimenting, otherwise we risk creating an unstable codebase for
# production.  Note that an env variable can be used for development work,
# rather than editing this file.
#
# TODO: Use tags here so it's clearer what's going on when stuff changes!
openoni_checkout=${openoni_checkout:-866893255947f8f09969575768e2e1ff673f1aeb}
plugin_featured_content_checkout=${plugin_featured_content_checkout:-9c9a2cf31ecc0be90be9dbe7561c425975d5a695}
plugin_map_checkout=${plugin_map_checkout:-244d1cfa21fcb0010c2192da5b41400fb7e9f238}
plugin_staticpages_checkout=${plugin_staticpages_checkout:-b5233dde24d8f5e26d60d522e924ba2835eea141}
oregononi_checkout=${oregononi_checkout:-1b754d3c705f098ac02b129edf1c66e97f2868ca}

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

  # Don't modify stuff that's already there so dev can happen
  if [[ -d $destination ]]; then
    echo "Cowardly refusing to modify existing directory"
    echo "If you really want to re-sync this repository, remove $(pwd)/$destination and re-run"
    return
  fi

  echo -n "  Cloning $group/$project.git: "
  run_git_command clone git@github.com:$group/$project.git $destination

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

checkout open-oni open-oni oni

pushd . >/dev/null
cd oni/onisite/plugins
get_oni_plugin featured_content
get_oni_plugin map
get_oni_plugin staticpages
popd >/dev/null

pushd . >/dev/null
cd oni/themes
checkout uoregon-libraries oregon-oni oregon
popd >/dev/null
