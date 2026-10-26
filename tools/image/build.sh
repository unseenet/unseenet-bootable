#!/bin/sh
# Build the bootable image in an Alpine container (podman or docker).
#
#   tools/image/build.sh CORE_CHECKOUT [PORTABLE_USB_ZIP]
#
# CORE_CHECKOUT is a checkout of github.com/unseenet/unseenet (the core, its CLI
# and node, installed into the image; its version names the image). This
# repository holds the tools and is mounted at /src, the core at /core.
# Writes dist/image/unseenet-<version>-x86_64.img(.xz). With the portable
# USB zip (from the portable workflow), the stick also runs on Windows, macOS
# and Linux without booting from it.
set -eu
cd "$(dirname "$0")/../.."
CORE=$(cd "${1:?core checkout}" && pwd)
ALPINE=${ALPINE:-docker.io/library/alpine:3.24}
ENGINE=$(command -v podman || command -v docker)
VERSION=${VERSION:-$(cd "$CORE" && python3 tools/dev_version.py)}
mkdir -p dist/image
ZIP=""
if [ -n "${2:-}" ]; then
    cp "$2" dist/image/portable-usb.zip
    ZIP=/src/dist/image/portable-usb.zip
fi
exec "$ENGINE" run --rm -e NOXZ="${NOXZ:-}" -e UNSEENET_TUI="${UNSEENET_TUI:-}" -v "$PWD:/src:z" -v "$CORE:/core:ro,z" "$ALPINE" \
    sh /src/tools/image/build-in-alpine.sh /src/dist/image "$VERSION" $ZIP
