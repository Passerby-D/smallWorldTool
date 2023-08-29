import json

def fun1():
    temp_dict = {}

    with open('cards.json','r',encoding='utf-8') as f:
        card_infos = json.load(f)

    for cid in card_infos.keys():
        if 'data' not in card_infos[cid].keys() or card_infos[cid]['data']['level'] == 0:
            continue
        temp_dict.update({card_infos[cid]['id']:card_infos[cid]})

    with open('handled_cards.json','w',encoding='utf-8') as f:
        json.dump(temp_dict,f,indent=4,ensure_ascii=False)


def fun2():
    temp_dict = {}

    with open('handled_cards.json','r',encoding='utf-8') as f:
        card_infos = json.load(f)

    for id in card_infos.keys():
        temp_dict.update({card_infos[id]['cn_name']:id})

    with open('name2id.json','w',encoding='utf-8') as f:
        json.dump(temp_dict,f,indent=4,ensure_ascii=False)


if __name__ == '__main__':
    fun1()
    fun2()

