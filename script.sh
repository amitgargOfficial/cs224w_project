#!/bin/bash
python parser_two_graphs.py
./Infomap Edge_List_Items_Cell_Phones_and_Accessories.txt out/ -z -2 -u 
python create_input_PR_files.py
python analyze.py
python pagerank.py