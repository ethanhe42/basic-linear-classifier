import os
import subprocess
with open('output.txt','w') as f:
    for i in ['','2','3']:
        inp=['python','triclassify.py','training'+i+'.txt','testing'+i+'.txt']
        command=(' ').join(inp)
        f.write('$ '+command+'\n')
        f.write(subprocess.check_output(inp)+'\n')
