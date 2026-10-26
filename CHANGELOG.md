# Changelog

All notable changes to unseenet-bootable are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow the
[Unseenet conventions](https://github.com/unseenet/.github/blob/main/CONVENTIONS.md#versions).

## [Unreleased]

- **Releases follow unseenet-portable's** (#5, #9): `follow-portable` (daily)
  tags here each release unseenet-portable makes - `vX.Y.Z` and the
  `vX.Y.Z.postN` a newer Tor makes there - and builds it from that release's
  USB zips and the parts its `versions.toml` names; the `release` job publishes
  both images, the update zip and `SHA256SUMS.txt` for the maintainer to sign.
  The images take tor from Alpine: the build waits up to 7 days for Alpine to
  have the newest stable tor (`tools/tor_versions.py`), and the notes say which.

- **The image tools are here** (#5), with their history: `tools/image/` (the
  terminal image, from unseenet) and `tools/image-graphical/` (from unseenet-gui).
  They build checkouts of the core and the graphical client given as arguments
  (`tools/image/build.sh CORE [ZIP]`, `tools/image-graphical/build.sh GUI CORE [ZIP]`),
  mounted read-only in the Alpine container.
