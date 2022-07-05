#!/usr/bin/python3

import sys
# gdb_path="testGDB.gdb"
gdb_path = sys.argv[1]
#Requires pip install gdal

# standard imports

# import OGR
from osgeo import ogr
# use OGR specific exceptions
ogr.UseExceptions()
# get the driver
driver = ogr.GetDriverByName("OpenFileGDB")
# opening the FileGDB
try:
	gdb = driver.Open(gdb_path, 0)
except Exception as e:
	print(e)
	sys.exit()
featsClassList = []
for featsClass_idx in range(gdb.GetLayerCount()):
	featsClass = gdb.GetLayerByIndex(featsClass_idx)
	featsClassList.append(featsClass)

features_dict={}
primary_key = "Unit"
###
header_row = ['Block','Street','PostalCode','Level','Unit']
###

for layer in featsClassList:
	for feature in layer:
		dic = feature.items()
		feature_dict={}
		for idx,i in enumerate(header_row):
			if i != primary_key:
				feature_dict[i] = dic[i]
		features_dict[dic[primary_key]] = feature_dict

# clean close
del gdb

print(features_dict)