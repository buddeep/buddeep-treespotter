#!/bin/bash

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

mkdir -p ../streets
cd ../streets

if [ -f "streets.kml" ]; then
  echo "Skipping streets.kml, already exists."
else
  KML_URL="https://data.cityofnewyork.us/api/geospatial/exjm-f27b?method=export&format=KML"
  wget $KML_URL -O streets.kml
fi



