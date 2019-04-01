from django.shortcuts import render, redirect
from exam.models import Question, Fillblank, X2Questions, X2Space, X2ScorePoint, X2StudentAnswer, X2Training, X2Branch, Glossary
import exam.fillblank as fillblank
import json
import exam.short_answer as SA
from django.http import HttpResponse

class DisplayBlock:
    def __init__(self):
        self.point = []
        self.score = 0
        self.mode  = 0
        self.answer  = ""
        self.percentage = 0



def teacher(request):
    return render(request, 'exam/make-questions.html')


def edit(request):
    return render(request, 'exam/edit.html')


def training(request):
    id = request.GET.get('id', 1)
    answer = int(request.GET.get('answer', 0))
    question = Question.objects.get(id=id)
    answer_list = question.answer.split(';')
    mode = '完全匹配'
    if question.judge_mode == 1:
        mode = '关键词匹配'
    elif question.judge_mode == 2:
        mode = '语义匹配'
    score_points = question.scorepoint_set.all()

    student_answers = question.studentanswer_set.all()
    student_answer = ''
    if student_answers.count() > 0:
        student_answer = student_answers[answer].answer
    student_answer_list = student_answer.split(';')
    while len(student_answer_list) < len(answer_list):
        student_answer_list.append('')

    score_list = []
    detail_list = []
    points_list = []

    for i in range(len(answer_list)):
        position_list = list(score_points.filter(position=i+1).order_by('sub_no'))
        #points_list.append(position_list)           #未区分sub
        key_list = []
        key_dict = {}
        sub_no = 1
        for point in position_list:
            if point.sub_no != sub_no:
                key_list.append(key_dict)
                key_dict = {}
            key_dict[point.content] = point.percentage
        key_list.append(key_dict)
        points_list.append(key_list)
        score, detail = fillblank.mark(question.judge_mode, answer_list[i], student_answer_list[i], key_list)
        score_list.append(score)
        detail_list.extend(detail)
    return render(request, 'exam/test-training.html', {'question': question, 'answer_list': answer_list,
                                                       'mode': mode, 'points': points_list,
                                                       'student_answer': student_answer, 'score': score_list,
                                                       'detail':detail_list})

def fillblank_train(request):
    no = int(request.GET.get('no', 65874))
    answer = int(request.GET.get('answer', 0))

    #x2question = X2Questions.objects.filter(questiontype=5)[no]
    x2question = X2Questions.objects.get(questionid=no)

    answer_list = x2question.questionanswer.split(';')

    space_list = x2question.x2space_set.all()

    student_answers = x2question.x2studentanswer_set.all()
    student_answer = None
    student_answer_list=[]
    if student_answers.count() > answer:
        student_answer = student_answers[answer]
        student_answer_list = student_answer.content.split(';')
    while len(student_answer_list) < len(space_list):
        student_answer_list.append('')

    score_list = []
    display_list = []
    total_score = 0.0
    for i in range(len(space_list)):
        display_block = DisplayBlock()
        display_block.mode = space_list[i].mode
        display_block.score = space_list[i].score

        score_points = space_list[i].x2scorepoint_set.all().order_by('no')
        key_list = []
        key_dict = {}
        display_dict = {}
        no = 1
        for point in score_points:
            if point.no != no:
                key_list.append(key_dict)
                display_block.point.append(display_dict)
                key_dict = {}
                display_dict = {}
            if space_list[i].mode == 2:
                display_dict[Glossary.objects.get(id=point.content).word] = point.percentage
            else:
                display_dict[point.content] = point.percentage
            key_dict[point.content] = point.percentage
        key_list.append(key_dict)
        display_block.point.append(display_dict)

        score, detail = fillblank.mark(space_list[i].mode, answer_list[i], student_answer_list[i], key_list)

        total_score += score* 0.01 * space_list[i].score

        display_block.answer = student_answer_list[i]
        display_block.percentage = score

        score_list.append(score)
        display_list.append(display_block)

    return render(request, 'exam/fillblank.html', {'question': x2question, 'displays': display_list, 'total_score': total_score,
                                                   'answer': student_answer, 'answer_no': answer})


def update_question(request):
    if request.method == 'POST':
        question_id = request.POST.get("question_id")
        level_name = request.POST.get("level_name")
        level = request.POST.get("level")
        question = X2Questions.objects.get(questionid=question_id)
        question.questionlevel_name = level_name
        question.questionlevel = level
        question.save()
        return HttpResponse(json.dumps({
            "level": level
        }))

def update_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get("question_id")
        answer = request.POST.get("answer")
        question = X2Questions.objects.get(questionid=question_id)
        question.questionanswer = answer
        question.save()
        return HttpResponse(json.dumps({
            "answer": answer
        }))

def update_points(request):
    if request.method == 'POST':
        question_id = request.POST.get("question_id")
        space_position = request.POST.get("space")
        mode = request.POST.get('mode')
        points_str = request.POST.get("points")
        points= json.loads(points_str)
        question = X2Questions.objects.get(questionid=question_id)
        space = question.x2space_set.get(position=space_position)
        space.mode = int(mode)
        space.x2scorepoint_set.all().delete()
        space.save()
        for no in range(len(points)):
            points_dict = json.loads(points[no])
            for key in points_dict.keys():
                if key.strip() != "" and is_number(points_dict[key].strip()):
                    point = X2ScorePoint.objects.create(space=space, content=key, percentage=float(points_dict[key]), no=(no+1))
                    point.save()
        return HttpResponse()

