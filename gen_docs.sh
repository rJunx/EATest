#!/bin/bash

cd docs
sphinx-apidoc -f -o ./source ../EATest
make html
open build/html/index.html