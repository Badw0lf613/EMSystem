# EMSystem（教务管理系统）
## 上海大学数据库课程项目
## 持续更新中...
### 登录页面
&emsp;&emsp;背景图链接：https://oauth.shu.edu.cn/static/images/login-bg.jpg
### ~~学生端课程查询student_QueryCourse~~
&emsp;&emsp;学生查询课程时可以选择学期，因此可以查到非当前学期/当前学期未开设的课程。<br>
&emsp;&emsp;<big>__分情况考虑__</big>针对C表存在但O表中不存在的课程即当前学期未开设的课程，返回结果为C表所有字段。<br>&emsp;&emsp;对于C表和O表均存在的课程即当前学期开设的课程，返回结果仿照教务处选课系统，增加工号，教师名称，上课时间三个字段。<br>
&emsp;&emsp;故首先查询C表，使用filter方法将表单的字段与C表中已有的字段（xq,kh,km）进行匹配。此时gh,jsmc,sksj三个字段仍为空，需要利用到O表和T表进行多表查询。<big><big>注意：需要确保O表与C表的主键id对应一致，即C表包含所有id，O表只有其中一部分。</big></big>
### 学生端选课student_AddCourse
&emsp;&emsp;学生选课针对当前学期即2020-2021学年春季学期，
### 学生端退课student_DeleteCourse
### 学生端成绩查询student_QueryGrades
### 学生端课表student_CourseTable