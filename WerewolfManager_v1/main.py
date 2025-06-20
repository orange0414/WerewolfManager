import random
import json
import copy


class Role:
    def __init__(self, name:str, team:str, description:str):
        self.name = name
        self.team = team
        self.description = description
    
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
    
    def toString(self):
        return f"【{self.name}】【{self.team}】: \n {self.description}"

class Player:
    def __init__(self, id:int, role:Role):
        self.id = id
        self.role = role
        self.alive = True
        self.death_type:str = ""
    
    def isAlive(self):
        return self.alive
    
    def deathType(self):
        return self.death_type

with open("data/roles.json", "r", encoding = "utf-8") as f:
    data = json.load(f)

allRoles = [Role(**item) for item in data]
currentRoles = []
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
                    msg = "\n【感谢您的支持！欢迎下次使用！】\n"
                    startColor = (54, 209, 220)
                    endColor    = (91, 134, 229)
                    print_gradient_text(msg, startColor, endColor)
                    return
                case 1:
                    showRoles(currentRoles)
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
        title = f"【<{currentBoard}>角色介绍】" if roles == currentRoles else "【<所有版型>角色介绍】"
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
            print()
            print("="*178)
                
        print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                
    elif not roles:
        print("\033[31m" + "="*178 + "\033[0m")
        print("\033[31m" + "【未选择版型】" + "\033[0m")
        print("\033[31m" + "="*178 + "\033[0m")

'''
--------------------------- Choose Board -----------------------------------
'''
def chooseBoard():
    
    global currentBoard
    valid_actions = [0, 1, 2, 3, 4, 5, 6, 7]
    
    action = None
    
    while action not in valid_actions:
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
                break
            case 1:
                currentBoard = "预女猎白混"
                pickRoles({"预言家":1, "女巫":1, "猎人":1, "白痴":1, "混子":1, "村民":3, "狼人":4})
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                print("\033[32m" + "【您已选择<预女猎白混>配置】" + "\033[0m")
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                break
            case 2:
                currentBoard = "假面舞会"
                pickRoles({"预言家":1, "女巫":1, "舞者":1, "白痴":1, "村民":4, "狼人":3, "假面":1})
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                print("\033[32m" + "【您已选择<假面舞会>配置】" + "\033[0m")
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                break
            case 3:
                currentBoard = "孤注一掷"
                pickRoles({"预言家":1, "女巫":1, "猎人":1, "摄梦人":1, "村民":4, "狼人":3, "典狱长":1})
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                print("\033[32m" + "【您已选择<孤注一掷>配置】" + "\033[0m")
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                break
            case 4:
                currentBoard = "机械狼通灵师"
                pickRoles({"通灵师":1, "女巫":1, "守卫":1, "猎人":1, "村民":4, "狼人":3, "机械狼":1})
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                print("\033[32m" + "【您已选择<机械狼通灵师>配置】" + "\033[0m")
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                break
            case 5:
                currentBoard = "盗宝通灵"
                pickRoles({"通灵师":1, "毒师":1, "猎人":1, "摄梦人":1, "蒙面人":1,"村民":5, "狼人":4, "盗宝大师":1})
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                print("\033[32m" + "【您已选择<盗宝通灵>配置】" + "\033[0m")
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                break
            case 6:
                currentBoard = "鬼魂新娘"
                pickRoles({"预言家":1, "女巫":1, "猎人":1, "守卫":1, "村民":4, "狼人":3, "鬼魂新娘":1})
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                print("\033[32m" + "【您已选择<鬼魂新娘>配置】" + "\033[0m")
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                break
            case 7:
                currentBoard = "骑士狼美"
                pickRoles({"预言家":1, "女巫":1, "守卫":1, "骑士":1, "村民":4, "狼人":3, "狼美人":1})
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                print("\033[32m" + "【您已选择<骑士狼美>配置】" + "\033[0m")
                print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
                break
        return

