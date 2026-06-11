#!/bin/bash

echo "Compiling..."
echo "NOTE: input class should be named SemAn.java"
javac *.java
echo "NOTE: there are 250 examples to be analyzed"
echo "Starting analysis"
sleep 1.5

cnt=1 # current example index
for f in input/*.in
do
    name=${f%.in}
    name=${name#input/}
    myfile="yourOutput/"$name".out"
    echo $cnt 							#program output
    let "cnt = cnt + 1"
    java SemAn < $f &> $myfile 			#program call 
done

echo "Analysis done; starting compare.sh"
