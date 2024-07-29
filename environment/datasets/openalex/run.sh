#!/bin/bash

export ISSA_INSTANCE=$1

# ISSA environment definitions
. ../../../env.sh

openalex_sgds_dump=openalex-sdgs.ttl
openalex_topics_dump=openalex-topics.ttl
openalex_authorships_dump=openalex-authorships.ttl


echo "Backup previous data files"
backup_dir=./$ISSA_INSTANCE/bak/$(date "+%Y%m%d")
mkdir -p $backup_dir
cp -f ./$ISSA_INSTANCE/$openalex_sgds_dump          $backup_dir
cp -f ./$ISSA_INSTANCE/$openalex_topics_dump        $backup_dir
cp -f ./$ISSA_INSTANCE/$openalex_authorships_dump   $backup_dir


echo "Importing files in Virtuoso..."
./import.sh     $openalex_sgds_dump         import-sdgs.isql
./import.sh     $openalex_topics_dump       import-topics.isql
./import.sh     $openalex_authorships_dump  import-authorships.isql


echo "Move files to the instance directory..."
mkdir -p ./$ISSA_INSTANCE
mv -f ./$openalex_sgds_dump         ./$ISSA_INSTANCE
mv -f ./$openalex_topics_dump       ./$ISSA_INSTANCE
mv -f ./$openalex_authorships_dump  ./$ISSA_INSTANCE