def pickRoles(rolesToPick:dict[str,int]):
    global currentRoles
    currentRoles = []
    for name, cnt in rolesToPick.items():
        # 在 allRoles 里找到这个 name 对应的 Role 模板
        template = next((r for r in allRoles if r.name == name), None)
        if not template:
            print("\033[31m" + "="*178)
            print(f"【未能在现有角色中找到角色】: {name}")
            print("="*178 + "\033[0m")
        # 拷贝
        for _ in range(cnt):
            currentRoles.append(copy.deepcopy(template))

'''
----------------------------- Start Game -----------------------------------
'''

def startGame():
    if not currentRoles or currentBoard == "":
        print("\033[31m" + "="*178 + "\033[0m")
        print("\033[31m" + "【注意！ 未选择板子或选择出错" + "】\033[0m")
        print("\033[31m" + "="*178 + "\033[0m")
        return
    
    match currentBoard:
        case "预女猎白混":
            print("\033[32m" + "="*178)
            print(f"【正在编写】")
            print("="*178 + "\033[0m")
            GameBoard1().start()
        case _:
            msg = "\n【尚未加入该模型，尽请期待！】\n"
            startColor = (54, 209, 220)
            endColor    = (91, 134, 229)
            print_gradient_text(msg, startColor, endColor)

