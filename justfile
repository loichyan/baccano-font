set export := true
set ignore-comments := true
set positional-arguments := true
set shell := ['/usr/bin/env', 'bash', '-euo', 'pipefail', '-c']

just := quote(just_executable()) + ' --justfile=' + quote(justfile())
prefix := env('HOME') / '.local'

_default:
    @command {{just}} --list

build *args:
    ./build.py {{args}} ttf

build-nerdfont *args:
    mkdir -p build/TTF-NF/
    docker run -it --rm -v ./build/TTF:/in:Z -v ./build/TTF-NF:/out:Z nerdfonts/patcher:latest {{args}}

install:
    install -Dm644 build/TTF/* -t {{prefix / 'share/fonts/baccano'}}

patch: && fix-flags
    ./scripts/patch_fonts.py src/*.sfd

copy src +chars: && fix-flags
    ./scripts/copy_glyphs.py -s {{src}}                                             -t src/Baccano.sfd            "${@:2}"
    ./scripts/copy_glyphs.py -s {{replace_regex(src, '\.[^.]+$', '-Italic$0')}}     -t src/Baccano-Italic.sfd     "${@:2}"
    ./scripts/copy_glyphs.py -s {{replace_regex(src, '\.[^.]+$', '-Bold$0')}}       -t src/Baccano-Bold.sfd       "${@:2}"
    ./scripts/copy_glyphs.py -s {{replace_regex(src, '\.[^.]+$', '-BoldItalic$0')}} -t src/Baccano-BoldItalic.sfd "${@:2}"

test *args:
    echo {{quote(args)}}

fix-flags:
    sed 's/^Flags: HW$/Flags: W/' -i src/*.sfd # Doesn't know why flags changed
