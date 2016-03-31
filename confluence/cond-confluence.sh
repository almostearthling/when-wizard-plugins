#!/bin/sh
# usage: cond-confluence.sh GROUP BASEDIR

CONFLUENCE_GROUP="$1"
CONFLUENCE_BASEDIR="$2"
CONFLUENCE_PART="$3"

discard_out () {
  $@ > /dev/null 2>&1
}

PART_FILE="$CONFLUENCE_BASEDIR/$CONFLUENCE_GROUP.run"
EXPECTED_FILE="$CONFLUENCE_BASEDIR/$CONFLUENCE_GROUP.expected"

for x in `cat "$EXPECTED_FILE"`; do
    if ! discard_out fgrep "$x" "$PART_FILE" ; then
        exit 1
    fi
done
exit 0

# end.
