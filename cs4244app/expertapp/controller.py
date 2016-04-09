from flask import render_template, url_for, request, redirect, Blueprint
import clips
import sys
import cStringIO
import os

qnId = 1

expertapp = Blueprint('expertapp', __name__, template_folder='templates')

stdout_ = sys.stdout  # Keep track of the previous value.

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


def isQuestionTypeRadioInAskFact():
    questionType = findAskFact().Slots['questionType']
    if questionType == "RADIO":
        return True
    return False


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
    qnId = 1
    clips.Reset()
    clips.Run()
    if request.method == 'POST':
        if request.form['beginbtn'] == "BEGIN":
            return redirect(url_for('expertapp.question1'))

    return render_template('begin.html')

@expertapp.route('/end', methods=['GET', 'POST'])  # localhost:5000/expertapp/
def end():
    factResult = printFacts().split('\n')
    if request.method == 'POST':
        return redirect(url_for('expertapp.index'))
    return render_template('end.html', factResult = factResult)


@expertapp.route('/question', methods=['GET', 'POST'])  # localhost:5000/expertapp/question1
def question1():
    global qnId
    factResult = printFacts().split('\n')

    if findAskFact() is None:
        return redirect(url_for('expertapp.end'))


    # aaa = findDesiredFact()
    # tempMod1 = '(modify '+str(aaa.Index)+' (englishSpeaking "Yes"))'
    # clips.SendCommand(tempMod1)
    # clips.PrintFacts()
    # print(findDesiredFact().Slots['englishSpeaking'])
    # print(aaa.Slots.keys())
    # clips.PrintFacts()

    if request.method == 'POST':
        qnId += 1
        print(request.form)
        dictKey = list(request.form.keys())[0]
        combinedSlots = ' '
        valueList = request.form.getlist(dictKey)
        for i in valueList:
            combinedSlots += '"' + i + '"'
        toModify = '(modify ' + str(findDesiredFact().Index) + ' (' + dictKey + combinedSlots + '))'
        clips.SendCommand(toModify)
        findAskFact().Retract()
        clips.Assert("(check"+dictKey+" on)")
        clips.Run()
        return redirect(url_for('expertapp.question1'))
    return render_template('question.html', qnId=qnId, choiceList=getChoiceInAskFact(), question=getQuestionInAskFact(),
                           slotName=getSlotTypeInAskFact(), questionType=isQuestionTypeRadioInAskFact(),
                           factResult=factResult)


@expertapp.route('/question2', methods=['GET', 'POST'])  # localhost:5000/expertapp/question2
def question2():
    qnId = 2
    clips.PrintFacts()
    if request.method == 'POST':
        climate = request.form['climate']
        fact = ''.join(["(attribute (name climate) (value ", climate, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question3'))

    return render_template('question2.html', qnId=qnId)


@expertapp.route('/question3', methods=['GET', 'POST'])  # localhost:5000/expertapp/question3
def question3():
    qnId = 3
    clips.PrintFacts()
    if request.method == 'POST':
        englishSpeaker = request.form['english']
        fact = ''.join(["(attribute (name english) (value ", englishSpeaker, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question4'))

    return render_template('question3.html', qnId=qnId)


@expertapp.route('/question4', methods=['GET', 'POST'])  # localhost:5000/expertapp/question4
def question4():
    qnId = 4  # set the question number in the html
    clips.PrintFacts()
    if request.method == 'POST':
        visit = request.form['visit']
        fact = ''.join(["(attribute (name visit) (value ", visit, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question5'))

    return render_template('question4.html', qnId=qnId)


@expertapp.route('/question5', methods=['GET', 'POST'])  # localhost:5000/expertapp/question4
def question5():
    qnId = 5  # set the question number in the html
    clips.PrintFacts()
    if request.method == 'POST':
        indoorActivity = request.form['indoorActivity']
        fact = ''.join(["(attribute (name indoorActivity) (value ", indoorActivity, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question6'))

    return render_template('question5.html', qnId=qnId)


@expertapp.route('/question6', methods=['GET', 'POST'])  # localhost:5000/expertapp/question4
def question6():
    qnId = 6  # set the question number in the html
    clips.PrintFacts()
    if request.method == 'POST':
        outdoorActivity = request.form['outdoorActivity']
        fact = ''.join(["(attribute (name outdoorActivity) (value ", outdoorActivity, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question7'))

    return render_template('question6.html', qnId=qnId)

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