# 预女猎白混
class GameBoard1():
    def __init__(self):
        
        # 全局变量
        self.DAY = "day_phase"
        self.NIGHT = "night_phase"
        self.day = 1
        self.phase = self.NIGHT
        self.game_over = False
        self.players:list[Player] = None
        self.alive_players:list[int] = None
        
        # 夜间行动变量
        self.wild_child_model:int = -1
        self.wolf_last_target:int = -1
        self.witch_last_target:int = -1
        self.witch_antidote:bool = True
        self.poisson_used_tonight = False
        self.hunter_shot = True
        self.prophet_last_target:int = -1
        self.prophet_options:list[int] = None
        self.night_log:str = ""
        
    
    def start(self):
        print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")
        
        self.players = create_players_from_roles(currentRoles)
        self.alive_players = [p.id for p in self.players if p.isAlive()]
        self.prophet_options = [p.id for p in self.players if not p.role.name == "预言家"]
        
        print('='*178)
        print("【请准备好身份牌并分发给每位对应玩家】")
        print('='*178)
        
        while(not self.game_over):
            
            print("\033[38;2;100;149;237m" + '='*178 + '\033[0m')
            showCurrentPlayers(self.players)
            print("\033[38;2;100;149;237m" + '='*178 + '\033[0m')
        
            if self.phase == self.NIGHT:
                self.nightPhase()
                self.day += 1
                self.phase = self.DAY
                
            elif self.phase == self.DAY:
                self.dayPhase()
                self.phase = self.NIGHT
            
        
        print("\033[38;2;255;105;180m" + "="*178 + "\033[0m")

    # 夜间行动
    def nightPhase(self):
        print("\033[38;2;135;206;250m" + '='*178 + '\033[0m')
        # 第一夜环节: 混子行动
        if self.day == 1:
            wild_child_options = [p.id for p in self.players if not p.role.name == "混子"]
            print('='*178)
            print("【混子请睁眼】")
            while not self.wild_child_model in wild_child_options:
                wild_child_model_str = input("请选择榜样的号码: ")
                try:
                    self.wild_child_model = int(wild_child_model_str)
                except ValueError:
                    print("\033[31m" + "="*178 + "\033[0m")
                    print("\033[31m" + "【注意！请选择以下有效数字: " + f"{wild_child_options}" "】\033[0m")
                    print("\033[31m" + "="*178 + "\033[0m")
                    continue
                if not self.wild_child_model in wild_child_options:
                    print("\033[31m" + "="*178 + "\033[0m")
                    print("\033[31m" + "【注意！请选择以下有效数字: " + f"{wild_child_options}" "】\033[0m")
                    print("\033[31m" + "="*178 + "\033[0m")
                    continue
            print("【混子请闭眼】")
            print('='*178)
        
        # 狼人行动
        print('='*178)
        print("【狼人请睁眼】")
        while not self.wolf_last_target in self.alive_players and not self.wolf_last_target == 0:
            wolf_last_target_str = input("请选择要击杀的玩家号码，如果空刀请输入 0: ")
            try:
                self.wolf_last_target = int(wolf_last_target_str)
            except ValueError:
                print("\033[31m" + "="*178 + "\033[0m")
                print("\033[31m" + "【注意！请选择以下有效数字: " + f"{self.alive_players}" "】\033[0m")
                print("\033[31m" + "="*178 + "\033[0m")
                continue
            if self.wolf_last_target not in self.alive_players and not self.wolf_last_target == 0:
                print("\033[31m" + "="*178 + "\033[0m")
                print("\033[31m" + "【注意！请选择以下有效数字: " + f"{self.alive_players}" "】\033[0m")
                print("\033[31m" + "="*178 + "\033[0m")
                continue
        print("【狼人请闭眼】")
        print('='*178)
        # 女巫行动
        print('='*178)
        print("【女巫请睁眼】")
        self.poisson_used_tonight = False
        if self.witch_antidote:
            print("今晚死的玩家是: " + f"{self.wolf_last_target} 号, " + "你要救吗?")
            use_antidote_str = input("(如果女巫选择了救， 请输入对应玩家号码。若没有救，请输入任意字节): ")
            try:
                use_antidote = int(use_antidote_str)
            except ValueError:
                use_antidote = 0
            
            if use_antidote == self.wolf_last_target:
                self.wolf_last_target = -1
                self.witch_antidote = False
                self.poisson_used_tonight = True
        else: 
            print("今晚死的玩家是: " + "???号" + " 你要救吗?")
            print("(女巫的解药已经使用，不需要告知击杀对象, 这只是流程。)")
            input("按下 <ENTER> 继续")
        
        print("女巫你有一瓶毒药，请选择要使用的玩家号码。")
        if self.poisson_used_tonight:
            print("(女巫今夜已经用过解药， 无法再使用毒药，仅流程。)")
            input("按下 <ENTER> 继续")

        else:
            while not self.witch_last_target in self.alive_players:
                witch_last_target_str = input("(输入女巫毒药使用玩家号码): ")
                try:
                    self.witch_last_target = int(witch_last_target_str)
                except ValueError:
                    print("\033[31m" + "="*178 + "\033[0m")
                    print("\033[31m" + "【注意！请选择以下有效数字: " + f"{self.alive_players}" "】\033[0m")
                    print("\033[31m" + "="*178 + "\033[0m")
                    continue
                if not self.witch_last_target in self.alive_players:
                    print("\033[31m" + "="*178 + "\033[0m")
                    print("\033[31m" + "【注意！请选择以下有效数字: " + f"{self.alive_players}" "】\033[0m")
                    print("\033[31m" + "="*178 + "\033[0m")
                    continue
        
        print("【女巫请闭眼】")
        print('='*178)
        # 猎人睁眼确认开枪状态
        print('='*178)
        print("【猎人请睁眼】")
        print("请确认你的开枪状态:")
        for p in self.players:
            if p.role.name == "猎人" and self.witch_last_target == p.id:
                self.hunter_shot = False
        if self.hunter_shot:
            print("【 YES 】")
            input("按下 <ENTER> 继续")
        else: 
            print("【 NO 】")
            input("按下 <ENTER> 继续")

        
        print("【猎人请闭眼】")
        print('='*178)
        # 第一夜环节：白痴确认没看错身份
        if self.day == 1:
            print('='*178)
            print("【白痴请睁眼】")
            print("确认白痴身份")
            input("按下 <ENTER> 继续")
            print("【白痴请闭眼】")
            print('='*178)
        # 预言家环节
        print('='*178)
        print("【预言家请睁眼】")
        
        while not self.prophet_last_target in self.prophet_options:
            prophet_last_target_str = input("请选择要查验的玩家号码: ")
            try:
                self.prophet_last_target = int(prophet_last_target_str)
            except ValueError:
                print("\033[31m" + "="*178 + "\033[0m")
                print("\033[31m" + "【注意！请选择以下有效数字: " + f"{self.prophet_options}" "】\033[0m")
                print("\033[31m" + "="*178 + "\033[0m")
                continue
            if self.prophet_last_target not in self.prophet_options:
                print("\033[31m" + "="*178 + "\033[0m")
                print("\033[31m" + "【注意！请选择以下有效数字: " + f"{self.prophet_options}" "】\033[0m")
                print("\033[31m" + "="*178 + "\033[0m")
                continue
        for p in self.players:
            if p.id == self.prophet_last_target:
                if p.role.team == "神职" or p.role.team == "村民":
                    print("他的身份是(请用相应手势示意，例：大拇指): 【好人】" )
                else:
                    print("他的身份是(请用相应手势示意，例：狼爪): 【狼人】" )
        input("按下 <ENTER> 继续")
        print("【预言家请闭眼】")
        print('='*178)
        
        # 自动判定
        self.night_log = f"\n【昨夜信息】\n"
        dead_players:list[int] = []
        
        for p in self.players:
            if p.id == self.witch_last_target:
                p.alive = False
                p.death_type = f"{p.death_type} 毒药"
                dead_players.append(p.id)
            if p.id == self.wolf_last_target:
                p.alive = False
                p.death_type = f"{p.death_type} 狼刀"
                dead_players.append(p.id)
        self.alive_players = [p.id for p in self.players if p.isAlive()]
        
        if dead_players == []:
            self.night_log += ("昨夜, 平安夜。")
        else:
            random.shuffle(dead_players)
            self.night_log += ("昨夜, " + f"{len(dead_players)}" + "死，死亡顺序不分先后" + 
                                f"{dead_players[0]}号，{dead_players[1]}号 倒牌")
        
        if self.day == 1:
            self.night_log += ("请发表遗言。\n")
        else:
            self.night_log += ("没有遗言。\n")
            
        print("\033[38;2;135;206;250m" + '='*178 + '\033[0m')
        # 先不判断游戏进度
        
        
        
            
            
    # 白天阶段
    def dayPhase(self):
        
        print("\033[38;2;255;215;0m" + '='*178 + '\033[0m')
        print(self.night_log)
        
        # 测试阶段直接结束游戏
        self.game_over = True
        
        print("\033[38;2;255;215;0m" + '='*178 + '\033[0m')


