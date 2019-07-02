
//关于对模型的修改

1.在app目录下models.py中对Aritcle类进行修改
	在其属性中添加一条如下
	...
	article_sim = models.CharField(max_length=300) 
	...
	
	(注:
		该数据为字符串类型，为3个id用逗号连接，使用时需先split得到3个id，传入网页模板，设置url即可，调用的view可直接使用前面已经写好的
		)
	
2.在主文件夹中(与manage.py同目录)，输入如下命令
	python manage.py makemigrations app

	此时会受到提示，是否对新添加的model属性赋 默认值
	选择 是 ，默认值随意输入即可
	
	然后输入命令
	python manage.py migrate
	
//关于数据导入到数据库
1.将 similarity4.pickle 与inputsim.py 文件 放入 django project 的 主文件夹中 (与manage.py和数据库文件在同一目录下)
2.运行inputsim.py即可

