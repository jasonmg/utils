# -*- coding:utf8 -*-

# 把所有文件编译成pyc

# 把所有pyc文件复制到dist目录下
# 在原目录下清除多余的pyc文件
import os
import sys
from compileall import compile_dir


def check_environment(outparams, default=None):
    '''
    检查环境变量
    parameter
        outparams
    return
        boolean
    '''
    home = os.environ.get('APP_HOME')

    if default:
        outparams["home"] = default
        return True
    elif default:
        outparams["home"] = home
    else:
        print("APP_HOME undefine!")
        return False


def asm_compiler(dirList):
    '''
    编译
    parameter
        homtRoot 工程根目录
    return
        boolean
    '''
    for folder in dirList:
        result = compile_dir(dir=folder, maxlevels=20, force=1, legacy=True)
        if result == 0:
            print("[build error]:%s" % folder)
            return False
        else:
            print("[build success]:%s" % folder)
    return True


def asm_clear_all_compiler_files(dirList):
    '''
    清除所有编译文件
    parameter
        dirList 原目录列表
    return
        boolean
    '''
    for path in dirList:
        fList = []
        asm_ls_dirs(path, ".pyc", fList)
        for f in fList:
            if "target" in f:
                continue
            os.remove(f)
        del fList[:]


def asm_copy_compiler_files(home, distRoot):
    '''
    复制编译文件
    parameter
        home 原目录
        distRoot 目标根目录
    return
        boolean
    '''
    import shutil
    from shutil import ignore_patterns
    import os
    ret = os.path.exists(home)
    if ret:
        if os.path.exists(distRoot):
            shutil.rmtree(distRoot)
    # 设置忽略文件和目录
    shutil.copytree(
        home, distRoot,
        ignore=ignore_patterns(
            ".svn", ".git", ".idea", "*.py", "*.cer", "documents", "build", "dist", "tests", "tmp"
        )
    )


def asm_ls_dirs(path, fileext, fList):
    for p in os.listdir(path):
        f = path + os.path.sep + p
        if os.path.isdir(f):
            asm_ls_dirs(f, fileext, fList)
        else:
            if f.endswith(fileext):
                fList.append(f)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outparams = {}
    ret = check_environment(outparams, BASE_DIR)
    if ret:
        home = outparams['home']
        dirList = []
        dirList.append("".join([home, ""]))
        if asm_compiler(dirList):
            target = "".join([home, "/build/target"])
            print("copy compiler files...")
            asm_copy_compiler_files(home, target)
            print("clear original compiler files...")
            asm_clear_all_compiler_files(dirList)
            sys.exit(1)
    sys.exit(0)
