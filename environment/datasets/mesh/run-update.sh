#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Update the AGROVOC graph. An updated Agrovoc dump is typically available every first day of the month.

# download a data dump
./mesh_dump.sh

sleep 5m

# upload a new graph
./import_mesh.sh




