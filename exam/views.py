from django.shortcuts import render, redirect
from exam.models import FillBlank, Glossary, StudentAnswer
from exam.calculate import Calcu


def teacher(request):
    return render(request, 'exam/make-questions.html')


def edit(request):
    return render(request, 'exam/edit.html')


def training(request):

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


def update_answer(request):
    id = request.GET.get('id', 1)
    fill_blank = FillBlank.objects.get(id=id)
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
    fillBlank = FillBlank.objects.create(fbContent=question)
    fillBlank.save()
    return render(request, 'exam/new.html')
