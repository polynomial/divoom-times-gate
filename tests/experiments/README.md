# Experimental Tests

This directory contains various experimental test scripts that were used during the investigation of the Times Gate API, particularly for trying to get custom text display working.

These tests are not part of the main test suite and are kept here for reference only. They include:

- Various attempts to display text using different approaches
- Channel switching experiments  
- Display mode investigations
- Panel-specific control tests

## Note

These tests were helpful in discovering that:
1. The device accepts text commands but doesn't display them without proper app configuration
2. Panel-specific control works for timers and scoreboards (using undocumented LcdId parameter)
3. The device has 5 panels arranged horizontally

The main findings from these experiments have been incorporated into the library documentation and examples. 