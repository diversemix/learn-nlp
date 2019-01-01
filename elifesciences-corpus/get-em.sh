#!/bin/bash

ROOT="https://api.elifesciences.org/articles"

for id in $(seq 1 38519)
do
  FILE=${id}.json
  if [ ! -f ${FILE} ] ; then
    sleep 0.1
    curl -s ${ROOT}/${id} > ${FILE} &
  fi
done
