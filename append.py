import re
import os
import shutil

# Define the source file and target directory
source_file = './.config_base'
target_dir = './files'
target_file='config'

# Create the target directory if it doesn't exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Define the target file path
target_file = os.path.join(target_dir, target_file)

# Copy the source file to the target directory
shutil.copy(source_file, target_file)
os.chmod(target_file, 0o666)
print(f"Copied {source_file} to {target_file}")

pattern11 = r".*?\(([A-Za*--z\_\d\.]+)\)\s*\:\s*[\(\[\{\<]?([A-Za-z\_\d\.\-\>]+)[\)\]\}\>]?$"
print("appending...")
prefix = "#"


with open('output.txt', 'r') as input_file:
          with open(target_file, 'a') as output_file:
                     output_file.write('#///////////////////////////////\n')
                    
                     for line in input_file:
                                          if line.startswith(prefix):
                                                  continue

                                          mat_t=re.findall(pattern11, line)
                                          #print(line)
                                          #print(mat_t)
                                          mat_t = mat_t[0]
                                          if  mat_t[1]=='on' or mat_t[1]=='-->':
                                               n = 'CONFIG_'+mat_t[0]+'=y\n' 
                                          elif mat_t[1]=='off': 
                                               n = 'CONFIG_'+mat_t[0]+'=n\n' 
                                          
                                          else:
                                               n = 'CONFIG_'+mat_t[0]+'='+mat_t[1] + '\n'                         
                                          output_file.write(n)
input_file.close()
output_file.close()
