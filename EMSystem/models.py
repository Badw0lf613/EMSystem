from django.db import models

# Create your models here.
class S(models.Model):                                                     # 学生表
    xh = models.CharField(max_length=32, unique=True, primary_key=True)    # 学号（主键）
    xm = models.CharField(max_length=32)                                   # 姓名
    xb = models.CharField(max_length=4)                                    # 性别
    csrq = models.DateField()                                              # 出生日期
    jg = models.CharField(max_length=32)                                   # 籍贯
    sjhm = models.CharField(max_length=32, unique=True)                    # 手机号码
    yxh = models.ForeignKey('D', to_field='yxh', on_delete=models.CASCADE)      # 院系号(外键)


class D(models.Model):                                                     # 院系表
    yxh = models.CharField(max_length=8, primary_key=True)                 # 院系号
    yxm = models.CharField(max_length=32)                                  # 院系名称
    lxdh = models.CharField(max_length=32, unique=True)                    # 联系电话
    dz = models.CharField(max_length=64)                                   # 地址


class T(models.Model):
    gh = models.CharField(max_length=32, unique=True, primary_key=True)    # 工号(主键)
    xm = models.CharField(max_length=32)                                   # 姓名
    xb = models.CharField(max_length=4)                                    # 性别
    csrq = models.DateField()                                              # 出生日期
    xl = models.CharField(max_length=32)                                   # 学历
    gz = models.FloatField()                                               # 工资
    yxh = models.ForeignKey('D', to_field='yxh',on_delete=models.CASCADE)      # 院系号(外键)
    pf = models.FloatField()                                               # 评分


class C(models.Model):
    xq = models.CharField(max_length=32)                 # 学期
    kh = models.CharField(max_length=32)                 # 课号
    km = models.CharField(max_length=32)                 # 课名
    xf = models.IntegerField()                                             # 学分
    xs = models.IntegerField()                                             # 学时
    yxh = models.ForeignKey('D', to_field='yxh',on_delete=models.CASCADE)      # 院系号(外键)
    class Meta:
        unique_together=("xq", "kh")              # 联合主键(学期，课号)


class O(models.Model):
    cid = models.ForeignKey('C', to_field='id',on_delete=models.CASCADE)      # 课程序号(外键)
    kh = models.CharField(max_length=32)                 # 课号
    gh = models.ForeignKey('T', to_field='gh',on_delete=models.CASCADE)         # 工号(外键)
    sksj = models.CharField(max_length=32)               # 上课时间
    class Meta:
        unique_together = ("kh", "gh", "sksj")

class E(models.Model):
    cid = models.ForeignKey('C', to_field='id',on_delete=models.CASCADE)      # 课程序号(外键)
    xn = models.CharField(max_length=32)                 # 学年
    xq = models.CharField(max_length=32)                 # 学期
    xh = models.ForeignKey('S', to_field='xh',on_delete=models.CASCADE)         # 学号(外键)
    kh = models.CharField(max_length=32)                 # 课号
    gh = models.ForeignKey('T', to_field='gh',on_delete=models.CASCADE)         # 工号(外键)
    pscj = models.FloatField(null=True,blank=True)       # 平时成绩
    kscj = models.FloatField(null=True,blank=True)       # 考试成绩
    zpcj = models.FloatField(null=True,blank=True)       # 总评成绩
    class Meta:
        unique_together = ("xn", "xq", "xh", "kh", "gh")

class TEMP(models.Model):
    xq = models.CharField(max_length=32)
    km = models.CharField(max_length=32)
    yxh = models.ForeignKey('D', to_field='yxh',on_delete=models.CASCADE)
    xf = models.IntegerField()
    gh = models.CharField(max_length=32)
    stats = models.CharField(max_length=32)