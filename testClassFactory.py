import unittest
from classFactory import build_row

import mysql.connector as msc
from database import login_info




class DBTest(unittest.TestCase):
    
    def setUp(self):
        
        self.table = 'animal'
        #cursor to test animal table  against retrieve function
        self.db = msc.Connect(**login_info)
        self.cursor = self.db.cursor()
        self.A = build_row('animal', 'id name family weight')
        self.a = self.A([100, 'Joe', 'Python', 30])
     
        #total number of rows in animal table
        self.cursor.execute('''SELECT COUNT(*) from {0}'''.format(self.table))
        self.count = self.cursor.fetchall()[0][0]
        
        #Optional conditions to test with retrieve function
        self.conditions = '1<2, 2==2,"a"=="a"'
       
        self.C = build_row('user', 'id name email')
        self.c = self.C([1, 'Steve Holden', 'steve@holdenweb.com'])
        
    def test_attributes(self):
        self.assertEqual(self.c.id, 1)
        self.assertEqual(self.c.name, "Steve Holden")
        self.assertEqual(self.c.email, "steve@holdenweb.com")
        
    def test_retrieve_without_conditions(self):
        result_list =[]
        results = self.a.retrieve(self.cursor)
        for row in results:
            result_list.append(row)
        self.assertEqual(len(result_list), self.count)
        
    def test_retrieve_with_conditions(self):
        conditioned_list =[]
        results = self.a.retrieve(self.cursor, self.conditions)
        for row in results:
            for condition in self.conditions.split(','):
                self.assertTrue(eval(condition) == True)
            conditioned_list.append(row)    
        self.assertEqual(len(conditioned_list), self.count)
        
    
    def test_repr(self):
        self.assertEqual(repr(self.c), 
                         "user_record(1, 'Steve Holden', 'steve@holdenweb.com')")

if __name__ == "__main__":
    unittest.main()

