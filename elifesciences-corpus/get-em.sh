#!/bin/bash

ROOT="https://api.elifesciences.org/articles"

for id in $(seq 1 38519)
do
  curl -s ${ROOT}/${id} > ${id}.json &
done
