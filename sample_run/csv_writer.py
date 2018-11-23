import argparse
import csv
import os


def write(fileName, data):
  if fileName is None:
    print ('ERROR! Need csv file. Please add --file <path_to_csv>')
    exit(1)

  if os.path.isfile(fileName):
    fileEmpty = os.stat(fileName).st_size == 0
  else:
    fileEmpty = True

  with open(fileName, "a") as csvFile:
    keys = data.keys()
    del keys[keys.index('model')]
    del keys[keys.index('image')]
    del keys[keys.index('text button')]

    keys.insert(0, 'image')
    keys.insert(1, 'model')
    keys.insert(2, 'text button')

    headers = keys

    writer = csv.DictWriter(csvFile, delimiter=',', lineterminator='\n', fieldnames=headers)
    if fileEmpty:
      writer.writeheader()  # file doesn't exist yet, write a header
    writer.writerow(data)
