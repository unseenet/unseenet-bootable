# Changelog

All notable changes to unseenet-bootable are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow the
[Unseenet conventions](https://github.com/unseenet/.github/blob/main/CONVENTIONS.md#versions).

## [Unreleased]

- **The image tools are here** (#5), with their history: `tools/image/` (the
  terminal image, from unseenet) and `tools/image-graphical/` (from unseenet-gui).
  They build checkouts of the core and the graphical client given as arguments
  (`tools/image/build.sh CORE [ZIP]`, `tools/image-graphical/build.sh GUI CORE [ZIP]`),
  mounted read-only in the Alpine container.
