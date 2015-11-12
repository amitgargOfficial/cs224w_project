#!/bin/bash

item="Cell_Phones_and_Accessories"
directoryReviews="/Users/shlokadesai/Downloads/Cell_Phones_and_Accessories/" # Directory of year wise reviews files (Input)
directoryItems="/Users/shlokadesai/Downloads/" # Directory of users file (Input)
directory="/Users/shlokadesai/Documents/cs224w_project/" # Will automatically create a directory specifically for this item at that location (Output)
goodRating="3"
year=(2007 2008) # Mention years for parser_two_graphs.py file

directory=$directory$item"/"
mkdir -p $directory

python parser_two_graphs.py $directory $directoryReviews $directoryItems $item $goodRating ${year[*]}

echo "Completed parser_two_graphs.py"

python centrality.py $directory $item

echo "Completed centrality.py"

infomapItemsInput=$directory"Edge_List_Items_"$item".txt"
infomapItemsOutput=$directory"Clusters_Items/"

./Infomap $infomapItemsInput $infomapItemsOutput -z -2 -u

echo "Completed Infomap for Items"

infomapUsersInput=$directory"Edge_List_Users_"$item".txt"
infomapUsersOutput=$directory"Clusters_Users/"

./Infomap $infomapUsersInput $infomapUsersOutput -z -2 -u

echo "Completed Infomap for Users"

#python create_input_PR_files.py

echo "Completed create_input_PR_files.py"

