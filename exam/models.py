from django.db import models
from tinymce.models import HTMLField
import tinymce


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

'''
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
    sub_no = models.IntegerField(blank=True, null=True)

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


class X2Questions(models.Model):
    questionid = models.AutoField(primary_key=True)
    questionid_xh = models.CharField(max_length=4, blank=True, null=True)
    questiontype = models.IntegerField(blank=True, null=True)
    questiontype_char = models.CharField(max_length=120, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    questionuserid = models.IntegerField(blank=True, null=True)
    questionusername = models.CharField(max_length=120, blank=True, null=True)
    questionlastmodifyuser = models.CharField(max_length=120, blank=True, null=True)
    questionselect = models.TextField(blank=True, null=True)
    questionselectnumber = models.IntegerField(blank=True, null=True)
    questionanswer = models.TextField(blank=True, null=True)
    questiondescribe = models.TextField(blank=True, null=True)
    questionknowsid = models.CharField(max_length=1000, blank=True, null=True)
    questionknowsid_new = models.CharField(max_length=1000, blank=True, null=True)
    questioncreatetime = models.IntegerField(blank=True, null=True)
    questionstatus = models.IntegerField(blank=True, null=True)
    questionhtml = models.TextField(blank=True, null=True)
    questionparent = models.IntegerField(blank=True, null=True)
    questionsequence = models.IntegerField(blank=True, null=True)
    questionlevel = models.IntegerField(blank=True, null=True)
    questionlevel_name = models.CharField(max_length=20, blank=True, null=True)
    subjectid = models.IntegerField(blank=True, null=True)
    subjectid_name = models.CharField(max_length=20, blank=True, null=True)
    levelid = models.IntegerField(blank=True, null=True)
    levelname = models.CharField(max_length=6, blank=True, null=True)
    knowscode = models.CharField(max_length=100, blank=True, null=True)
    questionpicture = models.CharField(max_length=60, blank=True, null=True)
    backpicture = models.CharField(max_length=60, blank=True, null=True)
    timeid = models.IntegerField(blank=True, null=True)
    timename = models.CharField(max_length=20, blank=True, null=True)
    times = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    solution = models.IntegerField(blank=True, null=True)
    usertype = models.IntegerField(blank=True, null=True)
    draw_pic = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x2_questions'


class X2ScorePoint(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=300)
    space = models.ForeignKey('X2Space', models.DO_NOTHING, db_column='space', blank=True, null=True)
    percentage = models.FloatField()
    no = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'x2_score_point'


class X2Space(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(X2Questions, models.DO_NOTHING, db_column='question', blank=True, null=True)
    mode = models.IntegerField()
    position = models.IntegerField()
    score = models.FloatField(default=0)

    class Meta:
        managed = False
        db_table = 'x2_space'


class X2StudentAnswer(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(X2Questions, models.DO_NOTHING, db_column='question', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x2_student_answer'
'''
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
    sub_no = models.IntegerField(blank=True, null=True)

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


class X2Branch(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey('X2Questions', models.DO_NOTHING, db_column='question', blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x2_branch'


class X2Questions(models.Model):
    questionid = models.AutoField(primary_key=True)
    questionid_xh = models.CharField(max_length=4, blank=True, null=True)
    questiontype = models.IntegerField(blank=True, null=True)
    questiontype_char = models.CharField(max_length=120, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    questionuserid = models.IntegerField(blank=True, null=True)
    questionusername = models.CharField(max_length=120, blank=True, null=True)
    questionlastmodifyuser = models.CharField(max_length=120, blank=True, null=True)
    questionselect = models.TextField(blank=True, null=True)
    questionselectnumber = models.IntegerField(blank=True, null=True)
    questionanswer = models.TextField(blank=True, null=True)
    questiondescribe = models.TextField(blank=True, null=True)
    questionknowsid = models.CharField(max_length=1000, blank=True, null=True)
    questionknowsid_new = models.CharField(max_length=1000, blank=True, null=True)
    questioncreatetime = models.IntegerField(blank=True, null=True)
    questionstatus = models.IntegerField(blank=True, null=True)
    questionhtml = models.TextField(blank=True, null=True)
    questionparent = models.IntegerField(blank=True, null=True)
    questionsequence = models.IntegerField(blank=True, null=True)
    questionlevel = models.IntegerField(blank=True, null=True)
    questionlevel_name = models.CharField(max_length=20, blank=True, null=True)
    subjectid = models.IntegerField(blank=True, null=True)
    subjectid_name = models.CharField(max_length=20, blank=True, null=True)
    levelid = models.IntegerField(blank=True, null=True)
    levelname = models.CharField(max_length=6, blank=True, null=True)
    knowscode = models.CharField(max_length=100, blank=True, null=True)
    questionpicture = models.CharField(max_length=60, blank=True, null=True)
    backpicture = models.CharField(max_length=60, blank=True, null=True)
    timeid = models.IntegerField(blank=True, null=True)
    timename = models.CharField(max_length=20, blank=True, null=True)
    times = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    solution = models.IntegerField(blank=True, null=True)
    usertype = models.IntegerField(blank=True, null=True)
    draw_pic = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x2_questions'


class X2ScorePoint(models.Model):
    content = models.CharField(max_length=300)
    space = models.ForeignKey('X2Space', models.DO_NOTHING, db_column='space', blank=True, null=True)
    percentage = models.FloatField()
    no = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'x2_score_point'


class X2Space(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(X2Questions, models.DO_NOTHING, db_column='question', blank=True, null=True)
    mode = models.IntegerField()
    position = models.IntegerField()
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x2_space'


class X2StudentAnswer(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(X2Questions, models.DO_NOTHING, db_column='question', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x2_student_answer'


class X2Training(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    branch = models.ForeignKey(X2Branch, models.DO_NOTHING, db_column='branch', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x2_training'
