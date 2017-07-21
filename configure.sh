#!/usr/bin/env bash
#
# Copies the various configuration files into their respective locations
set -eu

force=0
if [[ ${1:-} == "--force" ]]; then
  force=1
fi

copyfile() {
  source=$1
  destination=$2

  if [[ $force == 1 ]]; then
    rm -f $destination
  fi

  if [[ -f $destination ]]; then
    echo "Cowardly refusing to overwrite $destination; use --force if you really want this"
  else
    cp $source $destination
  fi
}

copyfile settings/onisite/urls.py open-oni/onisite/urls.py
copyfile settings/onisite/settings_local.py open-oni/onisite/settings_local.py
copyfile settings/featured/config.py open-oni/onisite/plugins/featured_content/config.py
