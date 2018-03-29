import pandas
import json

fight_data = "/Users/Darragh/College/DataVis/mma_visualization/ufc_data/ufc-fighters-fight-data-from-fightmetriccom/Fights_Edit.csv"

weightclasses = {'Flyweight': 0, 'Bantamweight': 1, 'Featherweight': 2, 'Lightweight': 3, 'Welterweight': 4, 'Middleweight': 5,
                'Light Heavyweight': 6, 'Heavyweight': 7, 'Women\'s Strawweight': 8, 'Women\'s Bantamweight': 9}


# TODO:// Filter out weightclasses such as Ultimate Fighter Australia vs. UK Lightweight Tournament &&
# Ultimate Fighter 17 Middleweight Tournament also interim title fights

def parse_matchup(match):
    index = match.find('   VS')
    if index == -1:
        index = match.find('  VS')
        fighter_1 = match[:index].rstrip()
        fighter_2 = match[index + 6:].rstrip()
    else:
        fighter_1 = match[:index].rstrip()
        fighter_2 = match[index + 7:].rstrip()
    return (fighter_1, fighter_2)

def parse_winner(fighter_1, fighter_2, f1_outcome):
    if f1_outcome == 'W':
        return (fighter_1, fighter_2)
    else:
        return (fighter_2, fighter_1)

def parse_weightclass(weightclass):
    index = weightclass.find(' Title Bout')
    if index == -1:
        index = weightclass.find(' Bout')
        parsed_wc = weightclass[:index]
    else:
        parsed_wc = weightclass[:index]
        parsed_wc = parsed_wc[4:]
        print(parsed_wc)

    if parsed_wc in weightclasses:
        return weightclasses[parsed_wc]
    else:
        return 10

def check_duplicate(fights, fighter):
    for x in fights['nodes']:
        # print(x['id'])
        if x['id'] == fighter:
            return False
    return True

def check_rematches(fights, fighter_1, fighter_2):
    for x in fights['links']:
        # print(x['source'])
        # print(x['target'])
        if x['source'] == fighter_1 and x['target'] == fighter_2:
            return False
        if x['source'] == fighter_2 and x['target'] == fighter_1:
            return False
    return True

if __name__ == '__main__':
    ufc_fight_data = pandas.read_csv(fight_data, sep=",")

    json_file = open("fights.json", 'w')

    fights = {}
    fights['nodes'] = []
    fights['links'] = []

    weightclass_filter = 0

    for index, row in ufc_fight_data.iterrows():
        if str(row.Matchup) != "nan":
            (fighter_1, fighter_2) = parse_matchup(str(ufc_fight_data.Matchup[index]))
            (fighter_w, fighter_l) = parse_winner(fighter_1, fighter_2, str(ufc_fight_data.F1Outcome[index]))
            # print(fighter_w)

            weightclass_group = parse_weightclass(ufc_fight_data.Weightclass[index])

            if check_duplicate(fights, fighter_w):
                if weightclass_group == weightclass_filter:
                    fights['nodes'].append({'id': fighter_w, 'group': weightclass_group})
                elif weightclass_filter == -1:
                    fights['nodes'].append({'id': fighter_w, 'group': weightclass_group})

            if check_duplicate(fights, fighter_l):
                if weightclass_group == weightclass_filter:
                    fights['nodes'].append({'id': fighter_l, 'group': weightclass_group})
                elif weightclass_filter == -1:
                    fights['nodes'].append({'id': fighter_l, 'group': weightclass_group})

            if check_rematches(fights, fighter_1, fighter_2):
                if weightclass_group == weightclass_filter:
                    fights['links'].append({'source': fighter_w, 'target': fighter_l, 'value': 1})
                elif weightclass_filter == -1:
                    fights['links'].append({'source': fighter_w, 'target': fighter_l, 'value': 1})

    print(fights)
    json_file.write(json.dumps(fights))