import sys, os
wd = os.getcwd()
unipath = wd[:wd.rindex('/')] + '/unisi'
if os.path.exists(unipath):
    print('added possible unipath', unipath)
    sys.path.insert(0,unipath) 
