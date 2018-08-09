
# BH

## To install

`pip install -r requirements.txt`

## To Run

Place the raw data file in the corresponding sub-directory under `raw-data` directory and then run

`python3 process_data.py --dataset <dataset_name>`

For available dataset names run with help option

### Example:

For Soy data create the following directory structure `raw-data/soy-data` and place the raw data file in it.

`python3 process_data.py --dataset SOY`

## Help

`python3 process_data.py -h` or `python3 process_data.py --help`

to show a list of available datasets and usage

## Other Info
End point files will be generated in `processed-data` directory
