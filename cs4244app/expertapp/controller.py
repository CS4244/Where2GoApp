from flask import render_template, url_for, request, redirect, Blueprint, session
import clips
import sys
import cStringIO
import os, json, time
from . import environmentList, environmentDict, enviromentUsageDict

invalidChars = ['-', ',', ' ', '.', '_']
countriesImgPath = 'http://localhost:5000/static/img/countries/'

expertapp1 = Blueprint('expertapp', __name__, template_folder='templates')

intFact = ['budget', 'daysReq']

# getting questions
# print(getQuestionInAskFact())
# test = getChoiceInAskFact()
# for i in test:
#     print i



def getDestinationFact():
    for i in environmentDict.get(session['clips']).FactList():
        if i.Relation == clips.Symbol('destination'):
            return i
    return None

def findDestinationCountFact():
    for i in environmentDict.get(session['clips']).FactList():
        if i.Relation == clips.Symbol('destinationCount'):
            return i
    return None


def printFacts():
    stdout_ = sys.stdout
    stream = cStringIO.StringIO()
    sys.stdout = stream
    environmentDict.get(session['clips']).PrintFacts()
    facts = stream.getvalue()
    sys.stdout = stdout_
    return facts


def getQuestionTypeInAskFact():
    return findAskFact().Slots['questionType']


def getSlotTypeInAskFact():
    return findAskFact().Slots['slotName']


def findAskFact():
    for i in environmentDict.get(session['clips']).FactList():
        if i.Relation == clips.Symbol('ask'):
            return i
    return None


def getQuestionInAskFact():
    return findAskFact().Slots['question']


def getChoiceInAskFact():
    return [i for i in findAskFact().Slots['choice']]


def findDesiredFact():
    for i in environmentDict.get(session['clips']).FactList()[::-1]:
        if i.Relation == clips.Symbol('desired'):
            return i

def setup():
    countryDict = {}
    for i in environmentDict.get(session['clips']).FactList():
        if i.Relation == clips.Symbol('destination'):
            countryDict[i.Slots['name']] = 0

    with open("countries.json", 'w') as outfile:
        json.dump(countryDict, outfile, indent=1)

def seleniumProcesses():
    if session['count'] == 0 and (findDesiredFact().Slots['budget'] > 0 or findDesiredFact().Slots['daysReq'] > 0):
        with open('fail.txt', 'a') as file:
            file.write(findDesiredFact().PPForm())
    if session['count'] > 1 and (not session['ask']):  # more than 1 destination and no questions remaining
        countriesDict = {}
        with open('countries.json') as file:
            countriesDict = json.load(file)

        for i in environmentDict.get(session['clips']).FactList():
            if i.Relation == clips.Symbol('destination'):
                countriesDict[i.Slots['name']] += 1
        with open("countries.json", 'w') as outfile:
            json.dump(countriesDict, outfile, indent=1)

def prepareForDisplay(destinationList):
    for i in environmentDict.get(session['clips']).FactList():
        if i.Relation == clips.Symbol('destination'):
            destinationDict = {}
            strippedInvalidName = ''.join([j for j in i.Slots['name'] if j not in invalidChars])


            destinationDict['picture'] = "img/countries/"+strippedInvalidName+".jpg"
            destinationDict['leisure'] = []
            destinationDict['waterActivity'] = []
            destinationDict['outdoorActivity'] = []
            for k in i.Slots['leisure']:
                temp = ""
                for j in k:
                    temp += j
                destinationDict['leisure'].append(temp)
            for k in i.Slots['waterActivity']:
                temp = ""
                for j in k:
                    temp += j
                destinationDict['waterActivity'].append(temp)
            for k in i.Slots['outdoorActivity']:
                temp = ""
                for j in k:
                    temp += j
                destinationDict['outdoorActivity'].append(temp)
            temp = ""
            for k in i.Slots['name']:
                temp+= k
            destinationDict['name'] = temp

            destinationList.append(destinationDict)
    print(destinationList)
@expertapp1.route('/', methods=['GET', 'POST'])  # localhost:5000/expertapp/
def index():
    if len(environmentList) == 0:
        return  render_template('begin.html', freeSlots = 0)

    if request.method == 'POST':
        if request.form['beginbtn'] == "BEGIN":
            session['clips'] = environmentList[len(environmentList) - 1]
            environmentList.pop()
            environmentDict[session['clips']].Reset()
            environmentDict[session['clips']].Run()
            enviromentUsageDict[session['clips']] = int(time.time())
            session['start'] = True
            return redirect(url_for('expertapp.question1'))

    return render_template('begin.html', freeSlots = len(environmentList))


@expertapp1.route('/end', methods=['GET', 'POST'])  # localhost:5000/expertapp/
def end():
    # session.pop('start', None)

    if request.method == 'POST':
        return redirect(url_for('expertapp.index'))
    if not ('start' in session):
        return redirect(url_for('expertapp.index'))

    factResult = printFacts().split('\n')
    for i in factResult:
        print(i)

    environmentDict.get(session['clips']).ShowGlobals()


    seleniumProcesses()

    destinationList = []
    prepareForDisplay(destinationList)

    environmentList.append(session['clips'])
    enviromentUsageDict[session['clips']] = 0
    session.clear()

    return render_template('endDraft.html', destinationList=destinationList)



