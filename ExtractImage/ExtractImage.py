# report bugs or ask questions to d21@ic.ac.uk via Teams; made in September 2021 by David - for chemengwiki

import re
import os

# add the path here 
path = input("Path: ").replace("\\","/")
with open("input.txt",encoding="utf-8") as fhandle:
    text = fhandle.read()
text = text.replace("&amp;","&")
output = [i.strip('"') for i in re.findall(r'".*\.(?:png|jpg|gif|jpeg)"',text)]

# for debugging only
# with open("output.txt","w") as fhandle:
#     fhandle.write("\n".join(output))

for ii in range(len(output)):
    try:
        os.rename(path+"/"+output[ii],path+"/"+str(ii+1)+output[ii][-4:])
    except:
        print(output[ii] +" image used twice at position " + str(ii+1) +" !!!")

with open("input.txt","w") as fhandle:
    fhandle.write("")

