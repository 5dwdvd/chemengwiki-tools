# report bugs or ask questions to d21@ic.ac.uk via Teams. made in September 2021 by David - for chemengwiki
import os 
output = ""
root = input("Please enter the directory of this page: ").replace("\\","/")
number = max([int(ii[:-4]) for ii in os.listdir(root)])
# number = int(input("Number: ").strip())
root = root[root.find("Year")-4:]
for i in range(1,number+1):
    # name = input("Name: ").strip()
    name = "[ENTER DESCRIPTION]"
    if number == "":
        break
    output = output + f'<img src="https://chemengwiki.com/{root}/'+str(i)+f'.png" style="width:40%" alt="{name}">\n<p style="font-size: 14px; text-align: center; color: grey">\n'+str(i)+f'. {name}\n</p>\n'
with open("output.txt","w") as fhandle:
    fhandle.write(output)

