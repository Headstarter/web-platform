#!/bin/bash
input="db.txt"
echo "[";
while IFS= read -r line
do
    echo -n "("
    for i in `seq 1 7` ; do
        if [ $i -gt 1 ] && [ $i -lt 5 ]; then
            echo -n "'";
        fi
        echo -n "$line" | cut -d'|' -f$i | xargs echo -n;
        if [ $i -gt 1 ] && [ $i -lt 5 ]; then
            echo -n "'";
        fi
        echo -n ", ";
    done
    echo -n "$line" | cut -d'|' -f8 | xargs echo -n;
    echo "),";
done < "$input"
echo "]";