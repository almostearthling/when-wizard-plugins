#!/bin/sh
# usage: confluence.sh GROUP BASEDIR EVENT_UNIQUEID

CONFLUENCE_GROUP="$1"
CONFLUENCE_BASEDIR="$2"
CONFLUENCE_PART="$3"

discard_out () {
  $@ > /dev/null 2>&1
}

PART_FILE="$CONFLUENCE_BASEDIR/$CONFLUENCE_GROUP.run"

if ! discard_out fgrep "$CONFLUENCE_PART" "$PART_FILE" ; then
    echo "$CONFLUENCE_PART" >> "$PART_FILE"
fi
exit 0

# end.
