import json
from name2id import name2id


def sw1(start,end):
    try:
        int(start)
    except:
        start=name2id(start)

    try:
        int(end)
    except:
        end=name2id(end)

    with open("handled_cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)

    record=[]
    for i in cards.keys():
        same_times=0
        if cards[start]['data']['attribute']==cards[i]['data']['attribute']:same_times+=1
        if cards[start]['data']['atk']==cards[i]['data']['atk']:same_times+=1
        if cards[start]['data']['def']==cards[i]['data']['def']:same_times+=1
        if cards[start]['data']['level']==cards[i]['data']['level']:same_times+=1
        if cards[start]['data']['race']==cards[i]['data']['race']:same_times+=1
        if same_times==1:
            if cards[end]['data']['attribute']==cards[i]['data']['attribute']:same_times+=1
            if cards[end]['data']['atk']==cards[i]['data']['atk']:same_times+=1
            if cards[end]['data']['def']==cards[i]['data']['def']:same_times+=1
            if cards[end]['data']['level']==cards[i]['data']['level']:same_times+=1
            if cards[end]['data']['race']==cards[i]['data']['race']:same_times+=1
            if same_times==2:
                record.append(cards[i]['cn_name'])

    with open("test2.json", "w", encoding="utf-8") as f:
        json.dump(record, f, indent=4, ensure_ascii=False)
    return record


def sw2(deckPath,start_id):


    with open("./handled_cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)


    with open(deckPath, "r", encoding="utf-8") as f:
        deck = f.readlines()
        try:
            start=deck.index('#main\n')+1
            end=deck.index('#extra\n')
            main_deck=[]
            for i in range(start,end):
                temp_card=deck[i].strip()
                if temp_card not in main_deck:
                    if temp_card in cards.keys():
                        main_deck.append(temp_card)
        except:
            return '请使用正确的卡组码'
    
    print(main_deck)
    try:
        start_id = int(start_id)
    except:
        start_id=name2id(start_id,main_deck)


    print(start_id)

    if start_id not in main_deck:
        return '请输入正确的卡名或id！'


    path=[]
    end=[]

    for j in main_deck:
        same_times=0
        if cards[j]['data']['attribute']==cards[start_id]['data']['attribute']:same_times+=1
        if cards[j]['data']['atk']==cards[start_id]['data']['atk']:same_times+=1
        if cards[j]['data']['def']==cards[start_id]['data']['def']:same_times+=1
        if cards[j]['data']['level']==cards[start_id]['data']['level']:same_times+=1
        if cards[j]['data']['race']==cards[start_id]['data']['race']:same_times+=1
        if same_times==1:
            for k in main_deck:
                same_times=0
                if cards[k]['data']['attribute']==cards[j]['data']['attribute']:same_times+=1
                if cards[k]['data']['atk']==cards[j]['data']['atk']:same_times+=1
                if cards[k]['data']['def']==cards[j]['data']['def']:same_times+=1
                if cards[k]['data']['level']==cards[j]['data']['level']:same_times+=1
                if cards[k]['data']['race']==cards[j]['data']['race']:same_times+=1
                if same_times==1 and int(cards[j]['data']['level'])*int(cards[k]['data']['level'])>0:
                    path.append([cards[j]['cn_name'],cards[k]['cn_name']])
                    if cards[k]['cn_name'] not in end:
                        end.append(cards[k]['cn_name'])

    conclusion=''
    for i in end:
        conclusion+=' | '+ i


    
    msgs=[conclusion]
    end_count=[]
    for i in path:
        if i[1] not in end_count:
            msg = []
            msg.append('*'+i[1]+'*')
            end_count.append(i[1])
            for j in path:
                if j[1]==i[1]:
                    msg.append(cards[start_id]['cn_name']+'-->'+j[0]+'-->'+j[1])
            msgs.append(msg)

    return msgs if conclusion else '没有可检索的目标'

