# TODO: Fix image loading issues

## Problem
Images in `/images/` and `/illustrations/` directories are being redirected by fumadocs i18n middleware to `/en/images/` which serves HTML instead of the actual image.

This causes hydration mismatches and images not displaying.

## Solution
Move all images to `/public/assets/` directory and update paths in MDX files.

## Tasks
- [x] Move agent-skills-sdk.svg to /public/assets/img/
- [x] Update agent-skills-sdk.mdx image path to /assets/img/
- [ ] Move other images from /public/images/docs/ to /public/assets/img/
- [ ] Update all MDX file image references to use /assets/img/
- [ ] Update blog card component to handle /assets/ paths
- [ ] Test that images load correctly
