#!/bin/bash

cat ~/.ensocommands > ~/.ensocommands

for cmd in $(find /Users/takai/Python/my-enso-commands -name '*.py'); do
    echo "execfile(\"$cmd\")" >> ~/.ensocommands
done

cat ~/.ensocommands
