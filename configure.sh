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
    echo "  Cowardly refusing to overwrite $destination."
    echo "  Use --force if you really want this."
  else
    cp $source $destination
  fi
}

dest=${1:-}
if [[ $force == 1 ]]; then
  dest=${2:-}
fi

dest=$(realpath $dest)

if [[ $dest == "" ]]; then
  echo "You must specify a destination path"
  exit 1
fi

echo
echo "* Copying configuration to $dest"

copyfile settings/onisite/urls.py $dest/onisite/urls.py
copyfile settings/onisite/settings_local.py $dest/onisite/settings_local.py
copyfile settings/featured/config.py $dest/onisite/plugins/featured_content/config.py
copyfile settings/docker-compose.override.yml $dest/docker-compose.override.yml-development
