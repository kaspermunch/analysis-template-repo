#!/bin/bash
cp _quarto.yml _tmp.yml && 
cp slides/_quarto.yml _quarto.yml &&
quarto render .
cp _tmp.yml _quarto.yml
