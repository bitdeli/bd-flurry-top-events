from bitdeli.widgets import Title, Description, set_theme
from bitdeli.chain import Profiles
from collections import Counter

set_theme('sail')

text = {}

def stats(profiles):
    stats = Counter()
    apps = Counter()
    for profile in profiles:
        for session in profile['sessions']:
            apps[session['$app']] += 1
            for event in session['l']:
                stats[event['e']] += 1
                
    top_apps = apps.most_common()
    top_events = stats.most_common()
    text['applist'] = '\n'.join(' - **%s**: %d sessions' % app
                                for app in top_apps)
    text['total'] = total = float(sum(stats.itervalues()))
    text['top'] = top_events[0][0]
    
    yield {'type': 'text',
           'size': (12, 2),
           'label': 'Top Application',
           'color': 2,
           'head': top_apps[0][0]}
    
    yield {'type': 'text',
           'size': (4, 2),
           'label': 'Total Number of Events (All Apps)',
           'head': int(total)}
    
    yield {'type': 'table',
           'size': (12, 5),
           'label': 'Events',
           'chart': {'Percent': 'bar'},
           'data': [{'Event': event,
                     'Count': count,
                     'Percent': count / total}
                    for event, count in top_events]}

Profiles().map(stats).show()

Title("The most common event is *{top}*", text)

Description("Currently tracking the following applications:\n\n"
            "{applist}", text)    

