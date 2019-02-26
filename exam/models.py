from django.db import models
from tinymce.models import HTMLField
import tinymce

'''
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


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    type = models.CharField(max_length=20, blank=True, null=True)
    choose = models.TextField(blank=True, null=True)
    tips = models.CharField(max_length=300, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    course_name = models.CharField(max_length=20, blank=True, null=True)
    chapter_no = models.CharField(max_length=20, blank=True, null=True)
    chapter_name = models.CharField(max_length=30, blank=True, null=True)
    knowledge_point_no = models.CharField(max_length=20, blank=True, null=True)
    judge_mode = models.IntegerField()

class ScorePoint(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=300, blank=False, null=False)
    question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.SET_NULL)
    percentage = models.FloatField(default=0)
    position = models.IntegerField(default=1)
'''


#python manage.py makemigrations
#python manage.py migrate

#python manage.py inspectdb >> exam/models.py

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ExamAdmin(models.Model):
    admid = models.CharField(db_column='admId', max_length=20)  # Field name made lowercase.
    admname = models.CharField(db_column='admName', max_length=20)  # Field name made lowercase.
    admpassword = models.CharField(db_column='admPassword', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'exam_admin'


class Fillblank(models.Model):
    fbcourse = models.CharField(db_column='fbCourse', max_length=20)  # Field name made lowercase.
    fbgrade = models.CharField(db_column='fbGrade', max_length=5)  # Field name made lowercase.
    fbcontent = models.CharField(db_column='fbContent', max_length=200)  # Field name made lowercase.
    fbanswer = models.CharField(db_column='fbAnswer', max_length=300, blank=True, null=True)  # Field name made lowercase.
    fbscore = models.FloatField(db_column='fbScore', blank=True, null=True)  # Field name made lowercase.
    alpha = models.FloatField()
    beta1 = models.FloatField()
    beta2 = models.FloatField()
    beta3 = models.FloatField()
    beta4 = models.FloatField()

    class Meta:
        managed = False
        db_table = 'fillblank'


class Glossary(models.Model):
    word = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    sememes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glossary'


class Question(models.Model):
    title = models.TextField()
    type = models.CharField(max_length=20, blank=True, null=True)
    choose = models.TextField(blank=True, null=True)
    tips = models.CharField(max_length=300, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    course_name = models.CharField(max_length=20, blank=True, null=True)
    chapter_no = models.CharField(max_length=20, blank=True, null=True)
    chapter_name = models.CharField(max_length=30, blank=True, null=True)
    knowledge_point_no = models.CharField(max_length=20, blank=True, null=True)
    judge_mode = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'question'


class ScorePoint(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=300)
    question = models.ForeignKey(Question, models.DO_NOTHING, db_column='question', blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    sub_no = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'score_point'


class ShortAnswer(models.Model):
    sacourse = models.CharField(db_column='saCourse', max_length=20)  # Field name made lowercase.
    sagrade = models.CharField(db_column='saGrade', max_length=5)  # Field name made lowercase.
    sacontent = models.CharField(db_column='saContent', max_length=200)  # Field name made lowercase.
    saanswer = models.TextField(db_column='saAnswer')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'short_answer'


class Student(models.Model):
    stuid = models.CharField(db_column='stuId', max_length=20)  # Field name made lowercase.
    stuname = models.CharField(db_column='stuName', max_length=20)  # Field name made lowercase.
    stupassword = models.CharField(db_column='stuPassword', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student'


class StudentAnswer(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, models.DO_NOTHING, db_column='question', blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    score = models.FloatField()

    class Meta:
        managed = False
        db_table = 'student_answer'


class Teacher(models.Model):
    teaid = models.CharField(db_column='teaId', max_length=20)  # Field name made lowercase.
    teaname = models.CharField(db_column='teaName', max_length=20)  # Field name made lowercase.
    teapassword = models.CharField(db_column='teaPassword', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teacher'
