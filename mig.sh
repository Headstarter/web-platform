#!/bin/bash
input="db.txt"
echo "[";
while IFS= read -r line
do
    echo -n "("
    for i in `seq 1 7` ; do
        echo -n "'";
        echo -n "$line" | cut -d'|' -f$i | xargs echo -n;
        echo -n "', ";
    done
    echo -n "'";
    echo -n "$line" | cut -d'|' -f8 | xargs echo -n;
    echo "'),";
done < "$input"
echo "]";