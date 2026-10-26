#!/bin/sh
# Build the bootable, graphical image in an Alpine container (podman or docker).
#
#   tools/image-graphical/build.sh GUI_CHECKOUT CORE_CHECKOUT [PORTABLE_USB_ZIP]
#
# GUI_CHECKOUT is a checkout of github.com/unseenet/unseenet-gui (the graphical
# client; its version names the image), CORE_CHECKOUT one of github.com/unseenet/
# unseenet (the client core), both installed into the image. This repository
# holds the tools and is mounted at /src, the client at /gui, the core at /core.
# Writes dist/image/unseenet-gui-<version>-x86_64.img(.xz).
# With the portable USB zip (from the portable workflow) the stick also starts
# the graphical client on Windows, macOS and Linux without booting from it.
set -eu
cd "$(dirname "$0")/../.."
GUI=$(cd "${1:?graphical client checkout}" && pwd)
CORE=$(cd "${2:?core checkout}" && pwd)
ALPINE=${ALPINE:-docker.io/library/alpine:3.24}
ENGINE=$(command -v podman || command -v docker)
VERSION=${VERSION:-$(sed -n 's/^__version__ = "\(.*\)"/\1/p' "$GUI/src/unseenet_gui/__init__.py")}
mkdir -p dist/image
ZIP=""
if [ -n "${3:-}" ]; then
    cp "$3" dist/image/portable-usb.zip
    ZIP=/src/dist/image/portable-usb.zip
fi
exec "$ENGINE" run --rm -e NOXZ="${NOXZ:-}" -e UNSEENET_TUI="${UNSEENET_TUI:-}" -v "$PWD:/src:z" -v "$GUI:/gui:ro,z" -v "$CORE:/core:ro,z" "$ALPINE" \
    sh /src/tools/image-graphical/build-in-alpine.sh /src/dist/image "$VERSION" $ZIP
