# vrn7500tools

Tools for programming the Vero N-7500 and Retevis RT99 mobile amateur radios, in particular from data available at [RepeaterBook](https://repeaterbook.com/index.php/en-us/home)

# Workflow

1. Perform search on RepeaterBook.
1. Export to csv in CHIRP format.
1. `$ chirp2cg -n "My Channel Group" < my.csv > my.json`
1. Open `my.json` on phone via Dropbox, Google Drive, or similar.
1. Select all file content and copy to clipboard.
1. Open HT app to import channel group.

# Recommended settings for export to CHIRP

  - memory name 1: call sign
  - memory name 2: none (channel names are limited to 8 characters)
  - S to N
  - W to E

# How to contribute

Anybody is welcome to submit issues and/or pull requests!

# References

- https://chirp.danplanet.com/projects/chirp/wiki/DevelopersToneModes
- https://github.com/stedolan/jq/wiki/Cookbook#convert-a-csv-file-with-headers-to-json
- 