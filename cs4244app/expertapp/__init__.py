import clips, os

currentPath = os.path.dirname(os.path.realpath(__file__))
# clips.Load("".join((currentPath, '/CLP/data.cl#p')))
print(os.getcwd())
myPath = os.getcwd()+'/cs4244app/expertapp/CLP/data.CLP'
# clips.Load(myPath)
# clips.Reset()
# clips.Run()


aClips = clips.Environment()
# aClips.Load(myPath)
bClips = clips.Environment()
# bClips.Load(myPath)
environmentList = []

environmentDict = {}
# environmentDict['a'] = aClips
# environmentDict['b'] = bClips

for i in range(50):
    if i not in environmentList:
        environmentList.append(i)
        environmentDict[i] = clips.Environment()
        environmentDict.get(i).Load(myPath)


# for key, value in environmentDict.iteritems():
#     environmentDict.get(key).Load(myPath)

