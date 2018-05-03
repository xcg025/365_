interval_cond = {'fsdafas': 1}
interval = interval_cond.get('hhh', None)
print(interval)
if interval == None:
    print(interval)

score = '3:5'
score_a = int(score.split(':')[0])
score_b = int(score.split(':')[1])
if abs(score_a - score_b) <= 1:
    print('dasfasf')
