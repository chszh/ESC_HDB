import main
import unittest
test_xslx_filename = "TestGDBExcel.xlsx"
test_gdb_filename = "testGDB.gdb"
test_key = "Unit"
	
class TestAll(unittest.TestCase):
	def test_read_xslx(self):
		result_header,result_data = main.read_xslx(test_xslx_filename,test_key)
		answer_header = ["Block","Street","PostalCode","Level","Unit"]
		answer_data = {'01': {'Block': '1', 'Street': 'ABC Street', 'PostalCode': '380004', 'Level': '01', 'Unit': '01'}, '02': {'Block': '1', 'Street': 'ABC Street', 'PostalCode': '380004', 'Level': '01', 'Unit': '02'}, '03': {'Block': '1', 'Street': 'ABC Street', 'PostalCode': '380004', 'Level': '02', 'Unit': '03'}, '99': {'Block': '2', 'Street': 'ABC Street', 'PostalCode': '380002', 'Level': '99', 'Unit': '99'}, '130': {'Block': '123', 'Street': 'Toa Payoh Lor1', 'PostalCode': '380123', 'Level': '01', 'Unit': '130'}, '132': {'Block': '123', 'Street': 'Toa Payoh Lor1', 'PostalCode': '380123', 'Level': '01', 'Unit': '132'}, '256': {'Block': '122a', 'Street': 'Toa Payoh Lor2', 'PostalCode': '380122', 'Level': '05', 'Unit': '256'}, '456': {'Block': '122a', 'Street': 'Toa Payoh Lor2', 'PostalCode': '380122', 'Level': '05', 'Unit': '456'}, '457': {'Block': '122a', 'Street': 'Toa Payoh Lor2', 'PostalCode': '380122', 'Level': '06', 'Unit': '457'}}
		self.assertEqual(result_header,answer_header)
		self.assertEqual(result_data,answer_data)
	def test_read_gdb(self):
		result_header,result_data = main.read_xslx(test_xslx_filename,test_key)
		result_gdb_data = main.read_gdb(test_gdb_filename,test_key,result_header)
		answer_gdb_data = {'01': {'Block': '1', 'Street': 'ABC Street', 'PostalCode': '380004', 'Level': '01', 'Unit': '01'}, '02': {'Block': '1', 'Street': 'ABC Street', 'PostalCode': '380004', 'Level': '01', 'Unit': '02'}, '03': {'Block': '1', 'Street': 'ABC Street', 'PostalCode': '380004', 'Level': '02', 'Unit': '03'}, '99': {'Block': '2', 'Street': 'ABC Street', 'PostalCode': '380002', 'Level': '99', 'Unit': '99'}, '130': {'Block': '123', 'Street': 'Toa Payoh Lor1', 'PostalCode': '380123', 'Level': '01', 'Unit': '130'}, '132': {'Block': '123', 'Street': 'Toa Payoh Lor1', 'PostalCode': '380123', 'Level': '01', 'Unit': '132'}, '256': {'Block': '122a', 'Street': 'Toa Payoh Lor2', 'PostalCode': '380122', 'Level': '05', 'Unit': '256'}, '456': {'Block': '122a', 'Street': 'Toa Payoh Lor2', 'PostalCode': '380122', 'Level': '05', 'Unit': '456'}}
		self.assertEqual(result_gdb_data,answer_gdb_data)
	def test_mappings(self):
		test_mapping = {"BLK":"Block","STRT":"Street"}
		test_header = ["BLK","STRT","PostalCode","Level","Unit"]
		result_gdb_data = main.read_gdb(test_gdb_filename,test_key,test_header,mappings=test_mapping)
		answer_gdb_data = {'01': {'BLK': '1', 'STRT': 'ABC Street', 'PostalCode': '380004', 'Level': '01', 'Unit': '01'}, '02': {'BLK': '1', 'STRT': 'ABC Street', 'PostalCode': '380004', 'Level': '01', 'Unit': '02'}, '03': {'BLK': '1', 'STRT': 'ABC Street', 'PostalCode': '380004', 'Level': '02', 'Unit': '03'}, '99': {'BLK': '2', 'STRT': 'ABC Street', 'PostalCode': '380002', 'Level': '99', 'Unit': '99'}, '130': {'BLK': '123', 'STRT': 'Toa Payoh Lor1', 'PostalCode': '380123', 'Level': '01', 'Unit': '130'}, '132': {'BLK': '123', 'STRT': 'Toa Payoh Lor1', 'PostalCode': '380123', 'Level': '01', 'Unit': '132'}, '256': {'BLK': '122a', 'STRT': 'Toa Payoh Lor2', 'PostalCode': '380122', 'Level': '05', 'Unit': '256'}, '456': {'BLK': '122a', 'STRT': 'Toa Payoh Lor2', 'PostalCode': '380122', 'Level': '05', 'Unit': '456'}}
		self.assertEqual(result_gdb_data,answer_gdb_data)
	def test_compare_row(self):
		a = {"id":"1","age":"02","height":"	3"}
		b = {"id":"01","age":"2","height":"03 "}
		c = {"id":"a","age":"2","height":"03"}
		equalResult = main.compare_row(a,b)
		unequalResult = main.compare_row(a,c)
		unequalKey = main.compare_row(b,c,getkey=True)
		self.assertEqual(equalResult,0)
		self.assertEqual(unequalResult,1)
		self.assertEqual(unequalKey,("01","a"))

if __name__ == '__main__':
    unittest.main()