#! /bin/bash

MAX_CHANNELS=13
IFS=$'\n'

for (( i=1; i <= $1; i++ ))
do
    for f in *.csv
    do              
        bname=${f%.csv}
        echo generating channel group $bname $i
        chirp2cg -s $(( (i - 1) * $MAX_CHANNELS )) -n "$bname $i" > "${bname}-$i.json" < $f
    done
done
