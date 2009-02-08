#!/bin/bash

cat ~/.ensocommands > ~/.ensocommands

for cmd in $(find . -name '*.py'); do
    echo "execfile(\"$cmd\")" >> ~/.ensocommands
done

cat ~/.ensocommands
