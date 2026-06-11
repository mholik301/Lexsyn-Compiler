#!/bin/bash

touch differences.txt
echo "DIFFERENCES:" > differences.txt
cnt=1
total=250 		#hardcoded number of examples
correct=0
for f in input/*.in
do
    name=${f%.in}
    name=${name#input/}
    myfile="yourOutput/"$name".out"
    hisfile="expectedOutput/"$name".out"
    difference=$(diff $myfile $hisfile)
    echo $name >> differences.txt
    echo "-------------------------------------------" >> differences.txt
    diff $myfile $hisfile >> differences.txt
    echo "===========================================" >> differences.txt
    echo >> differences.txt
    echo >> differences.txt
    let "cnt = cnt + 1"
    if [[ -z $difference ]];
	then
	let "correct = correct + 1";
	fi
done
echo "======================================================"
echo "Number of passed / total examples:"
echo "$correct / $total"
echo "Comparisson done, have a look at differences.txt"
echo "to see individual issues"
echo "======================================================"
