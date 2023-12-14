#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../../env.sh

echo "graph namespace: $ISSA_NAMESPACE"
              

# Start Virtuoso container if needed
CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME


if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -gt 1 ]; then 

	docker exec -w $VIRTUOSO_CONT_SCRIPT_DIR $CONTAINER_NAME \
     	  isql -H localhost -U dba -P $VIRTUOSO_PWD \
                 exec="LOAD ./delete-graphs.isql" -i $ISSA_NAMESPACE 

fi
