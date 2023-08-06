# URLdt
URLdt is a tool used to detect the amount of URL if it is available.


## Installation
You can install urldt by:
`pip install urldt`
*(please use the latest pip to install)*

## Usage


### Required

The targets that you want to check should be put in a CSV file,
the CSV header should at least contain *url* and *title*.

For example:

```csv
url,title
http://shangcode.cn, blog of shangcode
http://dokebi.cn, blog of a cool guy
```

### Running

1. check if targets are available
    `urldt -f my_targets.csv` or `urldt --file my_targets.csv`

    The result will be output to the terminal in real-time.

2. output result to file
    `urldt -f my_targets.csv -o result.csv` or `urldt --file my_targets.csv --output result.csv`

    Save the available URL information into a CSV file.