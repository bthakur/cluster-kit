#!/bin/bash

export dir_qmaster_spool=/genepool/GridEngine/spool/genepool/qmaster

export dir_scratch='/global/homes/q/qsuge/project_genepool/dispatchedjobs'

#---#

export Tmp_disp="$dir_scratch/Tmp_disp"
export Tmp_cycl="$dir_scratch/Tmp_cycl"
export Tmp_mesg="$dir_scratch/Tmp_messages"

#---#

[ -f "$Tmp_disp" ] && rm "$Tmp_disp"
[ -f "$Tmp_cycl" ] && rm "$Tmp_cycl"
[ -f "$Tmp_mesg" ] && mv "$Tmp_mesg" "$Tmp_mesg".old
#
touch "$Tmp_disp"
touch "$Tmp_cycl"
touch "$Tmp_mesg"

#---#

for f in $(ls -lt "$dir_qmaster_spool"/messages* |awk '{print $9}' |head -n 10); do
    echo $f
    if [[ "$f" == *.gz ]]; then
	zcat $f >> $Tmp_mesg
    else
	cat $f >> $Tmp_mesg
    fi
done

cat $Tmp_mesg |grep 'schedd run took'|awk '{print $1 $2 " " $7}' > "$Tmp_cycl"
cat $Tmp_mesg |grep 'PROF: dispatched'|awk '{print $1 $2 " " $5}' > "$Tmp_disp"

