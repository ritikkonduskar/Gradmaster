import pandas as pd
import os
import sys
import time

def main(opts, commline_list):
    """(main):
    Driver of the grademaster script.
    """
    time_start = time.time()

    # now the standard part of the script begins
    logfile = open(opts.logfile, 'a', 0)
    error_file = open(opts.error_file, 'a', 0)

    banner(logfile, SCRIPT_NAME, SCRIPT_VERSION, REVISION_DATE, AUTHOR, DESCRIPTION)

    # give out options of this run
    print_invoked_opts(logfile, opts, commline_list)

    home_dir = os.getcwd()

    tmp_str = "------------------------------------------------------------------------------ "
    print(tmp_str)
    logfile.write(tmp_str + '\n')
    # read in the CSV file with the raw data of grades
    opts.data_file = pd.read_csv("../tests/grade_dummy_file.csv")
    # make a logfile entry and screen entry so that we know where we s
    # print(opts.data_file)

    # print(opts.data_file)
    tmp_str = "Starting data acquisition..."
    print(tmp_str)
    logfile.write(tmp_str + '\n')

    # check that file exists, get filename from optparse
    if opts.data_file is None:
        tmp_str = "... data file not specified!"
        print(tmp_str)
        logfile.write(tmp_str + '\n')
        error_file.write(tmp_str + '\n')

        tmp_str = "Aborting due to missing data file!"
        logfile.write(tmp_str + '\n')
        error_file.write(tmp_str + '\n')
        sys.exit(tmp_str)
    tmp_str = "   ...reading in data..."
    print(tmp_str)
    logfile.write(tmp_str + '\n')

    # open CSV file with raw data
    rawdata_df = pd.read_csv(opts.data_file)
    print_df(rawdata_df)
    sys.exit("print_df(rawdata_df)")

    tmp_str = "   ...cleaning data structure..."
    print(tmp_str)
    logfile.write(tmp_str + '\n')

    # remove empty entries
    for i in rawdata_df.columns:
        if 'Unnamed' in i:
            rawdata_df = rawdata_df.drop(i, 1)
    rawdata_df = rawdata_df.dropna(how='all')
    print_df(rawdata_df)

    tmp_str = "   ...identify keys..."
    print(tmp_str)
    logfile.write(tmp_str + '\n')

    # read top line of data file, which defines the keys
    keys_list = list(rawdata_df.columns)
    n_keys = len(keys_list)
    print(keys_list)

    data_file = open(opts.data_file, 'r')
    # read top line of data file, which defines the keys
    line = data_file.readline()
    # use commas for split operation
    words = line.split(',')
    # extract keys, get rid of empty entries
    keys_list = []
    for word in words:
        if word != '' and word != '\r\m':
            keys_list.append(word)

    tmp_str = "   ...checking validity of data structure..."
    print(tmp_str)
    logfile.write(tmp_str + '\n')
    # check that the standard keys are amongst the first three keys, because that's all we have implemented so far
    if "Last name" not in keys_list[0:4]:
        tmp_str = "   ...'Last name' missing in data structure!"
        print(tmp_str)
        logfile.write(tmp_str + '\n')
        error_file