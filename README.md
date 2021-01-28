# EMSystem（教务管理系统）
## 上海大学数据库课程项目
## 持续更新中...
### 登录页面
&emsp;&emsp;背景图链接：https://oauth.shu.edu.cn/static/images/login-bg.jpg
### 学生端选课限制（时间段or学分上限）触发器
### ~~学生端课程查询student_QueryCourse~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/kccx.png)
&emsp;&emsp;学生查询课程时可以选择学期，因此可以查到非当前学期/当前学期未开设的课程。<br>
&emsp;&emsp;<big>__分情况考虑__</big>针对C表存在但O表中不存在的课程即当前学期未开设的课程，返回结果为C表所有字段。<br>&emsp;&emsp;对于C表和O表均存在的课程即当前学期开设的课程，返回结果仿照教务处选课系统，增加工号，教师名称，上课时间三个字段。<br>
&emsp;&emsp;故首先查询C表，使用filter方法将表单的字段与C表中已有的字段（xq,kh,km）进行匹配。此时gh,jsmc,sksj三个字段仍为空，需要利用到O表和T表进行多表查询。<big><big>注意：需要确保O表与C表的主键id对应一致，即C表包含所有id，O表只有其中一部分。</big></big>
### ~~学生端选课student_AddCourse~~~~选课成功/失败信息弹窗~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/xk.png)
&emsp;&emsp;学生选课针对当前学期即2020-2021学年春季学期，使用课程号、工号、学期和学号对E表进行查询。首先利用这四个字段在E表中找出id，再分别到C、O、T表中通过id找出课程名称、上课时间和教师名称。<br>
&emsp;&emsp;是否要考虑一个老师一学期同一门课开两次的情况（如信号处理）。<br>
&emsp;&emsp;解决重复选课的bug。
### ~~学生端退课student_DeleteCourse选课~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/tk.png)
&emsp;&emsp;复选框效果完成，jQuery方法删除对应的课程，对于未选择课程和选课成功均设置弹窗。
### ~~学生端成绩查询student_QueryGrades~~
![image](https://github.com/Badw0lf613/EMSystem/blob/master/static/images/cjcx.png)
### 学生端课表student_CourseTable
### 院系号变院系
### C变O
&emsp;&emsp;方案：老师发申请，放入一张新表（一个字段表示课程状态，课程变开课表|认领页面|申请页面），管理员去读，类似于借阅表，管理员给课号，输入课名时（触发器），不重复就可以
### C增加
&emsp;&emsp;方案：老师发申请，放入一张新表（一个字段表示课程状态，为开设新课程表|认领页面|申请页面），管理员给课号