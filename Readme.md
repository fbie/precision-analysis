# Tool for Gaze Precision Analysis #

## Prerequisites ##

This tool requires Python 2.7 and NumPy installed.

## Data Preparation ##

All files that need to be analyzed should be put in a folder
```watch-rsvp-data/```. To make things prety, the files need to have
headers added. To do so, you can simply run

```
$ cd watch-rsvp-data/
$ sh add-headers
```

which will add headers to all ```.csv``` files that did not already
have headers.

## Usage ##

With all files that you'd like to be analyzed in the
```watch-rsvp-data/```, you can run the tool via

```
$ sh precision.sh
```

and a file ```precision.csv``` will be written, which contains the
precision data for the analyzed files.
