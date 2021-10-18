#  Migration From Confluence to Wiki.js
This document highlights the conversion of chemengwiki pages from Confluence to Wiki.js. The process is quite monotonous and laborious, but some of it can be automated with scripts. 
> The previous workflow document is outdated with our current situation but is a good read because I might gloss over some things here; not too experienced with documentation 

> The scripts, all placed neatly in a folder structure with I/O .txt files, can be found on GitHub in [5dwdvd/chemengwiki-tools](https://github.com/5dwdvd/chemengwiki-tools). Use this if you would like to clone the repo or to download all the scripts to a .zip. I made it public because there shouldn't be any restricted information related to ICL and Wiki content there.
>

##  Initial Steps
I find it better to create the page structure prior to migrating, taking it from the Confluence page: 

<img src="http://chemengwiki.com/Migration_workflow/Assets/update/1.png" alt="drawing" width="400"/>

For convenience, the pages should be made in WIki.js itself by clicking the "New Page" option on the top right menu. This is because Wiki.js uses a metadata header; the pages will not be imported if we make an empty .md file and push it to remote.

<img src="http://chemengwiki.com/Migration_workflow/Assets/update/2.png" alt="drawing" width="400"/>

> A shortcut to this process is to immediately type out the page url into your browser with the format 
>`chemengwiki-test.herokuapp.com/e/en/[RELATIVE PATH]`
>

Wiki.js technically does not use folders. The folders are specified in the path. In the case of `3rd_Year/RE2/1_Introduction_To_RE2`, the page is in the folder `RE2` within the folder `3rd_Year`. Once the entire page structure is created and synced with [Git](https://github.com/nhcheng/chemengwiki), it will be far easier for us to upload Assets by directly pushing (instead of using Wik.js' very limited upload tool).

##  Conversion From HTML to Markdown
Conversion is mainly done via the [chemengwiki-migration](https://chemengwiki-migration.herokuapp.com) page. We're still using Wiki.js; we're just using another webpage to prevent cache issues. 


1. Copy the HTML source code from the Confluence page. This is done through clicking "Edit" and then clicking "Open in source editor" (`< >`) on the top right. In his document, Jingxian recommended copying chunk by chunk (200 to 300 lines).
	![3.png](/Migration_workflow/Assets/update/3.png)
	Personally, I used Ctrl+A and copied everything; I do not think I have found errors.
1. Go to the [conversion page](http://chemengwiki-migration.herokuapp.com/en/Conversion/ConversionPage) and through the menu on the top right, make sure the page is converted to HTML.
1. Edit the page. Clear everything in there and paste the entire source code into it.
1. I recommend keeping a copy of the HTML code in a file or keeping the confluence editor page open for the Image script. I will go into it later on. 
1. Save the page, leave it, and convert the page to Markdown. 

##  Correcting Latex Equations and Headers
1. Copy the Markdown version of the page. The headers and Latex equations will be incorrect.
1. To fix this, use the Python script below. 
> This script requires an input.txt and output.txt file. I recommend using it within a folder.
> Copy the Markdown page into the input.txt file, run the Python script, and copy the corrected Markdown from the output.txt file.
> 
3. Copy the output.txt contents and enter that into the corresponding page in [chemengwiki-test](https://chemengwiki-test.herokuapp.com) via the Markdown editor. 
```Python
#  report bugs or ask questions to d21@ic.ac.uk via Teams; made in September 2021 by David - for chemengwiki

import re
def fixlatex(text):
    text = text.replace("\\\\","\\")
    text = text.replace("\\[","[").replace("\\]","]").replace("\\_","_").replace("\\*","*").replace("\\-","-")
    text = text.replace("\\^","^").replace("^","^ ").replace("_","_ ").replace("{*}","{* }")
    return text
def resub(text):
    text = text.replace("\\\\\\[","$$").replace("\\\\\\]","$$")
    text = re.sub(r"\$[^\$]*\$",lambda x:fixlatex(x.group()),text)
    text = re.sub(r"\$\$[^\$]*\$\$",lambda x:fixlatex(x.group()),text)
    return text


with open("input.txt",encoding='utf-8') as fhandle:
    text = fhandle.read()
#  fix
text = text.replace("###","#")
output = resub(text)

#  this part is to remove possible causes of the redundant braces error (see Teams conversation for more information)
#  this snippet is highly untested, only use when redundant braces error occurs
#  as much as possible do a manual inspection, these two lines might cause further content errors which might need to be corrected manually
output = re.sub(r'_ \',lambda x: "_ " + x.group()[3],output) #replaces _ {x} with _ x 
output = re.sub(r'\^ \',lambda x: "^ " + x.group()[3],output) #replaces ^ {x} with ^ x

with open("output.txt","w", encoding='utf-8') as fhandle:
    fhandle.write(output)
    
#  this part is only to empty the input.txt file once the script is done, remove if uncomfortable with this setting
with open("input.txt","w") as fhandle:
    fhandle.write("")

```
>What this script does is ensure all equations use dollars, replace double backslashes with a single one, reverse all equation breaking modifications, and add spaces (ignored by Latex) to escape Markdown formatting. It also removes the most common redundant curly braces I have observed, which may cause a page-breaking error in Wiki.js (will elaborate below). 
>

##  Redundant Curly Braces Error
See this [page](http://chemengwiki-migration.herokuapp.com/e/en/Test/Break) to understand the error. When curly braces are redundant, the entire page will break. Examples of such redundancy are: `{{T}}`, `{\frac}^{2}`, and `{\left(\right)}^2`. 

To be honest, I have not exactly investigated which of these redundant braces will cause the errors, but it is better to be safe and remove braces when they are not necessary. This is a manual process, but it can be sped up by using a text editor (like VSCode) and finding all the occurences of `{{` and `}}`. 

When it is difficult to figure out which part of the page is causing errors, do a "binary search"-ish trial and error, dividing the page in half and using the half which causes errors to investigate. 

##  Extracting Images
I recommend doing this part simultaneously with the HTML to Markdown conversion because we will need to use the HTML source code. 
1. If the page has images, click `...` on the top right, click on Attachments, and download all the Attachments to a single .zip file.
2. Extract the files to any folder. 
3. We will use this script:
>This script requires a input.txt file. I recommend using it within a folder. 
> Copy the HTML source code to the input.txt file and run the Python script. 
```Python
#  report bugs or ask questions to d21@ic.ac.uk via Teams; made in September 2021 by David - for chemengwiki

import re
import os

#  add the path here 
path = input("Path: ").replace("\\","/")
with open("input.txt",encoding="utf-8") as fhandle:
    text = fhandle.read()
output = [i.strip('"') for i in re.findall(r'".*\.(?:png|jpg|gif|jpeg)"',text)]

#  for debugging only
#  with open("output.txt","w") as fhandle:
#      fhandle.write("\n".join(output))

for ii in range(len(output)):
        try:
            os.rename(path+"/"+output[ii],path+"/"+str(ii+1)+output[ii][-4:])
        except:
            print(output[ii] +" image used twice at position " + str(ii+1) +" !!!")

with open("input.txt","w") as fhandle:
    fhandle.write("")
```
4. The terminal will then request a file path using the message: `Path: `, copy the path of the image-containing folder. 
5. The image is sorted numerically. Remove any unrenamed images and copy the numbered images to the Assets folder for that page. 
6. Assets folders are located in the same folder as the page, and within these Assets folders are subfolders for each page. You can check the GitHub repository to see the way how Assets folders are used. 
>Sometimes, the message containing image used twice at position will appear. In this case, extract the files to another folder from the .zip again, and copy that reused image to the folder with the numbered images. Manually rename it to the specified position, and you're good to go. 
>

>What this script does is sort out all the occurences of the most common image file extensions in the HTML source code and use the file name to rename the images in the specified folder. 

I have not found any errors using this script. 

##  Uploading Images
I'm sure you can do this through either the GitHub developer editor (Thomas showed me this, very cool stuff) by pressing `.` on the repository. I personally do it in my local repository from 	`git clone`. Once you have placed the images into the correct assets folders, I'm sure you can do a 
```git
git add . 
git commit -m "assets"
git push -u origin main
```
and the images will be uploaded to the remote repository. If I recall correctly, this will immediately allow you to access the images from the website link.
> I think a `git pull` might be needed sometimes to sync your local repo with the remote. 
>

##  Inserting Images
This is by far the most arduous, mentally straining, and monotonous process. I've tried automating this but I currently have no idea how to bring this about. Any reference to the images is completely deleted during the conversion to Markdown via Wiki.js. 

Images are generally inserted using this format:
```html
<img src="https://chemengwiki.com/[RELATIVE PATH]/1.png" style="width:250px" alt="[ENTER DESCRIPTION]">
<p style="font-size: 14px; text-align: center; color: grey">
1. [ENTER DESCRIPTION]
</p>
```
[ENTER DESCRIPTION] is alternative text for accessibility to be filled by Jingxian if I recall correctly; leave it as is. [RELATIVE PATH] is to be entered with the file path for where the assets folder is. 

I've written a very simple script to semi-automate this (so there is no need to manually edit the numbers each picture, and because you can just cut and paste there is no need to spend mental resources keeping track of the numbers).

```Python
#  report bugs or ask questions to d21@ic.ac.uk via Teams; made in September 2021 by David - for chemengwiki
output = ""
root = input("Please enter the directory of this page: ").replace("\\","/")
number = int(input("Number: ").strip())
for i in range(1,number+1):
    #  name = input("Name: ").strip() #  this was made to allow entering the alternative text and descriptors, currently unused
    name = "[ENTER DESCRIPTION]"
    if number == "":
        break
    output = output + f'<img src="https://chemengwiki.com/{root}/'+str(i)+f'.png" style="width:250px" alt="{name}">\n<p style="font-size: 14px; text-align: center; color: grey">\n'+str(i)+f'. {name}\n</p>\n'
with open("output.txt","w") as fhandle:
    fhandle.write(output)

```
1. Enter the relative path to the assets folder. With VSCode, you can immediately copy the path relative to the local repository. Otherwise, keep in mind that the first folder will be 3rd_Year or 4th_Year. 
1. Find the largest number on the images in the Assets folder. 
1. Enter this number when requested by the terminal.
1. Open the output.txt file created. You will see a long list of HTML snippets. Sadly, I have not found a way to adjust the file extension automatically. Edit all .jpg, .gif. and .jpeg files manually. 
1. Compare the Confluence page to the Markdown file and "cut and paste" all the HTML snippets inside. 

##  BlockQuote
Sometimes, the pages will have blockquote. This can be done fairly simply manually by adding a `>` in front of each new line. A much easier way to do this is to use the "T in a box" in the Markdown editor above. Simply select the chunk to be quoted and select which decorator/colour to use:

```markdown
> first line
> second line
> 
```
> first line
> second line
> 

In Confluence, we used Danger, Warning, and Success quote blocks. With Wiki.js, we convert these to Warning, Info, and Success, respectively. 
>`is-warning`, previously danger 

>`is-info`, previously warning 

>`is-success`, remains success 

###  Latex Error
Latex equations may sometimes break the decorator (not always, the example below actually works). Correct this by adding a backslash in one line before the decorator.
```markdown
>Latex Break
>$$\text{This is in Latex}$$
>\
>
```
>Latex Break
>$$\text{This is in Latex}$$
>\
>

###  HTML Error
With HTML snippets, it's better to add spacing with the decorator. 
```markdown
><img src="https://chemengwiki.com/1st_Year/Maths1/Assets/maths1_1/1.png" style="width:10%" alt="[ENTER DESCRIPTION]">
><p style="font-size: 14px; text-align: center; color: grey">
>1. [ENTER DESCRIPTION]
></p>
>
```
><img src="https://chemengwiki.com/1st_Year/Maths1/Assets/maths1_1/1.png" style="width:10%" alt="[ENTER DESCRIPTION]">
><p style="font-size: 14px; text-align: center; color: grey">
>1. [ENTER DESCRIPTION]
></p>
>
 for instance, breaks. This doesn't. 
```markdown
><img src="https://chemengwiki.com/1st_Year/Maths1/Assets/maths1_1/1.png" style="width:10%" alt="[ENTER DESCRIPTION]">
><p style="font-size: 14px; text-align: center; color: grey">
>1. [ENTER DESCRIPTION]
></p>
>
>
```
><img src="https://chemengwiki.com/1st_Year/Maths1/Assets/maths1_1/1.png" style="width:10%" alt="[ENTER DESCRIPTION]">
><p style="font-size: 14px; text-align: center; color: grey">
>1. [ENTER DESCRIPTION]
></p>
>
>

###  Markdown List Error
```markdown
>- MarkDown Lists
>- do not like 
>- your decorators.
>
```
>- MarkDown Lists
>- do not like 
>- your decorators.
>

Fix this by adding spacing and a backslash. Both are necessary. 
```markdown
>- MarkDown Lists
>- do not like 
>- your decorators
>- but there's a way to solve this!
>
>\
>
```
>- MarkDown Lists
>- do not like 
>- your decorators.
>- but there's a way to solve this!
>
>\
>
