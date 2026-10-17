#!/bin/sh
# Build the bootable, graphical image in an Alpine container (podman or docker).
#
#   tools/image/build.sh CORE_CHECKOUT [PORTABLE_USB_ZIP]
#
# CORE_CHECKOUT is a checkout of github.com/unseenet/unseenet (the client core,
# installed into the image). Writes dist/image/unseenet-web-<version>-x86_64.img(.xz).
# With the portable USB zip (from the portable workflow) the stick also starts
# the web client on Windows, macOS and Linux without booting from it.
set -eu
cd "$(dirname "$0")/../.."
CORE=$(cd "${1:?core checkout}" && pwd)
ALPINE=${ALPINE:-docker.io/library/alpine:3.24}
ENGINE=$(command -v podman || command -v docker)
VERSION=${VERSION:-$(sed -n 's/^__version__ = "\(.*\)"/\1/p' src/unseenet_web/__init__.py)}
mkdir -p dist/image
ZIP=""
if [ -n "${2:-}" ]; then
    cp "$2" dist/image/portable-usb.zip
    ZIP=/src/dist/image/portable-usb.zip
fi
exec "$ENGINE" run --rm -e NOXZ="${NOXZ:-}" -v "$PWD:/src:z" -v "$CORE:/core:ro,z" "$ALPINE" \
    sh /src/tools/image/build-in-alpine.sh /src/dist/image "$VERSION" $ZIP