@expertapp1.route('/question', methods=['GET', 'POST'])  # localhost:5000/expertapp/question1
def question1():

    if not ('start' in session):
        return redirect(url_for('expertapp.index'))
    factResult = printFacts().split('\n')
    print(len(factResult))




    if getTotalDestinationGlobal() == 0 or getTotalDestinationGlobal() == 1:
        session['count'] = getTotalDestinationGlobal()
        session['ask'] = True
        return redirect(url_for('expertapp.end'))
    if getTotalDestinationGlobal() > 1 and findAskFact() is None:
        session['count'] = getTotalDestinationGlobal()
        session['ask'] = False
        return redirect(url_for('expertapp.end'))


    # aaa = findDesiredFact()
    # tempMod1 = '(modify '+str(aaa.Index)+' (englishSpeaking "Yes"))'
    # clips.SendCommand(tempMod1)
    # clips.PrintFacts()
    # print(findDesiredFact().Slots['englishSpeaking'])
    # print(aaa.Slots.keys())
    # clips.PrintFacts()
    if request.method == 'POST':
        print(request.form)
        if (len(request.form) == 0):
            return render_template('question.html', choiceList=getChoiceInAskFact(),
                                   question=getQuestionInAskFact(),
                                   slotName=getSlotTypeInAskFact(), questionType=getQuestionTypeInAskFact(),
                                   factResult=factResult, error=True, errorMsg="Please Make A Choice")
        dictKey = list(request.form.keys())[0]
        combinedSlots = ' '
        valueList = request.form.getlist(dictKey)
        for i in valueList:
            if not dictKey in intFact:
                combinedSlots += '"' + i + '"'
            else:
                if not i.isdigit():
                    return render_template('question.html', choiceList=getChoiceInAskFact(),
                                           question=getQuestionInAskFact(),
                                           slotName=getSlotTypeInAskFact(), questionType=getQuestionTypeInAskFact(),
                                           factResult=factResult, error=True,
                                           errorMsg="Only Numeric Values Are Allowed")
                combinedSlots += i

        toModify = '(modify ' + str(findDesiredFact().Index) + ' (' + dictKey + combinedSlots + '))'
        environmentDict.get(session['clips']).SendCommand(toModify)
        findAskFact().Retract()
        environmentDict.get(session['clips']).Assert("(check" + dictKey + " on)")
        environmentDict.get(session['clips']).Run()
        # environmentDict.get(session['clips']).DebugConfig.ActivationsWatched = True
        # environmentDict.get(session['clips']).DebugConfig.FactsWatched = True
        # environmentDict.get(session['clips']).DebugConfig.RulesWatched = True
        # t = environmentDict.get(session['clips']).TraceStream.Read()
        # print t
        environmentDict.get(session['clips']).ShowGlobals()
        environmentDict.get(session['clips']).PrintFacts()
        return redirect(url_for('expertapp.question1'))
    return render_template('question.html', choiceList=getChoiceInAskFact(), question=getQuestionInAskFact(),
                           slotName=getSlotTypeInAskFact(), questionType=getQuestionTypeInAskFact(),
                           factResult=factResult)



    #
    # @expertapp.route('/question3', methods=['GET', 'POST'])  # localhost:5000/expertapp/question1
    # def question2():
    #     # return render_template('index.html')
    #     stdout_ = sys.stdout
    #     stream = cStringIO.StringIO()
    #     sys.stdout = stream
    #     clips.PrintFacts()
    #     facts = stream.getvalue()
    #     sys.stdout = stdout_
    #     if request.method == 'POST':
    #         climate = request.form['climate']
    #         fact = ''.join(["(attribute (name climate) (value ",climate, "))"])
    #         clips.Assert(fact)
    #         clips.PrintFacts()
    #         return redirect(url_for('expertapp.question3'))
    #
    #     return render_template('question2.html', title="CS4244 Where2Go", facts=facts.splitlines(),
    #                            factsCount=len(facts.splitlines()))


def getTotalDestinationGlobal():
    for i in environmentDict.get(session['clips']).GlobalList():
        if environmentDict.get(session['clips']).FindGlobal(i).Name == clips.Symbol('totalDestination'):
            # print(clips.FindGlobal(i).Name)
            return environmentDict.get(session['clips']).FindGlobal(i).Value

@expertapp1.route('/admin', methods=['GET', 'POST'])  # localhost:5000/expertapp/question1
def admin():
    if request.method == 'POST':
        if request.form['resetBtn']:
            print(request.form)
            print(request.form['resetBtn'])
            environmentList.append(int (request.form['resetBtn']))
            enviromentUsageDict[int (request.form['resetBtn'])] = 0
            print(enviromentUsageDict)
        return redirect(url_for('expertapp.admin'))


    return render_template('admin.html', environmentUsageDict= enviromentUsageDict, time = int(time.time()))