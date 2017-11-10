import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 8,8

'''
Inspired by the book Bursts by Barabasi
In this script we explore page ~124
The idea that wait times in priority lists
have a bursty or power law like signature

Algorithm:
1. Create a to do list ranked by priority
2. Execute top priority item
3. Add another item with random priority
Repeat 2 and 3
Record time each item was on list before execution
Plot resulting wait times, it should have a power law dist

Routines:
-> Have a timer running
-> Have a completed items list
-> Log time when item entered list
-> Log time when item leaves list
-> List structred using numpy array of tuples
-> Each tuple contains item priority, entered time and leaving time
-> Priority goes by numerical sorting
-> Run until completed items reaches statistic signficance
-> Take diffs of start and stop time
-> Plot the diffs
'''

### Setting parameters
time = 0 #holds current time 
todo = 20 #length of todo list
end = 150 #number of items to complete before statistics

### Initializing variables
completed = np.array([0,0,0])
start = np.array([[np.random.random(),0,np.nan] for x in np.arange(todo)])
todo_holder = []

while len(completed) < end:
	###For tracking purposes
	todo_holder.append(start[:,0])
	### Moving time forward
	time += 1
	
	# Picking of top priority task
	leave = start[0]
	leave = [leave[0],leave[1],time]
	start = start[1:]
	
	### Adding the completed task to completed array
	completed = np.vstack([completed,leave])
	
	### Adding item of random priority
	# Assigning random priority to new item
	new_priority = np.random.randint(len(start)+1)
	# Placing item in todo list
	temp = start[:new_priority]
	temp = np.vstack([temp,[10*np.random.random(),time,np.nan]])
	temp = np.vstack([temp,start[new_priority:]])
	
	### Reset for repeat
	start = temp

### Creating array of completion times
completion_times = completed[:,2]-completed[:,1]

### Plotting a histogram
x = plt.hist(completion_times)
plt.title('Distribution of times to completion of each item')
plt.xlabel('Completion Times / Iterations')
plt.ylabel('Counts')
plt.show()

todo_holder = np.array(todo_holder)

rcParams['figure.figsize'] = 8,30
plt.imshow(todo_holder,aspect='auto',interpolation='nearest',cmap='jet')
plt.xlabel('ToDo List Priority (0 highest)')
plt.ylabel('Iterations')
plt.title('ToDo List Tracker: New Color is New Item')
plt.show()


'''
Note how the lower down in rank an item (or color) starts, the longer
it sustains. The idea is that distribution of time the items (or colors)
sustain follows a power law.
'''
