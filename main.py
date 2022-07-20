#!/usr/bin/python3
import tkinter
import tkinter.filedialog
import subprocess

root=tkinter.Tk()
try:
	root.tk.call('tk_getOpenFile', '-foobarbaz')
except:
	pass
# root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
# root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')

baseFrame = tkinter.Frame(root)
baseFrame.grid()

####
#Functions
def setDirName(entry):
	loc = tkinter.filedialog.askdirectory(initialdir = ".")
	entry.delete(0,'end')
	entry.insert(0,loc)
	entry.xview_moveto(1)

def setFileName(entry):
	loc = tkinter.filedialog.askopenfilename(initialdir = ".")
	entry.delete(0,'end')
	entry.insert(0,loc)
	entry.xview_moveto(1)

def read_xslx(filepath,key):
	import openpyxl
	wb = openpyxl.load_workbook(filename=filepath)
	all_sheets = wb.sheetnames
	header_row = [i.value for i in wb[all_sheets[0]][1]]
	sheets_dict={}
	for sheet in wb.sheetnames:
		ws = wb[sheet]
		primary_key = key
		for row in ws.iter_rows(min_row=2):
			row_dict={}
			for idx,i in enumerate(header_row):
				row_dict[header_row[idx]]=str(row[idx].value)
			sheets_dict[row[header_row.index(primary_key)].value]=row_dict
	return header_row,sheets_dict

import os
import sys
with open(os.path.dirname(os.path.realpath(sys.argv[0]))+"/mappings.config","r") as f:
	lines = f.readlines()
	llines = [line.strip().split(",") for line in lines]
	mappings={}
	xsl_idx = llines[0].index('xslx')
	gdb_idx = llines[0].index('gdb')
	for line in llines[1:]:
		mappings[line[xsl_idx]] = line[gdb_idx]

def read_gdb(filepath,key,header_row):
	import sys
	from osgeo import ogr
	ogr.UseExceptions()
	driver = ogr.GetDriverByName("OpenFileGDB")
	gdb_path = filepath
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
	primary_key = key
	for layer in featsClassList:
		for feature in layer:
			dic = feature.items()
			if dic['NUM_TYPE'] != "STRATA":
				continue
			feature_dict={}
			for idx,i in enumerate(header_row):
				#for field in header row, extract from dic and place into feat_dict
				if i in dic:
					feature_dict[i] = dic[i]
				elif mappings[i] in dic:
					feature_dict[i] = dic[mappings[i]]
				else:
					print(f"Field {i} does not exist for feature {dic}")
					continue
			features_dict[dic[primary_key]] = feature_dict
	del gdb
	return features_dict

def compare(a,b,getkey=False):
	for key in a.keys():
		aa=a[key].strip()
		bb=b[key].strip()
		if aa.isdigit() and bb.isdigit():
			aa=int(aa)
			bb=int(bb)
		if aa != bb:
			if getkey:
				return (aa,bb)
			return 1
	return 0

success=[]
nonexist=[]
mismatch=[]
def start_analysis():
	gdb_filepath = gdbEntry.get()
	xslx_filepath = xslxEntry.get()
	key=keyEntry.get()
	header_row,xslx_dict = read_xslx(xslx_filepath,key)
	# print(xslx_dict)
	gdb_dict = read_gdb(gdb_filepath,key,header_row)
	to_return = []
	for unit in xslx_dict.keys():
		if unit in gdb_dict:
			a=xslx_dict[unit]
			b=gdb_dict[unit]
			r = compare(a,b)
			if r==0:
				to_return.append((0,unit))
			elif r==1:
				a,b = compare(a,b,getkey=True)
				to_return.append((1,unit,a,b,xslx_dict[unit],gdb_dict[unit]))
		else:
			to_return.append((2,unit))
	return to_return
	pass

