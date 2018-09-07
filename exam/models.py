from django.db import models
from tinymce.models import HTMLField
import tinymce


# 学生表（学生编号，姓名，密码）
class Student(models.Model):
    stuId = models.CharField(max_length=20, verbose_name=u'编号')
    stuName = models.CharField(max_length=20, verbose_name=u'登录名')
    stuPassword = models.CharField(max_length=30, verbose_name=u'登录密码')


# 老师表（老师编号，姓名，密码）
class Teacher(models.Model):
    teaId = models.CharField(max_length=20, verbose_name=u'编号')
    teaName = models.CharField(max_length=20, verbose_name=u'登录名')
    teaPassword = models.CharField(max_length=30, verbose_name=u'登录密码')


# 管理员表（管理员编号，姓名，密码）
class Admin(models.Model):
    admId = models.CharField(max_length=20, verbose_name=u'编号')
    admName = models.CharField(max_length=20, verbose_name=u'登录名')
    admPassword = models.CharField(max_length=30, verbose_name=u'登录密码')


'''
# 单选题表（科目类别，题干，选项A，选项B，选项C，选项D，答案）
class SingleChoice(models.Model):
    scCourse = models.CharField(max_length=30)
    scContent = models.CharField(max_length=200)
    # scImg = models.ImageField(null=True)
    scOpA = models.CharField(max_length=50)
    scOpB = models.CharField(max_length=50)
    scOpC = models.CharField(max_length=50)
    scOpD = models.CharField(max_length=50)
    scAnswer = models.CharField(max_length=2)


# 判断题（科目类别，题干，答案）
class Judgement(models.Model):
    judCourse = models.CharField(max_length=20)
    judContent = models.CharField(max_length=100)
    judAnswer = models.BooleanField()
'''


# 填空题（科目类别，难度[A,B,C]，题干，答案） 最多有十个填空
class FillBlank(models.Model):
    fbCourse = models.CharField(max_length=20, verbose_name=u'科目类别')
    fbGrade = models.CharField(max_length=5, verbose_name=u'难度等级')
    fbContent = models.CharField(max_length=200, verbose_name=u'题目内容')
    #同个空格不同答案通过空格隔开，不同空格通过'\n'隔开
    fbAnswer = models.CharField(max_length=300, null=True, verbose_name=u'填空答案')
    fbScore = models.FloatField(null=True, verbose_name=u'分数')
    alpha = models.FloatField(default=1.6, verbose_name=u'参数')
    beta1 = models.FloatField(default=0.5, verbose_name=u'参数')
    beta2 = models.FloatField(default=0.2, verbose_name=u'参数')
    beta3 = models.FloatField(default=0.17, verbose_name=u'参数')
    beta4 = models.FloatField(default=0.13, verbose_name=u'参数')
    '''
    fbAnswer2 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空2答案')
    fbAnswer3 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空3答案')
    fbAnswer4 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空4答案')
    fbAnswer5 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空5答案')
    fbAnswer6 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空6答案')
    fbAnswer7 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空7答案')
    fbAnswer8 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空8答案')
    fbAnswer9 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空9答案')
    fbAnswer10 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空10答案')
    '''


# 简答题（科目类别，难度[A,B,C]，题干，答案）
class ShortAnswer(models.Model):
    saCourse = models.CharField(max_length=20, verbose_name=u'科目类别')
    saGrade = models.CharField(max_length=5, verbose_name=u'难度等级')
    saContent = models.CharField(max_length=200, verbose_name=u'题目内容')
    saAnswer = models.TextField(max_length=500, verbose_name=u'答案')


class Glossary(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=20, verbose_name=u'词语')
    type = models.CharField(max_length=15, verbose_name=u'词性')
    sememes = models.CharField(max_length=200, verbose_name=u'义原')


class StudentAnswer(models.Model):
    id = models.IntegerField(primary_key=True)
    fillBlankId = models.IntegerField(default=0)
    answer = models.CharField(max_length=300, verbose_name=u'学生答案')
    score = models.FloatField(default=0)



#python manage.py makemigrations
#python manage.py migrate


