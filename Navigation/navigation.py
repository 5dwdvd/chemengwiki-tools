from os import listdir
from functools import partial

maths_wiki_path = '/Users/thomascheng/Desktop/wiki/wiki_repo/mathswiki'
maths_wiki_url = 'https://imperialmathswiki.com'
module_dir = '1st_year/MATH40002_Analysis'


def navigation(wiki_dir, module_dir):

    # Require the page to be named in the format of 1-9.1-9
    # may break if it runs over 10 pages, e.g. 1.10
    
    directory = wiki_dir + '/' + module_dir
    md_files = sorted([f for f in listdir(directory) if f.endswith('.md')])
    md_files_len = len(md_files); md_files_range = range(md_files_len)
    
    md_links = dict(
                    zip(md_files_range, 
                        map(partial(md_link, files=md_files, module_dir=module_dir)
                            , md_files_range)
                        )
                    )

    result = {file:[
                md_links[(md_files_len+i-1) % md_files_len],
                md_links[(md_files_len+i+1) % md_files_len]] 
              for i,file in enumerate(md_files)}
 
    return result

    
def md_link(i, files, module_dir):
    
    page_link = '%s/%s/%s' % (maths_wiki_url, module_dir, files[i])
    md = '[%s](%s)' %(files[i].split('.')[0], page_link)
    return md

navigation(wiki_dir = maths_wiki_path, module_dir = module_dir)    
