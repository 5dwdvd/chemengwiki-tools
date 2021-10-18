# report bugs or ask questions to d21@ic.ac.uk via Teams; made in September 2021 by David - for chemengwiki

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
output = resub(text)

# this part is to remove possible causes of the redundant braces error (see Teams conversation for more information)
# this snippet is highly untested, only use when redundant braces error occurs
# as much as possible do a manual inspection, these two lines might cause further content errors which might need to be corrected manually
output = re.sub(r'_ \{.\}',lambda x: "_ " + x.group()[3],output) #replaces _ {x} with _ x 
output = re.sub(r'\^ \{.\}',lambda x: "^ " + x.group()[3],output) #replaces ^ {x} with ^ x

with open("output.txt","w", encoding='utf-8') as fhandle:
    fhandle.write(output)
with open("input.txt","w") as fhandle:
    fhandle.write("")


