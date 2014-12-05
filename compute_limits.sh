#!/bin/bash

# Compute all the limits for the VH PAS

# How it works:
# ls -d limits/cmb ... produces a list of the limit configures/masses to
# compute.  i.e. limits/cmb/115, limits/cmb/120.
# This is piped to xargs, which takes each directory DIR 1 at a time (-n 1)
# and calls limit.py --no-repeat --asymptotic --noprefit --expectedOnly DIR
# which actually computes the limit.  The -P 10 option says to do 10 in
# parallel.  For a machine with fewer cores this should be reduced.

TYPE=$1
NUMPROCS=$2

rm -f limits/$TYPE/.limits_computed

if ls -d limits/$TYPE/* | xargs -n 1 -P $NUMPROCS limit.py --asymptotic --expectedOnly --no-prefit
then touch limits/.limits_computed
else exit 1
fi

exit 0
