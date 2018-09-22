程序名：选课系统
为了更好地使用程序，请阅读一下文档
一、程序包含四个文件
		1、readme.txt
		2、程序流程图
		3、选课系统UML图
		4、程序代码文件夹course_selection
二、程序功能
		1、学员在线注册，选课，查看班级，上传作业、缴学费的功能
		2、老师查看班级，选择上课班级，修改学员成绩
		3、管理员可以添加课程、添加班级，添加讲师，添加学员，为班级制定老师，查看学校、班级、课程、讲师等信息
三、使用方法
		运行bin\start.py文件，即可运行程序
		账号数据请查看db\userinfo
四、程序目录结构
D:.
│  tree.txt
│  __init__.py
│  作业要求.py
│  
└─course_selection 	#程序根目录
    │  
    │  __init__.py
    │  
    ├─bin	程序启动目录
    │      start.py	#程序启动文件
    │      __init__.py
    │      
    ├─conf	程序配置目录
    │  │  config.py	程序配置文件
    │  │  __init__.py
    │  │  
    │  └─__pycache__
    │          config.cpython-36.pyc
    │          __init__.cpython-36.pyc
    │          
    ├─core	程序核心功能目录
    │  │  auth.py	账号认证模块
    │  │  logger.py	记录日志模块
    │  │  main.py	逻辑主程序
    │  │  Manager.py	管理员类模块
    │  │  my_pickle.py	序列化工具模块
    │  │  school.py	学校类模块
    │  │  Student.py	学生类模块
    │  │  Teacher.py	讲师类模块
    │  │  Utility_class.py	共用父类模块
    │  │  __init__.py
    │  │  
    │  └─__pycache__
    │          auth.cpython-36.pyc
    │          logger.cpython-36.pyc
    │          main.cpython-36.pyc
    │          Manager.cpython-36.pyc
    │          my_pickle.cpython-36.pyc
    │          school.cpython-36.pyc
    │          Student.cpython-36.pyc
    │          Teacher.cpython-36.pyc
    │          Utility_class.cpython-36.pyc
    │          __init__.cpython-36.pyc
    │          
    ├─db	程序数据模块
    │      class_obj		班级对象数据
    │      class_students(Go_s1)	班级Go_s1所有学生对象数据，
    │      class_students(Go_s2)	班级Go_s2所有学生对象数据
    │      class_students(Python_s1)		班级Python_s1所有学生对象数据
    │      course_obj		课程对象数据
    │      Manager_obj		管理员对象数据
    │      school_obj		学校对象数据
    │      Student_obj 	学生对象数据
    │      Teacher_obj	老师对象数据
    │      userinfo	登录信息数据
    │      __init__.py
    │      
    └─logs	日志目录
            access.log		账号登陆，退出日志
            manager.log	管理员操作日志
            students.log	学生操作日志
            teachers.log	老师操作日志
            __init__.py
            
