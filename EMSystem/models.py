from django.db import models

# Create your models here.
class S(models.Model):                                                     # 学生表
    xh = models.CharField(max_length=32, unique=True, primary_key=True)    # 学号（主键）
    xm = models.CharField(max_length=32)                                   # 姓名
    xb = models.CharField(max_length=4)                                    # 性别
    csrq = models.DateField()                                              # 出生日期
    jg = models.CharField(max_length=32)                                   # 籍贯
    sjhm = models.CharField(max_length=32, unique=True)                    # 手机号码
    yxh = models.CharField(max_length=8)                                   # 院系号


class D(models.Model):                                                     # 院系表
    yxh = models.CharField(max_length=8, primary_key=True)                 # 院系号
    yxm = models.CharField(max_length=32)                                  # 院系名称
    lxdh = models.CharField(max_length=32, unique=True)                    # 联系电话
    dz = models.CharField(max_length=64)                                   # 地址


class T(models.Model):
    gh = models.CharField(max_length=32, unique=True, primary_key=True)    # 工号
    xm = models.CharField(max_length=32)                                   # 姓名
    xb = models.CharField(max_length=4)                                    # 性别
    csrq = models.DateField()                                              # 出生日期
    xl = models.CharField(max_length=32)                                   # 学历
    gz = models.FloatField()                                               # 工资
    yxh = models.CharField(max_length=8)                                   # 院系号
    pf = models.FloatField()                                               # 评分

class C(models.Model):
    xq = models.CharField(max_length=32)                 # 学期
    kh = models.CharField(max_length=32)                 # 课号
    km = models.CharField(max_length=32)                 # 课名
    xf = models.IntegerField()                                             # 学分
    xs = models.IntegerField()                                             # 学时
    yxh = models.CharField(max_length=8)                                   # 院系号
    class Meta:
        unique_together=("xq", "kh", "km")

class O(models.Model):
    kh = models.CharField(max_length=32)                 # 课号
    gh = models.CharField(max_length=32, unique=True)    # 工号
    sksj = models.CharField(max_length=32)               # 上课时间
    class Meta:
        unique_together = ("kh", "gh", "sksj")

class E(models.Model):
    xn = models.CharField(max_length=32)                 # 学年
    xq = models.CharField(max_length=32)                 # 学期
    xh = models.CharField(max_length=32)                      # 学号
    kh = models.CharField(max_length=32)                 # 课号
    gh = models.CharField(max_length=32, unique=True)    # 工号
    pscj = models.FloatField()                                             # 平时成绩
    kscj = models.FloatField()                                             # 考试成绩
    zpcj = models.FloatField()                                             # 总评成绩
    class Meta:
        unique_together = ("xn", "xq", "xh", "kh", "gh")



