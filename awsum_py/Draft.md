# Awsum Draft
Here lies some ideas than I had for this project and I have to do.

### Synopsis
./awsum.py
#### Arguments Done
```
  -h, --help
    Show the help message and exit
  -c CONFIGFILE, --configfile CONFIGFILE
    Specify the path to the configfile
  -o output_file, --output output_file
      Specify the output file of awsum
```
#### Arguments To be done
```
  --overwrite
      Overwrite output file
```

If -o isn't used, the output file will be writed as output.csv in the cwd.  
If the file already exist, awsum will try to add his data by concatenation except if overwrite is used.  
For the moment, everything is overwrited. Won't be the case in the future.

### Log system (Output)
Awsum must stock his data in a file, probably a CSV file.

### Graph generator
Awsum could have a side program called awsum-graph which take an output file from awsum and generate a graph about it.

### Other things to do
* Check the output path (permission/isfile)
