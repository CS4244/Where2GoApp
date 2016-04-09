from flask import render_template, url_for, request, redirect, Blueprint
import clips
import sys
import cStringIO
import os

expertapp = Blueprint('expertapp', __name__, template_folder='templates')

stdout_ = sys.stdout  # Keep track of the previous value.

    #getting questions
    # print(getQuestionInAskFact())
    # test = getChoiceInAskFact()
    # for i in test:
    #     print i



def findAskFact():
    for i in clips.FactList():
        if i.Relation == clips.Symbol('ask'):
            return i
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
    if request.method == 'POST':
        if request.form['beginbtn'] == "BEGIN":
            return redirect(url_for('expertapp.question1'))

    return render_template('begin.html')


@expertapp.route('/question1', methods=['GET', 'POST'])  # localhost:5000/expertapp/question1
def question1():
    qnId = 1
    clips.PrintFacts()



    # print(cc.__dict__)
    # print(cc.Index)
    # print(cc._Fact__fact)
    # print(cc.Slots.keys())
    # print cc.Slots['outdoorActivity']
    # clips.Assert("(duck)")
    # clips.Assert("(man)")
    # clips.Assert("(woman)")
    aaa = findDesiredFact()
    tempMod1 = '(modify '+str(aaa.Index)+' (englishSpeaking "Yes"))'
    clips.SendCommand(tempMod1)
    clips.PrintFacts()
    print(findDesiredFact().Slots['englishSpeaking'])
    # print(aaa.Slots.keys())
    clips.PrintFacts()

    # tt = clips.FactList()[-1]
    # print(tt.__dict__)
    # print(tt.PPForm())
    # print(tt.Relation)
    # print(type(tt.Relation))
    # sdf = clips.Symbol('desired')
    # print(type(sdf))
    # if sdf == tt.Relation:
    #     print("yesss")
    # else:
    #     print("NOOO")
    #
    # print(tt.__dict__)
    # print(tt._Fact__fact)
    # print(cc.Index)
    if request.method == 'POST':
        budget = request.form['budget']
        fact = ''.join(["(attribute (name budget) (value ",budget, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        # return redirect(url_for('expertapp.question2'))
    return render_template('question1.html', qnId = qnId)

@expertapp.route('/question2', methods=['GET', 'POST'])  # localhost:5000/expertapp/question2
def question2():
    qnId = 2
    clips.PrintFacts()
    if request.method == 'POST':
        climate = request.form['climate']
        fact = ''.join(["(attribute (name climate) (value ",climate, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question3'))

    return render_template('question2.html', qnId = qnId)

@expertapp.route('/question3', methods=['GET', 'POST'])  # localhost:5000/expertapp/question3
def question3():
    qnId = 3
    clips.PrintFacts()
    if request.method == 'POST':
        englishSpeaker = request.form['english']
        fact = ''.join(["(attribute (name english) (value ",englishSpeaker, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question4'))

    return render_template('question3.html', qnId = qnId)

@expertapp.route('/question4', methods=['GET', 'POST'])  # localhost:5000/expertapp/question4
def question4():
    qnId = 4 #set the question number in the html
    clips.PrintFacts()
    if request.method == 'POST':
        visit = request.form['visit']
        fact = ''.join(["(attribute (name visit) (value ",visit, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question5'))

    return render_template('question4.html', qnId = qnId)

@expertapp.route('/question5', methods=['GET', 'POST'])  # localhost:5000/expertapp/question4
def question5():
    qnId = 5 #set the question number in the html
    clips.PrintFacts()
    if request.method == 'POST':
        indoorActivity = request.form['indoorActivity']
        fact = ''.join(["(attribute (name indoorActivity) (value ",indoorActivity, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question6'))

    return render_template('question5.html', qnId = qnId)

@expertapp.route('/question6', methods=['GET', 'POST'])  # localhost:5000/expertapp/question4
def question6():
    qnId = 6 #set the question number in the html
    clips.PrintFacts()
    if request.method == 'POST':
        outdoorActivity = request.form['outdoorActivity']
        fact = ''.join(["(attribute (name outdoorActivity) (value ",outdoorActivity, "))"])
        clips.Assert(fact)
        clips.PrintFacts()
        return redirect(url_for('expertapp.question7'))

    return render_template('question6.html', qnId = qnId)

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