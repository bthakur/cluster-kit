#!/bin/bash

set -Eeu

# Author: Bhupender Thakur 2017

TopLog="$HOME"
Comm='ibnetdiscover'
Logd="$TopLog/logs/infiniband"

Date=`date +%Y%m%d%H%M`
Logc=$Logd/${Comm}-last.txt
Logf=$Logd/${Comm}-last.log
Prev=$Logd/$Comm-prev.cache
Curr=$Logd/$Comm-curr.cache

Cache=$Logd/$Comm-${Date}.cache

## Create dirs
mkdir -p "$Logd"

## Run command
$Comm --cache ${Cache} >& ${Logc}

## Create link for previous cache if missing
#[ -L $Prev ] || ln -s ${Cache} ${Prev}

## Rotate cache links and spit diff
if [ -L $Curr ]; then
    $Comm --diff $Curr |tee ${Logf}
    if [ -L $Prev ]; then
        rm ${Prev} |tee -a ${Logf}
        mv -v ${Curr} ${Prev} |tee -a ${Logf}
    else
         mv -v $Curr $Prev |tee -a ${Logf}

    fi
fi

# Update current link
ln -vs ${Cache} ${Curr} |tee -a ${Logf}


