#!/opt/anaconda/bin/python

import sys
import os
import unittest
import string
from StringIO import StringIO
import py_compile
import nbformat as nbf

from pylint import lint
from pylint.reporters.text import TextReporter
    

# Simulating the Runtime environment
os.environ['TMPDIR'] = '/tmp'
os.environ['_CIOP_APPLICATION_PATH'] = '/application'
os.environ['ciop_job_nodeid'] = 'dummy'
os.environ['ciop_wf_run_root'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'artifacts')

#sys.path.append('../main/app-resources/util/')

#from util import log_input

class NodeATestCase(unittest.TestCase):

    def setUp(self):
        pass

    
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_compile(self):
        try:
          py_compile.compile('../main/app-resources/notebook/run', doraise=True)
        except:
          self.fail('failed to compile src/main/app-resources/notebook/run')
  
    def test_notebook_compile(self):

        nb_source = '../main/app-resources/notebook/libexec/input.ipynb'
        nb = nbf.read(nb_source, 4)

        with open('input.ipynb.py', 'w') as the_file:
    
            for index, cell in enumerate( nb['cells']):
                if cell['cell_type'] == 'code':
            
                    the_file.write("# ===== cell %s (index %s) =====\n" % (cell['execution_count'], index))
            
                    for line in cell['source'].split("\n"):
                        if str(line)[:1] == '%':
                            the_file.write("#%s\n" % str(line))
                        else:
                            the_file.write(str(line) + '\n')
                    
                    the_file.write("\n")

        try:
            py_compile.compile('input.ipynb.py', doraise=True)
        except:
            self.fail('failed to compile src/main/app-resources/notebook/libexec/input.ipynb')
      
    class WritableObject(object):
        "dummy output stream for pylint"
    
        def __init__(self):
            self.content = []
    
        def write(self, st):
            "dummy write"
            self.content.append(st)
    
        def read(self):
            "dummy read"
            return self.content
    
    def test_notebook_pylint(self):
           
        ARGS = ["-r",
            "n",
            '--disable=all',
            '--enable=E0602',
            '--enable=E0603',
            '--score=no'] 
    
        pylint_output = self.WritableObject()
    
        lint.Run(['input.ipynb.py']+ARGS,
                 reporter=TextReporter(pylint_output),
                 exit=False)
    
        for l in pylint_output.read():
            print l
    
        if pylint_output.read():
            raise Exception('Issues with the input.ipynb notebook')
        
if __name__ == '__main__':
    unittest.main()


