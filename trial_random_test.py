import numpy as np

trials_odd = np.zeros(int(200*0.3))
trials_stand = np.ones(int(200*0.7))
all_trials = np.concatenate([trials_odd, trials_stand])

random_trials = np.random.choice(all_trials, 200, replace=False)
odd_count = 0
stand_count = 0

for current in random_trials:
    # pick one random number

    print(current)

    if current == 1:
        odd_count += 1
    else:
        stand_count += 1

print('odd ', odd_count)
print('standard ', stand_count)

    # delete one number from the array