def download_report():
	import datetime
	from pathlib import Path
	epoch_string = datetime.datetime.now().strftime("%s")
	report_filename=f"report_{epoch_string}.txt"
	report_filepath = Path(reportEntry.get()).joinpath(report_filename)
	analysis_result = start_analysis()
	to_write=[]
	for i in analysis_result:
		if i[0] == 0:
			to_write.append(f"FOUNDINGDB,{i[1]}")
		elif i[0] == 1:
			to_write.append(f"MISMATCH,{i[1]}")
			to_write.append(f"\"{i[2]}\" != \"{i[3]}\"")
			to_write.append(f"XSLXENTRY:{i[4]}")
			to_write.append(f"GDBENTRY:{i[5]}")	
		elif i[0] == 2:
			to_write.append(f"NOTFOUNDINGDB,{i[1]}")
	with open(report_filepath,'w') as f:
		f.write('\n'.join(to_write))
	pass

gdbLabel = tkinter.Label(baseFrame, text="gdb file:")
gdbLabel.grid(row=0, column=0)

xslxLabel = tkinter.Label(baseFrame, text="xslx file:")
xslxLabel.grid(row=1, column=0)

reportLabel = tkinter.Label(baseFrame, text="report file:")
reportLabel.grid(row=2, column=0)

keyLabel = tkinter.Label(baseFrame, text="Key:")
keyLabel.grid(row=3, column=0)

keyEntry = tkinter.Entry(baseFrame)
keyEntry.grid(row=3, column=1, columnspan=2)
keyEntry.insert(tkinter.END,"NUM_UNIT_ID")

gdbEntry = tkinter.Entry(baseFrame)
gdbEntry.grid(row=0, column=1, columnspan=2)
gdbEntry.insert(tkinter.END,"gdb file location")

xslxEntry = tkinter.Entry(baseFrame)
xslxEntry.grid(row=1, column=1, columnspan=2)
xslxEntry.insert(tkinter.END,"xslx file location")

gdbPickerButton = tkinter.Button(baseFrame, text="Browse", command=lambda: setDirName(gdbEntry))
gdbPickerButton.grid(row=0, column=3)

xslxPickerButton = tkinter.Button(baseFrame, text="Browse", command=lambda: setFileName(xslxEntry))
xslxPickerButton.grid(row=1, column=3)

from tkinter import ttk
progressBar = ttk.Progressbar(baseFrame,orient="horizontal",mode="determinate",length=400)
progressBar.grid(row=4,column=0,columnspan=3)

reportPickerButton = tkinter.Button(baseFrame, text="Browse", command=lambda: setDirName(reportEntry))
reportPickerButton.grid(row=2, column=3)

reportEntry = tkinter.Entry(baseFrame)
reportEntry.grid(row=2, column=1, columnspan=2)
reportEntry.insert(tkinter.END,"report file location")

downloadButton = tkinter.Button(baseFrame, text="Analyze + Download", command=download_report)
downloadButton.grid(row=5, column=1)

quitButton = tkinter.Button(baseFrame, text="Quit", command=root.destroy, bg='Red', fg='Black')
quitButton.grid(row=5, column=3)
root.mainloop()

# gdb_filepath = "/home/cheze/SchoolRelated/term5/software_element/hdb_project/TPY_Batch12.gdb"
# xslx_filepath = "/home/cheze/SchoolRelated/term5/software_element/hdb_project/Unit Attributes(PIDB).xlsx"
# report_filepath = "/home/cheze/SchoolRelated/term5/software_element/hdb_project"
# key="NUM_UNIT_ID"
# header_row=["NUM_UNIT_ID","NUM_BLDNG_GL","NUM_BLK","NME_STREET","NUM_POSTAL_CODE","NUM_LEVEL","NUM_UNIT"]
# gdbEntry.delete(0,'end')
# gdbEntry.insert(0,gdb_filepath)
# xslxEntry.delete(0,'end')
# xslxEntry.insert(0,xslx_filepath)
# reportEntry.delete(0,'end')
# reportEntry.insert(0,report_filepath)
# root.mainloop()