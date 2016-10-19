#!/bin/bash
# Copyright (c) 2016, NVIDIA CORPORATION.  All rights reserved.
set -e

LOCAL_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ROOT_DIR=$( dirname "$(dirname "$LOCAL_DIR")")

set -x

cd $ROOT_DIR/packaging/deb
git fetch --tags
DEBIAN_REVISION=1ppa1 ./build.sh

if [ "$TRAVIS_REPO_SLUG" != "lukeyeager/python-engineio" ]; then
    echo Skipping PPA upload for fork $TRAVIS_REPO_SLUG
    exit 0
fi
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
    echo Skipping PPA upload for pull request
    exit 0
fi
if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo Uploading to ppa for master branch
fi
if [ ! -z "$TRAVIS_TAG" ]; then
    echo Uploading to ppa for a tag
fi

gpg --import private.key
cd dist/*
debsign *source.changes
dput ppa:luke-yeager/ppa *source.changes

