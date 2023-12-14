#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions

if [[ $ISSA_INSTANCE == "hal" ]] ; then 

	. ~/ISSA-2/config/hal/env.sh

elif [[ $ISSA_INSTANCE == "agritrop" ]] ; then

	. ~/ISSA-2/config/agritrop/env.sh

else

    echo "Specify the ISSA instance in the ISSA_INSTANCE environment variable."

fi

#TODO: change script file permissions
#chmod -R 774 ./**/*.sh



