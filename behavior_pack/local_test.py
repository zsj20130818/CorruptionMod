# -*- coding: utf-8 -*-
"""
本地测试脚本：用来验证模块导入路径是否正确
在 VS Code 中直接运行此文件 (F5 或点运行按钮)
"""

# 修复 Python 2.7 控制台编码问题
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

# 如果控制台是 Windows cmd，可能需要额外处理
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('gbk')(sys.stdout, 'ignore')
    sys.stderr = codecs.getwriter('gbk')(sys.stderr, 'ignore')


# 1. 将当前目录 (behavior_pack/) 加入 Python 的搜索路径
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
print("已将根目录加入路径: {}".format(base_dir))

# 2. 模拟 modMain.py 把子目录也加入搜索路径
sub_dirs = ["event", "network", "progression", "dialogue", "command", "registry", "client"]
for sub in sub_dirs:
    sub_path = os.path.join(base_dir, sub)
    if os.path.exists(sub_path):
        sys.path.insert(0, sub_path)
        print("已将子目录加入路径: {}".format(sub_path))

# 2.5 在本地创建一个假的 mod 模块，用来通过测试
class FakeModule:
    pass
sys.modules['mod'] = FakeModule()
sys.modules['mod.server'] = FakeModule()
sys.modules['mod.server.extraServerApi'] = FakeModule()
print("已创建模拟的 mod 环境，用于本地测试")

# 3. 尝试执行那个报错的导入语句！
print("\n开始尝试导入 verity_network ...")
try:
    # 这里使用我们讨论过的正确写法
    from network import verity_network
    print("✅ 成功从 network 导入了 verity_network！")
    print("模块位置: {}".format(verity_network.__file__))
except ImportError as e:
    print("❌ 导入失败: {}".format(e))
    print("请检查 network 文件夹下是否存在 verity_network.py 文件")

# 4. 你可以在这里继续添加其他测试，比如导入 event.scare_director
try:
    from event import scare_director
    print("✅ 成功导入了 event.scare_director")
except ImportError as e:
    print("❌ 导入 scare_director 失败: {}".format(e))