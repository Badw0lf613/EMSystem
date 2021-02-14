# EMSystem（教务管理系统）
## 上海大学数据库课程项目
## 持续更新中...
### ~~登录页面~~
背景图链接： <br>
https://oauth.shu.edu.cn/static/images/headerbg.jpg <br>
https://oauth.shu.edu.cn/static/images/footerbg.jpg <br>
https://oauth.shu.edu.cn/static/images/login-bg.jpg <br>
https://oauth.shu.edu.cn/static/images/logo-white.png
### 学生端选课限制（~~时间段~~or学分上限）触发器
### ~~学生端课程查询student_QueryCourse~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/kccx.png)
学生查询课程时可以选择学期，因此可以查到非当前学期/当前学期未开设的课程。<br>
<big>__分情况考虑__</big>针对C表存在但O表中不存在的课程即当前学期未开设的课程，返回结果为C表所有字段。<br>&emsp;&emsp;对于C表和O表均存在的课程即当前学期开设的课程，返回结果仿照教务处选课系统，增加工号，教师名称，上课时间三个字段。<br>
故首先查询C表，使用filter方法将表单的字段与C表中已有的字段（xq,kh,km）进行匹配。此时gh,jsmc,sksj三个字段仍为空，需要利用到O表和T表进行多表查询。<big><big>注意：需要确保O表与C表的主键id对应一致，即C表包含所有id，O表只有其中一部分。</big></big>
### ~~学生端选课student_AddCourse~~~~选课成功/失败信息弹窗~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/xk.png)
学生选课针对当前学期即2020-2021学年春季学期，使用课程号、工号、学期和学号对E表进行查询。首先利用这四个字段在E表中找出id，再分别到C、O、T表中通过id找出课程名称、上课时间和教师名称。<br>
是否要考虑一个老师一学期同一门课开两次的情况（如信号处理）。<br>
解决重复选课的bug。<br>
~~**选课时间段冲突。**~~
### ~~学生端退课student_DeleteCourse选课~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/tk.png)
复选框效果完成，jQuery方法删除对应的课程，对于未选择课程和选课成功均设置弹窗。
### ~~学生端成绩查询student_QueryGrades~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/cjcx.png)
触发器：更新GPA
~~### 学生端课表student_CourseTable~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/kb.png)
### 院系号变院系
### C变O
方案：老师发申请，放入一张新表（一个字段表示课程状态，课程变开课表|认领页面|申请页面），管理员去读，类似于借阅表，管理员给课号，输入课名时（触发器），不重复就可以
### C增加
方案：老师发申请，放入一张新表（一个字段表示课程状态，为开设新课程表|认领页面|申请页面），管理员给课号
### 触发器
选课：先建记录，再判断能不能插入<br>
hyd教学评估：新来学生的打分与原分数比，高/低，不需要新建一个表 before update update，先吉减再加<br>
ysy更新GPA：<br>
yce管理员：添加角色再加入auth_user表，例如添加学生的同时加入auth_user，并分配初始密码。<br>
开课申请表&认领课程表（0、1区分）：开课人工号，课名，学期，学分
开课表：加一列，对该老师的评价
### ~~管理员切换学期时/课程管理变换学期或删除课程修改课程时需要将开课表内容更新！！！~~
### 课程temp表多了个春季学期，
### 课程查询加一个选课人数，django的count
### ~~学生院系号变成院系~~
### ~~教师查询不能是学号要是工号~~
### ~~E表存了所有学期的课程，已选该课程的判定？？没问题，首先查开课表有无该课程，只需要对开课表更新~~