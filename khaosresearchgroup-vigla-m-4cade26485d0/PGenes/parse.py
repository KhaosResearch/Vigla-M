import numpy as np

def parse(input):
    dt=[]
    read=0
    for line in input.splitlines():
        if line.strip().startswith('</Code_Summary>'):
            read=0;
        if read==1 and not line.strip().startswith('CodeClass'):
            className,gene,tax,value=line.strip().split(",")
            dt.append(np.array([gene, className, np.float32(value)]))
            #print(line) 
        if line.strip().startswith('<Code_Summary>'):
            read=1
    dt = np.array(dt) 
    return dt

        
