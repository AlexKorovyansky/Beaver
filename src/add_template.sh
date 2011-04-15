for f in `find "$1" -name "*.$2"`; do cat $3 "$f" > "$f.tmp" ; mv "$f.tmp" "$f"; done
