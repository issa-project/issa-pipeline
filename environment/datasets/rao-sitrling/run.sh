#!/bin/bash

export ISSA_INSTANCE=$1

# ISSA environment definitions
. ../../../env.sh

dump=rao-stirling-dump.ttl

echo "Backup previous data files"
backup_dir=./$ISSA_INSTANCE/bak/$(date "+%Y%m%d")
mkdir -p $backup_dir
cp -f ./$ISSA_INSTANCE/$dump   $backup_dir

echo "Importing hierarchy in Virtuoso..."
./import.sh       $dump

echo "Move files to the instance directory..."
mkdir -p ./$ISSA_INSTANCE
mv -f ./$dump ./$ISSA_INSTANCE
