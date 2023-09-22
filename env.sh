#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
#. /home/issa/ISSA-2/HAL-EuroMov-DHM/config/hal/env.sh

if [[ $PIPELINE_INSTANCE == "hal" ]] ; then 

	. ~/ISSA-2/config/hal/env.sh

else
	. ~/ISSA-2/config/agritrop/env.sh

fi

#TODO: change script file permissions
#chmod -R 774 ./**/*.sh



