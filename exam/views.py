from django.shortcuts import render, redirect
from exam.models import Question, Fillblank, Glossary, StudentAnswer
import exam.fillblank as fillblank
from exam.calculate import Calcu


def teacher(request):
    return render(request, 'exam/make-questions.html')


def edit(request):
    return render(request, 'exam/edit.html')


def training(request):
    id = request.GET.get('id', 1)
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
        student_answer = student_answers[0].answer
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

    '''
    id = request.GET.get('id', 1)
    fill_blank = FillBlank.objects.get(id=id)
    finds = Glossary.objects.filter(word=fill_blank.fbAnswer)
    concepts = [find.sememes for find in finds]
    student_answers = StudentAnswer.objects.filter(fillBlankId=id)
    answer_id = int(request.GET.get('student', 0))
    answer = ""
    stu_concepts = []
    sim = 0
    if student_answers.count() > answer_id:
        student_answer = student_answers[answer_id]
        answer = student_answer.answer
        finds = Glossary.objects.filter(word=answer)
        stu_concepts = [find.sememes for find in finds]

        request.session["alpha"] = fill_blank.alpha
        request.session["beta1"] = fill_blank.beta1
        request.session["beta2"] = fill_blank.beta2
        request.session["beta3"] = fill_blank.beta3
        request.session["beta4"] = fill_blank.beta4

        calcu = Calcu(fill_blank.alpha, fill_blank.beta1, fill_blank.beta2,
                      fill_blank.beta3, fill_blank.beta4)
        calcu.init_sem_list("static/whole.dat")
        sim = calcu.cal_word_sim(fill_blank.fbAnswer, answer)

    return render(request, 'exam/test-training.html', {'fillBlank': fill_blank, 'questionId': id,
                                                       'concepts': concepts, 'answer': answer,
                                                       'stuConcepts': stu_concepts, 'sim': sim,
                                                       'studentAnswerId': answer_id})
    '''


def update_answer(request):
    id = request.GET.get('id', 1)
    fill_blank = Fillblank.objects.get(id=id)
    fill_blank.alpha = request.GET['alpha']
    fill_blank.beta1 = request.GET['beta1']
    fill_blank.beta2 = request.GET['beta2']
    fill_blank.beta3 = request.GET['beta3']
    fill_blank.beta4 = request.GET['beta4']
    fill_blank.fbAnswer = request.GET['answer']
    fill_blank.save()
    return redirect('/exam/training/?id='+request.GET['id']+'&&student='+request.GET['answerId'])


def add(request):
    question = request.POST['question']
    analysis = request.POST['analysis']
    num = request.POST['number']
    fillBlank = Fillblank.objects.create(fbContent=question)
    fillBlank.save()
    return render(request, 'exam/new.html')