def update_score(request):
    if request.method == 'POST':
        answer_id = int(request.POST.get("answer_id"))
        total_score = float(request.POST.get("totalScore"))
        stu_answer = X2StudentAnswer.objects.get(id=answer_id)
        stu_answer.score = total_score
        stu_answer.save()
    return HttpResponse()


def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False


def short_answer_train(request):
    no = int(request.GET.get('no', 72478))
    answer = int(request.GET.get('answer', 0))

    # x2question = X2Questions.objects.filter(questiontype=5)[no]
    x2question = X2Questions.objects.get(questionid=no)

    branch_list = x2question.x2branch_set.all()

    stu_answer = x2question.x2studentanswer_set.all()[answer]
    answer_list = stu_answer.content.split(';')
    if len(answer_list) < len(branch_list):
        answer_list.append("")

    branch_train = []
    score_list = []
    total_score = 0
    for i in range(len(branch_list)):
        tranings = branch_list[i].x2training_set.all()
        branch_dict = {}
        for training in tranings:
            branch_dict[training.content] = training.percentage
        branch_train.append(branch_dict)
        score = round(SA.colicTest(branch_dict, answer_list[i]),2)
        score_list.append(score)
        total_score += score * 0.01 * branch_list[i].score


    display_list = []
    for i in range(len(branch_list)):
        display = DisplayBlock()
        display.answer = answer_list[i]
        display.score = branch_list[i].score
        display.point = branch_train[i]
        display.percentage = score_list[i]
        display_list.append(display)

    return render(request, 'exam/short_answer.html', {'question': x2question, 'displays': display_list,
                                                      "total_score": round(total_score,2), 'stu_answer':stu_answer,
                                                      'answer_no': answer})

def update_branch(request):
    if request.method == 'POST':
        question_id = request.POST.get("question_id")
        branch_position = request.POST.get("branch")
        trains_str = request.POST.get("trains")
        trains= json.loads(trains_str)
        question = X2Questions.objects.get(questionid=question_id)
        branch = question.x2branch_set.get(position=branch_position)
        branch.x2training_set.all().delete()
        for key in trains.keys():
            if key.strip() != "" and is_number(trains[key].strip()):
                train = X2Training.objects.create(branch=branch, content=key, percentage=float(trains[key]))
                train.save()
        return HttpResponse()

def saveTraining(request):
    if request.method == 'POST':
        question_id = request.POST.get("question_id")
        trains_str = request.POST.get("trains")
        trains = json.loads(trains_str)
        question = X2Questions.objects.get(questionid=question_id)
        branches = question.x2branch_set.all().order_by('position')
        i = 0
        for key in trains.keys():
            if key.strip() != "" and is_number(trains[key].strip()):
                train = X2Training.objects.create(branch=branches[i], content=key, percentage=float(trains[key]))
                train.save()
                i += 1
    return HttpResponse()

def add_question(request):

    return render(request, 'exam/add_question.html')

def test(request):
    title = request.POST.get("title")
    subject = request.POST.get("subject")
    type = request.POST.get("type")
    answer = request.POST.get("answer")
    level = request.POST.get("level")
    mode_list = request.POST.getlist("mode")
    score_list = request.POST.getlist("score")
    point_list = request.POST.getlist("point")
    scoreb_list = request.POST.getlist("scoreb")
    branch_list = request.POST.getlist("branch")
    if title != None and type != None:
        question = X2Questions.objects.create()
        question.question = title
        question.subjectid = int(subject)
        question.questiontype = int(type)
        question.questionanswer = answer
        question.questionlevel = int(level)
        question.save()
        if type == '5':
            for i in range(len(mode_list)):
                space = X2Space.objects.create(mode=int(mode_list[i]), position=(i+1))
                space.question = question
                space.score = float(score_list[i])
                space.save()
                points = point_list[i].split('\n')
                for j in range(len(points)):
                    words = points[j].strip().split(';')
                    for word in words:
                        kav = word.split(" ")
                        if kav[0].strip() != "" and is_number(kav[1].strip()):
                            score_point = X2ScorePoint.objects.create(content=kav[0], percentage=kav[1], no=(j+1), space=space)
                            score_point.save()
        elif type == '6':
            for i in range(len(scoreb_list)):
                branch = X2Branch.objects.create()
                branch.score = float(scoreb_list[i])
                branch.position = i+1
                branch.question = question
                branch.save()
                kav = branch_list[i].split(" ")
                if kav[0].strip() != "" and is_number(kav[1].strip()):
                    train = X2Training.objects.create()
                    train.branch = branch
                    train.content = kav[0]
                    train.percentage = kav[1]
                    train.save()

    return render(request, 'exam/add_question.html')

def get_concepts(request):
    word_str = request.POST.get("words")
    print(word_str)
    word_list = word_str.split(";")
    concepts = set()
    for word in word_list:
        if word.strip() != "":
            concepts = concepts.union(fillblank.get_concept_set(word))
    concept_list = []
    for concept in concepts:
        concept_dict = {}
        concept_dict['id'] = concept.id
        concept_dict['word'] = concept.word
        concept_dict['type'] = concept.type
        concept_dict['concept'] = concept.concept
        concept_list.append(json.dumps(concept_dict))

    return HttpResponse(json.dumps({
            "concept_list": concept_list
        }))
