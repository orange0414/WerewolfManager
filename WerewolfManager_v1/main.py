import random
import json
import copy


class Role:
    def __init__(self, name, team, description):
        self.name = name
        self.team = team
        self.description = description
    
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
    
    def toString(self):
        return f"【{self.name}】【{self.team}】: \n {self.description}"

with open("data/roles.json", "r", encoding = "utf-8") as f:
    data = json.load(f)

allRoles = [Role(**item) for item in data]
actualRoles = []
currentBoard = ""

'''
------------------------------ Main ----------------------------------------
'''
def main():
    
    valid_actions = [0, 1, 2, 3, 4]
    
    while(True):
        action = None
        
        while(not action in valid_actions):
            main_menu()
            print("="*178)
            action = input("请输入你的选项: ")
            print("="*178)
            try:
                action = int(action)
            except ValueError:
                print("\033[31m" + "="*178 + "\033[0m")
                print("\033[31m" + "【注意！请输入以下选项中的一项: " + f"{valid_actions}" + "】\033[0m")
                print("\033[31m" + "="*178 + "\033[0m")
                continue
            if not action in valid_actions:
                print("\033[31m" + "="*178 + "\033[0m")
                print("\033[31m" + "【注意！请输入有效选项: " + f"{valid_actions}" + "】\033[0m") 
                print("\033[31m" + "="*178 + "\033[0m")
                continue
            
            match action:
                case 0:
                    msg = "感谢您的支持！欢迎下次使用！"
                    hotpink = (255, 105, 180)
                    aqua    = (  0, 255, 255)
                    print_gradient_text(msg, hotpink, aqua)
                    return
                case 1:
                    showRoles(actualRoles)
                    break
                case 2:
                    showRoles(allRoles)
                    break
                case 3:
                    chooseBoard()
                    break
                case 4:
                    startGame()
                    break

'''
---------------------------- Show Roles ------------------------------------
'''
def showRoles(roles: list[Role]):
    
    if roles:
        print("\033[38;2;255;105;180m" + "="*178)
        title = f"【<{currentBoard}>角色介绍】" if roles == actualRoles else "【<所有版型>角色介绍】"
        print(title + "\033[0m")
    
        # 定义阵营排序权重
        order = {"神职": 0, "村民": 1, "狼人": 2}
        
        # 去重并按阵营顺序排序
        uniqRoles = set(roles)
        sorted_roles = sorted(uniqRoles, key=lambda r: order.get(r.team, 99))
        
        for role in sorted_roles:
            print()
            if role.team == "神职":
                color = "\033[38;5;220m"
            elif role.team == "狼人":
                color = "\033[38;5;196m"
            elif role.name == "混子" or role.team == "第三方":
                color = "\033[38;5;141m"
            elif role.team == "村民":
                color = "\033[38;5;94m"
            else:
                color = ""
            
            if color:
                print(f"{color}【{role.name}】({role.team})\n\033[0m{role.description}")
            else:
                print(role.toString())
            
            print("="*178)
                
        print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                
    elif not roles:
        print("\033[31m" + "="*178 + "\033[0m")
        print("\033[31m" + "\t【未选择版型】" + "\033[0m")
        print("\033[31m" + "="*178 + "\033[0m")

'''
--------------------------- Choose Board -----------------------------------
'''
def chooseBoard():
    
    global currentBoard
    valid_actions = [0, 1]
    
    while(True):
        action = None
        
        while action not in [1]:
            board_menu()
            print("="*178)
            action = input("请输入你的选项: ")
            print("="*178)
            try:
                action = int(action)
            except ValueError:
                print("\033[31m" + "="*178 + "\033[0m")
                print("\033[31m" + "【注意！ 请输入以下选项中的一项: " + f"{valid_actions}" + "】\033[0m")
                print("\033[31m" + "="*178 + "\033[0m")
                continue
            if not action in valid_actions:
                print("\033[31m" + "="*178 + "\033[0m")
                print("\033[31m" + "【注意！ 请输入有效选项: " + f"{valid_actions}" + "】\033[0m")
                print("\033[31m" + "="*178 + "\033[0m")
                continue
            
            match action:
                case 0:
                    return
                case 1:
                    currentBoard = "预女猎白混"
                    pickRoles({"预言家":1, "女巫":1, "猎人":1, "白痴":1, "混子":1, "村民":3, "狼人":4})
                    print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                    print("\033[32m" + "\t您已选择【预女猎白混】配置" + "\033[0m")
                    print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass

def pickRoles(rolesToPick:dict[str,int]):
    global actualRoles
    actualRoles = []
    for name, cnt in rolesToPick.items():
        # 在 allRoles 里找到这个 name 对应的 Role 模板
        template = next((r for r in allRoles if r.name == name), None)
        if not template:
            print("\033[31m" + "="*178 + "\033[0m")
            print(f"\t【未能找到角色】: {name}")
            print("\033[31m" + "="*178 + "\033[0m")
            return
        # 拷贝
        for _ in range(cnt):
            actualRoles.append(copy.deepcopy(template))

'''
----------------------------- Start Game -----------------------------------
'''
def startGame():
    if not actualRoles or currentBoard == "":
        print("\033[31m" + "="*178 + "\033[0m")
        print("\033[31m" + "【注意！ 未选择板子或选择出错" + "】\033[0m")
        print("\033[31m" + "="*178 + "\033[0m")
        return
    
    
'''
------------------------------- Menu --------------------------------------- 
'''
def main_menu():
    print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
    print("\033[32m" + '''
    【主菜单】
    请选择您要进行的操作: 
    0. 退出
    1. 查看当前角色信息
    2. 查看所有角色信息
    3. 选择板子
    4. 开始游戏
    ''' +"\033[0m")
    print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")

def board_menu():
    print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
    print("\033[32m" + '''
    【板子选择】
    0. 返回
    1. 预女猎白混
    ''' +"\033[0m")
    print("\033[38;2;255;105;180m"+ "="*178 + "\033[0m")

'''
----------------------------- Others ----------------------------------------------------
'''
def print_gradient_text(text: str,
                        start_color: tuple[int,int,int],
                        end_color: tuple[int,int,int]) -> None:
    """
    按照 start_color -> end_color 的渐变，给 text 中的每个字符渲染颜色并打印。
    
    :param text: 要打印的字符串
    :param start_color: 起始 RGB 三元组 (e.g. (255,105,180))
    :param end_color: 结束 RGB 三元组 (e.g. (0,255,255))
    """
    length = len(text)
    for i, ch in enumerate(text):
        ratio = i / max(length - 1, 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        print(f"\033[38;2;{r};{g};{b}m{ch}", end="")
    print("\033[0m")


if __name__ == "__main__":
    main()