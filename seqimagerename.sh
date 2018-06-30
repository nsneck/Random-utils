#!/bin/bash

HELP=false
VERBOSE=false
while [[ $# -gt 0 ]]
do
arg="$1"

case $arg in
    -i|--in) # input directory
    INDIR="$2"
    shift
    shift
    ;;
    -o|--out) # output directory
    OUTDIR="$2"
    shift
    shift
    ;;
    -h|--help|--info) # print help text
    HELP=true
    shift
    ;;
    -v|--verbose)
    VERBOSE=true
    shift
    ;;
    *) # unknown arg
    shift
    ;;
esac
done

if [[ "$HELP" == true ]] || ! [[ -n "$INDIR" ]] || ! [[ -n "$OUTDIR" ]]; then
    printf "Required arguments:
    -i / --in               The input directory where the images to be renamed are.
    -o / --out              The output directory where renamed images will be saved.

Optional arguments:
    -v / --verbose          Prints file actions performed by the script.
    -h / --help / --info    Prints this help text.\n"
    exit 1
fi

# we do this in case the user doesn't leave a trailing / at the end of dir path
# otherwise file handling inside the dir becomes annoying
if ! [[ "${INDIR: -1}" == "/" ]]; then
    INDIR+="/"
fi
if ! [[ "${OUTDIR: -1}" == "/" ]]; then
    OUTDIR+="/"
fi

i=1
for file in $INDIR*; do
    if [[ -f "$file" ]]; then
        fileinfo=$(file -b "$file")
        case "$fileinfo" in
            *JPEG*)
            ext="jpg"
            ;;
            *PNG*)
            ext="png"
            ;;
            *)
            echo "Unknown file extension for file $file"
            continue
            ;;
        esac
        if [[ "$VERBOSE" == true ]]; then
            echo "Renaming file $file to $OUTDIR$i.$ext"
        fi
        mv -i "$file" "$OUTDIR$i.$ext"
        i=$((i + 1))
    fi
done