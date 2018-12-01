#!/bin/env bash
DIR="/home/reycobra/legoman/curly-robot/images"
inotifywait -m -r -e create "$DIR" | while read f

do
    # you may want to release the monkey after the test :)
    echo monkey
    # <whatever_command_or_script_you_liketorun>
done