def showCurrentPlayers(players:list[Player]):
    print()
    for p in players:
        if p.role.team == "神职":
            color = "\033[38;5;220m"
        elif p.role.team == "狼人":
            color = "\033[38;5;196m"
        elif p.role.name == "混子" or p.role.team == "第三方":
            color = "\033[38;5;141m"
        elif p.role.team == "村民":
            color = "\033[38;5;94m"
        else:
            color = ""
        
        if p.isAlive():
            print(f"\t{p.id} 号玩家\t{color}【{p.role.name}】\033[0m")
        else:
            print(f"\t\033[9m{p.id} 号玩家\t\033[38;2;211;211;211m【{p.role.name}】\033[0m" + f" {p.deathType()}")
    print()

    
def create_players_from_roles(roles: list[Role]) -> list[Player]:
    """
    根据给定的 Role 列表，创建对应的 Player 列表。
    
    :param roles: 已选定的角色列表 actualRoles
    :param shuffle_roles: 是否先打乱角色顺序，默认 True
    :return: Player 对象列表
    """
    roles_copy = roles.copy()
    random.shuffle(roles_copy)
    
    players = []
    for idx, role in enumerate(roles_copy, start=1):
        players.append(Player(id=idx, role=role))
    return players

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
    2. 假面舞会
    3. 孤注一掷
    4. 机械狼通灵师
    5. 盗宝通灵
    6. 鬼魂新娘
    7. 骑士狼美
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
    msg = "\n【欢迎使用WerewolfManager！】\n"
    hotpink = (255, 105, 180)
    aqua    = (  0, 255, 255)
    print_gradient_text(msg, hotpink, aqua)
    main()