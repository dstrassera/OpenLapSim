#!/bin/sh

# create a soft link for pre-commit in .git/hooks/

FILE=../.git/hooks/pre-commit.sample
if [[ -f $FILE ]]; then
	rm "$FILE" 
	echo "remouved $FILE"
fi

FILE2=../.git/hooks/pre-commit
if [[ -f $FILE2 ]]; then
	rm "$FILE2" 
	echo "removed $FILE2"
fi

BASEPATH=$(pwd)
#ln -s $BASEPATH/pre-commit ../.git/hooks/pre-commit
cp $BASEPATH/pre-commit ../.git/hooks/pre-commit

if [[ $? -eq 0 ]]; then
	echo "created .git/hooks/pre-commit symbolic link"
fi
