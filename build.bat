python D:\04.MyCode\PyInstaller-3.6\pyinstaller.py -F -w -i image\item.ico OAMTool.py -p my_base.py -p my_bond.py -p my_common.py -p my_global.py -p my_handler.py -p my_logger.py -p my_model.py -p my_module.py -p my_page.py -p my_setting.py -p my_ssh.py -p my_util.py -p my_view.py -p my_viewmodel.py -p my_viewutil.py -p my_timezone.py --hidden-import my_base --hidden-import my_bond --hidden-import my_common --hidden-import my_global --hidden-import my_handler --hidden-import my_logger --hidden-import my_model --hidden-import my_module --hidden-import my_page --hidden-import my_setting --hidden-import my_ssh --hidden-import my_util --hidden-import my_view --hidden-import my_viewmodel --hidden-import my_viewutil --hidden-import my_timezone --hidden-import pandas --hidden-import matplotlib 

:: pack to exe
:: -F -w
:: pack to dir
:: -D

pause     


