#!/bin/bash

timestamp=$(date +"%Y%m%d%H%M%S")
collection=/Users/martin/Desktop/newman_jobs/newmanci/ci/config/your-collection.json
env=/Users/martin/Desktop/newman_jobs/newmanci/ci/config/demo-config.json

# create separate outfile for each run
outfile=/Users/martin/Desktop/newman_jobs/newmanci/ci/newman_logs/outputs/outfile_$timestamp.json

# redirect all output to /dev/null
newman -c $collection -e $env -o $outfile -x 
