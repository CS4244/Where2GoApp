import clips, os

currentPath = os.path.dirname(os.path.realpath(__file__))
# clips.Load("".join((currentPath, '\CLP\data.cl#p')))
print(currentPath)
clips.Load('/app/cs4244app/expertapp/data.CLP')
clips.Reset()
clips.Run()