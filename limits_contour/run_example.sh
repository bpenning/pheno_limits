./makegrid.py -i $1/limit_X_Y.txt
#./plotContour.py darkHiggs_input/grid_info.txt
./extract_values.py $1/grid_info.txt > $1.limits
