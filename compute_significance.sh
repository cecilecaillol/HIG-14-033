#!/bin/bash

# Compute all the limits for the VH PAS

TYPE=$1

rm -f limits/$TYPE/.significance_computed

limit.py --significance-frequentist  limits/$TYPE/*
touch limits/.significance_computed

exit 0
