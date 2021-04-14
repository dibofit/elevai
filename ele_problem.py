import gym
from gym import spaces

class Elevator:
    def __init__(self,num_floor):
        self.ppls_destinations = [[]*num_floor]
        self.floors = [Floor() for i in range(num_floor)]
        
        #0~num_floor-1
        self.location = 0 
        self.waiting_times = []

    def ppl_ride(self):
        #people ride from current floor
        cur_floor = self.floors[self.location]

        #each person is recorded and presses their destination floor
        for person in cur_floor.ppl:
            self.ppls_destinations[person.destination].append(person)

        cur_floor.button_pressed = False
        cur_floor.ppl = []

    def ppl_get_off(self,cur_step_count):
        
        ppl_getting_off = self.ppls_destinations[self.location]
        for person in ppl_getting_off:
            person.end_time = cur_step_count
            self.waiting_times.append(person.get_time_taken())

        ppl_getting_off = []

    def move_up(self):
        self.location = min(num_floor-1,self.location+1)
        self.ppl_get_off()
        self.ppl_ride()

    def move_down(self):
        self.location = max(0,self.location-1)
        self.ppl_get_off()
        self.ppl_ride()


class Floor:
    def __init__(self):
        self.button_pressed = False
        self.ppl = []

    def make_person(self,person):
        self.ppl.append(person)


class Person:
    def __init__(self,start_time, destination):
        self.start_time = start_time
        self.end_time = -1
        self.destination = destination

    def get_time_taken(self):
        return self.end_time - self.start_time

class EleEnvi(gym.Env):
    def __init__(self,num_floors,num_elevators):
        super(EleEnvi,self).__init__()

        self.num_elevators = num_elevators

        #action: 0 => move down, 1 => don't move, 2 => move up
        self.action_space = spaces.MultiDiscrete([3]*num_elevators)

        #elevator location, number of steps taken
        self.location = 0
        self.step_counter = 0

        #observation:
        #location => Discrete(num_floors)
        #whether buttons in elevator pressed => MultiBinary(num_floors*num_elevators)
        #whether buttons on each floor pressed => MultiBinary(num_floors)
        self.observation_space = spaces.Tuple(spaces.MultiDiscrete([num_floors]*num_elevators),
                spaces.MultiBinary(num_floors*num_elevators),
                spaces.MultiBinary(num_floors))

        self.elevators = [Elevator(num_floors) for i in range(num_elevators)]
    
    def step(self,action):
        assert self.action_space.contains(action), "invalid action"

        for i in range(self.num_elevators):
            if action[i] == 0:
                self.elevator[i].move_down()
            elif action[i] == 2:
                self.elevator[i].move_up()

        self.state = ()
        done = False
        reward = 0

        return np.array(self.state), reward,done,{}

    def reset(self):

    def render(self):
        pass

