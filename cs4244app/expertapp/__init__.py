import clips, os

currentPath = os.path.dirname(os.path.realpath(__file__))
# clips.Load("".join((currentPath, '/CLP/data.cl#p')))
print(os.getcwd())
myPath = os.getcwd()+'/cs4244app/expertapp/CLP/data.CLP'
clips.Load(myPath)
clips.Reset()
clips.Run()