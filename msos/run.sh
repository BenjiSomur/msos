#!/bin/bash
read -p "Enter the name of the machine: " filename
eval "$(conda shell.bash hook)"
conda activate general
for (( i = 1; i <= 5; i++)); do
    for ((j = 1; j <=31; j++)) do
        python3 main.py $i $j $filename
        echo "Execution $j of instance $i finished"
    done
done

echo "Computation complete :)"
conda deactivate
