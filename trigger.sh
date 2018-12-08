#!/bin/env bash
DIR="./images"

inotifywait -m -e create "$DIR" | while read f
do
    # you may want to release the monkey after the test :)
    ./measurement_test/black_board.py --image $(ls -tr ${DIR}/ | tail -n 1)
    # <whatever_command_or_script_you_liketorun>
done
