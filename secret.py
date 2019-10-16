# coding:utf-8
import sys, os, time, shutil
from distutils.core import setup
from Cython.Build import cythonize
 
"""
使用方法:
file_name:setup.py
# python setup.py dir(.py项目目录)
会将错误的.py文件和__init__.py复制到build对应目录下，同时删除编译过程生成的.c和.o文件
"""
 
except_file = sys.argv[0]
parent_path = sys.argv[1]
start_time = time.time()
build_dir = "build"
build_tmp_dir = build_dir + "/temp"
#项目前缀，比如python文件中出现 import a.b.c 则project_pre为a
project_pre = ""
py_list = []
error_file = []
 
 
def py2so_operations(parent_path=parent_path, excepts=(except_file), get_py=False, del_C=False, copy_init_py=False):
    base_path = os.path.abspath('.')
    full_path = os.path.join(base_path, parent_path)
    for fod_name in os.listdir(full_path):
        fod_path = os.path.join(full_path, fod_name)
        if os.path.isdir(fod_path) and fod_name != build_dir and not fod_name.startswith('.'):
            py2so_operations(parent_path=os.path.join(parent_path, fod_name), get_py=get_py,
                             del_C=del_C)
        elif os.path.isfile(fod_path) and fod_name not in excepts:
            ext_name = os.path.splitext(fod_name)[1]
            if get_py is True and ext_name in ('.py', '.pyx') and not fod_name.startswith("__"):
                py_list.append(os.path.join(parent_path, fod_name))
            if del_C is True and ext_name == ".c":
                os.remove(fod_path)
            if copy_init_py is True and fod_name.startswith("__"):
                dst_dir = os.path.join(base_path, build_dir, base_path[base_path.find(project_pre):], parent_path)
                shutil.copyfile(fod_path, os.path.join(dst_dir, fod_name))
 
def copy_error_py(file_list):
    for file in file_list:
        base_path = os.path.abspath('.')
        dst_dir = os.path.join(base_path,build_dir,base_path[base_path.find(project_pre):],file[:file.rfind("/")])
        if not os.path.isdir(dst_dir): os.makedirs(dst_dir)
        filename = file[file.rfind("/"):].replace("/","")
        file_path = os.path.join(base_path,file)
        shutil.copyfile(file_path,os.path.join(dst_dir,filename))
 
def set_up(file_list):
    for file in file_list:
        try:
            setup(ext_modules=cythonize(file), script_args=["build_ext", "-b", build_dir, "-t", build_tmp_dir])
        except Exception as e:
            print "Error File:"+e.message
            file_list.remove(file)
            error_file.append(file)
            set_up(file_list)
    if os.path.exists(build_tmp_dir): shutil.rmtree(build_tmp_dir)
 
if __name__ == '__main__':
    py2so_operations(get_py=True)
    set_up(py_list)
    copy_error_py(error_file)
    py2so_operations(del_C=True, copy_init_py=True)
