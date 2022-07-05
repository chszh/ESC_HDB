#!/usr/bin/python3
import tkinter
import tkinter.filedialog
import subprocess

root=tkinter.Tk()
try:
	root.tk.call('tk_getOpenFile', '-foobarbaz')
except:
	pass
root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')

baseFrame = tkinter.Frame(root)
baseFrame.grid()

####
#Functions
def setDirName(entry):
	loc = tkinter.filedialog.askdirectory(initialdir = ".")
	entry.delete(0,'end')
	entry.insert(0,loc)

def setFileName(entry):
	loc = tkinter.filedialog.askopenfilename(initialdir = ".")
	entry.delete(0,'end')
	entry.insert(0,loc)

class toggleButton(tkinter.Button):
	def __init__(self,parent,text):
		super().__init__(parent)
		self.state = False
		self['text'] = text
		self['command'] = self.toggle
	def setTrue(self):
		self.state = True
		self['bg'] = 'White'
		self['fg'] = 'Black'
	def setFalse(self):
		self.state = False
		self['bg'] = 'Black'
		self['fg'] = 'White'
	def toggle(self):
		if not self.state:
			self.setTrue()
		else:
			self.setFalse()

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
			feature_dict={}
			for idx,i in enumerate(header_row):
				feature_dict[i] = dic[i]
			features_dict[dic[primary_key]] = feature_dict
	del gdb
	return features_dict
success=[]
nonexist=[]
mismatch=[]
def start_analysis():
	gdb_filepath = gdbEntry.get()
	xslx_filepath = xslxEntry.get()
	key=keyEntry.get()
	header_row,xslx_dict = read_xslx(xslx_filepath,key)
	gdb_dict = read_gdb(gdb_filepath,key,header_row)
	success=[]
	nonexist=[]
	mismatch=[]
	for unit in xslx_dict.keys():
		try:
			g = gdb_dict[unit]
			if xslx_dict[unit] == gdb_dict[unit]:
				success.append(unit)
			else:
				mismatch.append(unit)
		except:
			nonexist.append(unit)
	return success,nonexist,mismatch
	pass

def download_report():
	import datetime
	from pathlib import Path
	epoch_string = datetime.datetime.now().strftime("%s")
	report_filename=f"report_{epoch_string}.txt"
	report_filepath = Path(reportEntry.get()).joinpath(report_filename)
	success,nonexist,mismatch = start_analysis()
	to_write=[]
	for i in mismatch:
		to_write.append(f"MISMATCH,{i}")
	for i in nonexist:
		to_write.append(f"NONEXIST,{i}")
	for i in success:
		to_write.append(f"SUCCESS,{i}")
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
keyEntry.insert(tkinter.END,"Unit")

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

# startButton = tkinter.Button(baseFrame, text="Start", command=start_analysis)
# startButton.grid(row=2, column=3)

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
