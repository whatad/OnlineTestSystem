from django.shortcuts import render


def teacher(request):
    return render(request, 'exam/make-questions.html')


def edit(request):
    return render(request,'exam/edit.html')