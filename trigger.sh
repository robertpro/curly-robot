#!/bin/env bash
DIR="/home/reycobra/legoman/curly-robot/images"
inotifywait -m -r -e create "$DIR" | while read f

do
    # you may want to release the monkey after the test :)
    /home/$USER/legoman/curly-robot/measurement_test/black_board.py --image $(ls -tr images/ | tail -n 1)
    # <whatever_command_or_script_you_liketorun>
done
