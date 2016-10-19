#!/bin/bash
# Copyright (c) 2016, NVIDIA CORPORATION.  All rights reserved.
set -e

LOCAL_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ROOT_DIR=$( dirname "$(dirname "$LOCAL_DIR")")

set -x

cd $ROOT_DIR/packaging/deb
git fetch --tags
./build.sh
gpg --import private.key
cd dist/*
debsign *source.changes
dput ppa:luke-yeager/ppa *source.changes

