1、运行主程序
	主循环原理：循环遍历所有用户，检查其登录状态，根据其状态，开启或者关闭其线程。	
	
2、配置信息
	（1）服务器配置
	（2）管理员
	（3）用户类型和权限等级
	（4）指令
	（5）日志存储路径
	
3、验证管理员信息，若无管理员，则先设置管理员，管理员可以在微信端发送控制指令。
	
4、运行所有用户微信
	验证是否是自动登录
	允许自由登录或退出
	实时监测用户组变动，关闭或者开启用户线程
	
5、在数据库中记录、更新数据


定义用户类型：
	0、超级管理员（superAdmin）
	1、管理员（admin）
	2、超级用户（superUser）
	3、普通用户（user）
	4、试用用户（freeTrailUser）

定义管理权限：True、False
	试用用户权限：（freeTrailUserLimits）
	普通用户权限：（userLimits）
	超级用户权限：（superUserLimits）
	管理员权限：（adminLimits）
	超级管理员权限：（superAdminLimits）
	
	开启、关闭程序
	开启、关闭用户线程
	添加、删除用户
	指定用户类型

用户类（核心）：User
	属性：
		用户类型：0, 1, 2, 3, 4（userType）
		自动登录：True、False（autoLogin）
		在线状态：True、False（alive）
		
	方法：