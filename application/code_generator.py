import pandas as pd
from model import code_blocks
from application.parse_template import parse_template
from application.code_templates import read_csv

class CodeGenerator:
   def __init__(self):
      self.blocks = code_blocks.AllBlocks()
      self.dataframe = pd.DataFrame()

   def load_data(self, csv_file):
      (comments, code) = parse_template('application/code_templates/read_csv.py', csv_file)
      self.dataframe = read_csv.get_code([csv_file]) 
      #self.dataframe = pd.read_csv(csv_file)

      self._create_new_block(comments[0], code)
      #self._create_new_block("Create a dataframe",
      #   ["import pandas as pd", "dataframe = pd.read_csv(\'"+csv_file+"\')"])
      return self.dataframe.shape

   def describe_data(self):
      output = self.dataframe.describe()
      self._create_new_block("Describe data",
         ["data_description = dataframe.describe()", "print(data_description)"])
      return output

   def clean_data(self):
      self.dataframe.dropna(axis=0,inplace=True)
      self._create_new_block("Drop null rows",
         ["dataframe.dropna(axis=0,inplace=True)"])
      return self.dataframe.shape

   def get_labels(self):
      self._create_new_block("Get feature names",
         ["keys = dataframe.keys()", "print(keys)"])
      keys = self.dataframe.keys()
      return keys

   def download_code(self):
      return self.blocks.to_text()

   def _create_new_block(self, comment, statements):
      block = code_blocks.CodeBlock(comment, statements)
      self.blocks.add_next_block(block)
