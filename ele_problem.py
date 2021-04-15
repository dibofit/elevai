import gym
from gym import spaces

class Elevator:
    def __init__(self,floors):

        self.num_floors = len(floors)
        self.ppls_destinations = [[]]*self.num_floors
        self.floors = floors
        self.time_counter = 0
        
        #0~num_floor-1
        self.location = 0 

    def ppl_ride(self):
        #people ride from current floor
        cur_floor = self.floors[self.location]

        #each person is recorded and presses their destination floor
        for person in cur_floor.ppl:
            self.ppls_destinations[person.destination].append(person)

        cur_floor.button_pressed = False
        cur_floor.ppl = []

    def ppl_get_off(self):
        
        waiting_times = []

        ppl_getting_off = self.ppls_destinations[self.location]
        for person in ppl_getting_off:
            person.end_time = self.time_counter
            waiting_times.append(person.get_time_taken())

        ppl_getting_off = []

        return waiting_times

    def move_up(self):
        self.time_counter += 1
        self.location = min(self.num_floors-1,self.location+1)
        waiting_times = self.ppl_get_off()
        self.ppl_ride()
        return waiting_times

    def move_down(self):
        self.time_counter += 1
        self.location = max(0,self.location-1)
        waiting_times = self.ppl_get_off()
        self.ppl_ride()
        return waiting_times

    def dont_move(self):
        self.time_counter += 1



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
        self.num_floors = num_floors

        #action: 0 => move down, 1 => don't move, 2 => move up
        self.action_space = spaces.MultiDiscrete([3]*num_elevators)

        # number of steps taken
        self.step_counter = 0

        #observation:
        #location => Discrete(num_floors)
        #whether buttons in elevator pressed => MultiBinary(num_floors*num_elevators)
        #whether buttons on each floor pressed => MultiBinary(num_floors)
        self.observation_space = spaces.Tuple((spaces.MultiDiscrete([num_floors]*num_elevators),
                spaces.MultiBinary(num_floors*num_elevators),
                spaces.MultiBinary(num_floors)))

        self.floors = [Floor()]*num_floors
        self.elevators = [Elevator(self.floors)]*num_elevators

        self.buttons_on_floor = [False]*num_floors
        self.buttons_on_ele = [[False]*num_floors]*num_elevators
        self.ele_locations = [0]*num_elevators

    def step(self,action):
        assert self.action_space.contains(action), "invalid action"
        
        print(action)

        wait_times = []
        
        for i in range(self.num_elevators):
            if action[i] == 0:
                wait_times.append(self.elevators[i].move_down())
            elif action[i] == 1:
                self.elevators[i].dont_move()
                wait_times.append([])
            else:
                wait_times.append(self.elevators[i].move_up())

            for j in range(self.num_floors):
                self.buttons_on_ele[i][j] = (len(self.elevators[i].ppls_destinations[j])>0)

            self.ele_locations[i] = self.elevators[i].location

        for i in range(self.num_floors):
            self.buttons_on_floor[i] = self.floors[i].button_pressed

        #testing state: need to fix later 
        self.state = (self.ele_locations,wait_times[-1],self.buttons_on_floor,self.buttons_on_ele)
        done = False
        reward = 0
        
        self.step_counter += 1
        return self.state, reward,done,{}

    def reset(self,ppl_queue):
        #set elevator positions to 0th floor
        pass
        #receive queue of people: the queue will describe when and where they appear in the building

    def render(self):
        pass

