"""
classFactory: function to return tailored classes
"""

def build_row(table, cols):
    """Build a class that creates instances of specific rows"""
    class DataRow:
        """Generic data row class, specialized by surrounding function"""
        def __init__(self, data):
            """Uses data and column names to inject attributes"""
            assert len(data)==len(self.cols)
            for colname, dat in zip(self.cols, data):
                setattr(self, colname, dat)
                
        def retrieve(self, curs, condition=None):
            '''curs is a predefined database cursor,
            conditon if present, is a string of conditions separated by commas'''
            if condition:
                curs.execute('''SELECT * FROM {0}'''.format(table))
                for data_catch in curs.fetchall():
                    for cons in condition.split(','):
                        con = eval(cons)
                        if con != True:
                            break
                        elif con == True:
                            continue
                    if con != True:
                        print("Condition {0} was evaluated to be False".format(cons))
                        break
                    else:
                        yield DataRow(data_catch)
                        
                     
            else:
                curs.execute('''SELECT * FROM {0}'''.format(table))
                for data_catch in curs.fetchall():
                    yield DataRow(data_catch)
            
            
        def __repr__(self):
            return "{0}_record({1})".format(self.table, ", ".join(["{0!r}".format(getattr(self, c)) for c in self.cols]))
    
    DataRow.table = table
    DataRow.cols = cols.split()
    return DataRow

