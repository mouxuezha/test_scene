PROMPT_TEMPLATES = {
        "llm_chat": {
            "default":
                '{{ input }}',

            "with_history":
                'Answer my questions considering the coversation history.'
                'If you do not know the answer, just say do not know. \n\n'
                'Current conversation:\n'
                '{history}\n',
                
            "embrace":
                '请作为兵棋推演游戏的玩家，设想一个陆战作战场景。'
                '我方为红方，拥有坦克、步兵战车、自行迫榴炮、无人突击车和无人机、导弹发射车等装备，步兵下车后作战，'
                '请根据我的意图，生成相应的命令，对场景进行调整。\n'
                '在生成指令时，可以考虑历史态势和指令，下面是我们的对话历史：\n'
                '{history}'
                '不同的装备对应不同的装备类型，红方坦克：MainBattleTank_ZTZ100，蓝方坦克：MainBattleTank_ZTZ200，红方步兵战车：WheeledCmobatTruck_ZB100，蓝方步兵战车：WheeledCmobatTruck_ZB200，步兵班：infantry，自行迫榴炮：Howitzer_C100，无人突击车：ArmoredTruck_ZTL100，无人机：ShipboardCombat_plane，导弹发射车：missile_truck。此外，我们约定红方team_id为0，蓝方team_id为1\n'
                '请按照以下格式给出场景编辑指令。\n 增加装备：[add, unit_type=xxx, team_id=xxx], 如增加一辆红方坦克，则指令为[add, unit_type=MainBattleTank_ZTZ100, team_id=0]，增加两个蓝方步兵班，则指令为发送两遍[add, unit_type=infantry, team_id=1] \n 删除装备：[delete, unit_type=xxx, team_id=xxx], 如删除一辆红方步兵战车，则指令为[delete, unit_type=WheeledCmobatTruck_ZB100, team_id=0]',
        
            "jieshuo_embrace":
                '请作为解说员，解说一场兵棋推演比赛，尽量讲清楚双方作战过程和行动逻辑。场景如下：'
                '红方拥有坦克、步兵战车、自行迫榴炮、无人突击车和无人机、导弹发射车等装备，步兵下车后作战，'
                '红方需要攻取位于经纬度坐标(2.7100,39.7600)的夺控点，要将陆战装备移动到夺控点处并消灭夺控点附近敌人，地图范围为经度2.6000到2.8000，纬度范围为39.6500到39.8500，导弹发射车不能机动。地图西北方向为海洋，其余部分为陆地。陆地中间部分为山区，装备单位经过山区会由于坡度地形因素，导致行进速度减慢，夺控点周围是一片平原。'
                '蓝方则试图阻击，拥有更多的步兵力量和反导能力。'
                '每隔一定步数，我将告诉你红蓝态势和其他信息，并由你来生成解说词\n'
                '在生成指令时，可以考虑历史态势和指令，下面是我们的对话历史：\n'
                '{history}'
            #
            # "embrace": embrace_lang + '在生成指令时，可以考虑历史态势和指令，下面是我们的对话历史：\n {history}'
        
        }
    }
