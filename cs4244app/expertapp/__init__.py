import clips, os

currentPath = os.path.dirname(os.path.realpath(__file__))
clips.Load("".join((currentPath, '\CLP\data.clp')))
clips.Reset()
clips.Run()