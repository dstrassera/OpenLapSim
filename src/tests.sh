#!/bin/sh

# command to run
python3 test_SetupFileLoader.py
t1=$?
python3 test_AccEnvCalc.py
t2=$?
python3 test_LapTimeSimCalc.py
t3=$?
python3 test_RunOpenLapSim.py
t4=$?

# based on the output code $? (0 is OK else error)
if [ $t1 -ne 0 ] || [ $t2 -ne 0 ] || [ $t3 -ne 0 ] || [ $t4 -ne 0 ]; then
	cat < "NOK: Some test failed"
	exit 1
else
	echo "OK: All tests passed"
fi
