#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Update the HAL Domains graph.

# download a data dump
./extract-domains-graph.sh

sleep 5m

# upload a new graph
./import_hal-domains.sh



