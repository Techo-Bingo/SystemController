# Remote-Controller
服务器操作维护GUI工具
***
__本工具主要用于主备服务器状态巡检以及日志快速获取__
***

__特点:__
* 功能支持定制化，可扩展性强

__更新日志：__
* v1.0:
    * 此版本主要是个人兴趣开发，以及方便平时工作中的问题快速定位。  
        1.0版本中图标、图片均是通过base64加密成密码串写死在代码中，通过启动工具时动态生成，  
        此方式虽然可以让工具打包成单独的一个exe文件，但是也使得工具启动时间变长且不利于持续演进，  
        后续版本考虑只打包代码到exe，依赖文件在发布时通过人工操作跟exe一起压缩到一个zip包里。  

* v2.0:
    * 软件发布形态方面：
        v2.0不再是一个单独的exe文件，而是一个zip压缩包，解压后可以看到一个exe和一些依赖文件等；  
        作者将依赖的文件从代码中剥离，不动态生成，在软件发布时静态打包到压缩包里，不打包到单独的exe中；  
        并将依赖文件对应路径等关系写入配置文件，极大的提高了可扩展性；

    * 代码架构方面，遵循MVVM架构：  
        - Model板块（数据部分）完全与View板块（视图部分）解耦分离；  
        - View板块可以直接通知（调用）ViewModel板块来处理用户请求；  
        - Model板块负责定义数据模型和数据的存取实现；  
        - ViewModel板块不能直接调用View，需要以事件驱动View的回调函数；  
        - ViewModel板块依赖Model板块，ViewModel作为View和Model的中间件，负责映射（绑定）事件与数据的关系。  

* v2.1:
    * 版本修改：
        - 新增菜单栏和快捷工具栏；
        - 导航栏目录由LabelButton改成TreeView,目录更直观且可自由折叠和滚动，不再受个数限制；
        - 操作界面实现‘界面类型’，动态修改配置文件即可自由增删固定类型的界面；
        - 软件主界面宽高加大；
        - 其他优化；
        
* v2.2:
    * 版本修改：
        - 新增主页显示服务器简要信息；
        - 新增时区配置管理自定义界面；
        - 新增导入可视化库matplotlib到.exe编译包;
        - 优化界面实现和json配置文件，模板界面支持多个同类型控件，增强扩展性；
        - 其他代码优化；
    
* v2.3:
    * 版本修改：
        - 初步模板化界面控件，实现单一化控件界面；
        - 新增个性化窗体MyFrame，并扩展至整体界面风格；
        - 新增服务器断链自动重连机制；
        - 其他代码优化；    
   
* v2.4:
    * 版本修改：
        - 实现复杂控件类型模板化：'Label', 'Checkbox', 'Combobox', 'Entry', 'Text', 'Button'；
        - 实现单个界面可通过修改配置文件即可布局不同的控件；
        - 新增弹窗显示类型，显示执行结果；
        - 服务器脚本调用方式修改；
       
* v2.5:
    * 版本修改：
        - BUGFIX：解决单个线程依次执行多个服务器的脚本的问题；
        - BUGFIX：解决进度信息只在脚本执行结束后显示依次的问题；
        - 新增默认“首页”：简单向导；
        - 新增Notebook模板控件，用于‘只读’显示界面enter结果；
        - 新增可自定义快捷工具栏功能；
        - 修改界面实现，使用界面“属性”和控件“属性”概念替换之前的多个key；
        - 修改界面style，统一使用ttk原始主题风格；
        - 默认‘root执行’按钮不勾选，默认勾选‘后台执行’按钮；
        - 其他修改；

* v3.0:
      * 实现数据可视化模板；
      * 新增自定义进程资源数据可视化；

* v3.2:
      * 新增MultiCombobox和PlotNotebook模板控件；
      * 实现CPU和内存使用情况可视化；

* v3.3:
      * BUGFIX: 解决上传大文件失败问题；
      * 新增上传文件的详细进度界面；
