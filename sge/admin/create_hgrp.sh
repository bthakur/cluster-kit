#!/bin/bash

# File to create
  hgrp_file="mc_test"
  if [ -f "$hgrp_file" ]; then
    rm -v "$hgrp_file"
  fi
  touch "$hgrp_file"

# List of nodes in hostlist
  hgrp=$(for f in {21..54} {57..67}; do echo "mc13$f-ib.nersc.gov \\"; done)

# Write to file
  echo "group_name @mc_test" > "$hgrp_file"
  echo "hostlist ${hgrp%'\'}" >> "$hgrp_file"

# Create the hostgroup
  qconf -Ahgrp "$hgrp_file"

