from flask import render_template, url_for, request, redirect, Blueprint, session
import clips
import sys
import cStringIO
import os

expertapp = Blueprint('expertapp', __name__, template_folder='templates')

intFact = ['budget', 'daysReq']

# getting questions
# print(getQuestionInAskFact())
# test = getChoiceInAskFact()
# for i in test:
#     print i

def printFacts():
    stdout_ = sys.stdout
    stream = cStringIO.StringIO()
    sys.stdout = stream
    clips.PrintFacts()
    facts = stream.getvalue()
    sys.stdout = stdout_
    return facts


def getQuestionTypeInAskFact():
    return findAskFact().Slots['questionType']


def getSlotTypeInAskFact():
    return findAskFact().Slots['slotName']


def findAskFact():
    for i in clips.FactList():
        if i.Relation == clips.Symbol('ask'):
            return i
    return None


def getQuestionInAskFact():
    return findAskFact().Slots['question']


def getChoiceInAskFact():
    return [i for i in findAskFact().Slots['choice']]


def findDesiredFact():
    for i in clips.FactList()[::-1]:
        if i.Relation == clips.Symbol('desired'):
            return i


@expertapp.route('/', methods=['GET', 'POST'])  # localhost:5000/expertapp/
def index():
    clips.Reset()
    clips.Run()
    if request.method == 'POST':
        if request.form['beginbtn'] == "BEGIN":
            session['start'] = True
            return redirect(url_for('expertapp.question1'))

    return render_template('begin.html')


@expertapp.route('/end', methods=['GET', 'POST'])  # localhost:5000/expertapp/
def end():
    session.pop('start', None)
    factResult = printFacts().split('\n')
    clips.ShowGlobals()
    if request.method == 'POST':
        return redirect(url_for('expertapp.index'))
    return render_template('end.html', factResult=factResult)


@expertapp.route('/question', methods=['GET', 'POST'])  # localhost:5000/expertapp/question1
def question1():
    factResult = printFacts().split('\n')
    print(len(factResult))

    if findAskFact() is None:
        return redirect(url_for('expertapp.end'))
    if not ('start' in session):
        return redirect(url_for('expertapp.index'))

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
        clips.SendCommand(toModify)
        findAskFact().Retract()
        clips.Assert("(check" + dictKey + " on)")
        clips.Run()
        clips.DebugConfig.ActivationsWatched = True
        clips.DebugConfig.FactsWatched = True
        clips.DebugConfig.RulesWatched = True
        t = clips.TraceStream.Read()
        print t
        clips.ShowGlobals()
        clips.PrintFacts()
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
