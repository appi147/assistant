from pycricbuzz import Cricbuzz


c = Cricbuzz()


def cleanhtml(text):
    resp = []
    text = text.split('<br/>')
    for i in text:
        if len(i):
            resp.append(i)
    return resp


def commentary(mid):
    resp = []
    data = c.commentary(mid)
    for lines in data['commentary']:
        resp.extend(cleanhtml(lines))
    return resp


# Credits to umangahuja1
def live_score(mid):
    resp = []
    data = c.livescore(mid)
    score = {}
    score['matchinfo'] = "{}, {}".format(data['matchinfo']['mnum'], data['matchinfo']['mchdesc'])
    score['status'] = "{}, {}".format(data['matchinfo']['mchstate'].title(), data['matchinfo']['status'])
    score['bowling'] = data['bowling']
    score['batting'] = data['batting']

    text = ''
    text += score['matchinfo'] + '\n' + score['status'] + '\n'
    text += score['batting']['team'] + '\n'
    resp.append(text)

    text = ''
    for scr in reversed(score['batting']['score']):
        text += "{} :- {}/{} in {} overs\n".format(scr['desc'], scr['runs'], scr['wickets'], scr['overs'])
    for b in reversed(score['batting']['batsman']):
        text += "{} : {}({}) \n".format(b['name'].strip('*'), b['runs'], b['balls'])
    text += "\n" + score['bowling']['team'] + '\n'
    resp.append(text)

    text = ''
    for scr in reversed(score['bowling']['score']):
        text += "{} :- {}/{} in {} overs\n".format(scr['desc'], scr['runs'], scr['wickets'], scr['overs'])
    for b in reversed(score['bowling']['bowler']):
        text += "{} : {}/{} \n".format(b['name'].strip('*'), b['wickets'], b['runs'])
    return resp


# Credits to umangahuja1
def scorecard(mid):
    resp = []
    data = c.scorecard(mid)
    card = {}
    card['matchinfo'] = "{}, {}".format(data['matchinfo']['mnum'], data['matchinfo']['mchdesc'])
    card['status'] = "{}, {}".format(data['matchinfo']['mchstate'].title(), data['matchinfo']['status'])
    card['scorecard'] = data['scorecard']
    text = ''
    text += card['matchinfo'] + '\n' + card['status'] + '\n'
    resp.append(text)

    for scr in reversed(card['scorecard']):
        text = ''
        text += "{} {}\n{}/{} in {} overs\n\n".format(scr['batteam'], scr['inngdesc'], scr['runs'], scr['wickets'], scr['overs'])
        text += "Batting\n"
        text += "{:<17} {:<3} {:<3} {:<3} {}\n".format('Name', 'R', 'B', '4', '6')
        for b in scr['batcard']:
            text += "{:<17} {:<3} {:<3} {:<3} {}\n{}\n".format(b['name'], b['runs'], b['balls'], b['fours'], b['six'], b['dismissal'])
        text += "-" * 35 + "\n"
        text += "Bowling\n"
        text += "{:<17} {:<5} {:<3} {:<3} {}\n\n".format('Name', 'O', 'M', 'R', 'W')
        for b in scr['bowlcard']:
            text += "{:<17} {:<5} {:<3} {:<3} {}\n\n".format(b['name'], b['overs'], b['maidens'], b['runs'], b['wickets'])
        resp.append(text)
    return resp


def preview():
    resp = []
    current_matches = c.matches()
    for match in current_matches:
        if match['mchstate'] == 'preview':
            resp.append(match['srs'])
            resp.append(match['mchdesc'])
            resp.append(match['mnum'])
            resp.append(match['status'])
            resp.extend(commentary(match['id']))
    return resp


def result():
    resp = []
    current_matches = c.matches()
    for match in current_matches:
        if match['mchstate'] == 'Result':
            resp.extend(scorecard(match['id']))
    return resp


def live():
    resp = []
    current_matches = c.matches()
    for match in current_matches:
        if match['mchstate'] == 'live':
            resp.append(live_score(match['id']))
    return resp

if __name__ == '__main__':
    for r in result():
        print(r)
