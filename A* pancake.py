import heapq
import copy
import timeit
import random
from asyncio import PriorityQueue

def main():
    # Random 10-layers pancake stack
    stack = list(range(1,11))
    random.shuffle(stack)

    # for user input
    print("Enter pancake stack")
    print("Enter \"r\" for a randomized 10-pancake stack.")
    user = input().strip()

    # input query loop
    valid_input = False
    # accept when if it is a valid stack or random r
    while not valid_input:
        if user == "r":
            valid_input = True
        elif not user.isdigit():
            print("Invalid input. Please try again: ")
            user = input().strip()
        else:
            user_stack = [int(digit) for digit in user]
            if not valid_stack(user_stack):
                print("Invalid stack. Please try again: ")
                user = input().strip()
            else:
                stack = user_stack
                valid_input = True

    # astar object
    AStar = astar(stack)

    # start the timer
    timer_start = timeit.default_timer()

    print("Running search...")
    # run the search algorithm
    AStar.run()

    # stop the timer
    timer_end = timeit.default_timer()

    # print the solution with the time taken
    AStar.print_result()
    print("A* search time:", round(timer_end - timer_start,2),"seconds")

class astar:
    def __init__(self, initial_state):
        # length of the pancake
        self.length = len(initial_state)
        # the step should be added to node
        self.steps = 0
        # array of seen states
        self.seen = set()
        # forward cost function in priority
        self.forward = PriorityQueue()
        # create the initial pancake node
        self.root = Stack_State(initial_state, None, self.steps)
        # put the node on priority queue
        self.forward.put(self.root)
        # increase the number by flips
        self.steps += 1

    def run(self):
        while True:
            # if the priority is empty then no solution
            if self.forward.empty():
                self.solution = False
                return

            # get the priority flip
            curr = self.forward.get()

            # adds the flip to list of seen flips
            self.seen.add(tuple(curr.state))

            # if heuristic function return 0, then meet the goal
            if curr.heuristic() == 0:
                self.solution = curr
                return

            # adds all possible of the pancake stacks from flip
            # current pancake stack is in priority
            for i in range(2, self.length+1):
                temp = copy.deepcopy(curr)
                temp.flip(i)
                temp.prev = curr
                temp.steps = self.steps

                # adds the temp states to priority queue if not in the queue
                if (not self.forward.contains_state(temp.state)) and (tuple(temp.state) not in self.seen):
                    self.forward.put(temp)

                # if the priority already has state, will replace the state if it has better cost
                elif self.forward.contains_state(temp.state):
                    self.forward.better_cost(temp)

                self.steps += 1

        # prints the end result of the A* search
    def print_result(self):
        if self.solution == False:
            print("No solution")
        else:
            path = []
            curr = self.solution
            while curr != None:
                path.append(curr)
                curr = curr.prev

            # if the length path = 1,the pancake is sorted
            if len(path) == 1:
                print("Pancake stack is already sorted")
                return

            path.reverse()

            print("Pancake stack is: ", path[0].state, "is solved by the following flip sequence: ")
            for step in range(1, len(path)-1):
                print("F", path[step].depth, ", ", end="", sep="")
            print("F", path[len(path) - 1].depth, sep="")

def valid_stack(stack):
    return sorted(stack) == list(range(1, len(stack) + 1))

# stack class
class Stack_State:
    def __init__(self, state, prev, steps):
        self.state = state
        self.prev = prev
        self.backward_cost = 0
        self.steps = steps

    # comparator for heap
    def __lt__(self, other):
        if self.get_total() != other.get_total():
            return self.get_total() < other.get_total()
        else:
            return self.steps < other.steps

    # curr node and get total
    def get_total(self):
        return self.heuristic() + self.backward_cost

    # flips the stack with given depth
    def flip(self, depth):
        self.depth = depth
        self.state[:depth] = reversed(self.state[:depth])
        self.backward_cost += depth

    # heuristic function
    def heuristic(self):
        hgap = 0
        for i in range(1,len(self.state)):
            if abs(self.state[i] - self.state[i-1]) != 1:
                hgap += 1
        return hgap

# Priority Queue
class PriorityQueue():
    # default constructor; initializes the heap, represented by a list
    def __init__(self):
        self.heap = []

    # return when it empty
    def empty(self):
        return len(self.heap) == 0

    # put the node in priority queue
    def put(self, node):
        heapq.heappush(self.heap, node)

    # pop the node from the heap nd gets with lowest cost
    def get(self):
        top = heapq.heappop(self.heap)
        return top

    # checks to see if the given state is already in the priority queue
    def contains_state(self, state):
        for node in self.heap:
            if node.state == state:
                return True
        return False

    # if a node's state is already in the priority, then calculate the best cost
    def better_cost (self, new_node):
        for node in self.heap:
            if node.state == new_node.state:
                if node.get_total() > new_node.get_total():
                    self.heap[self.heap.index(node)] = new_node

if __name__ == '__main__':
    main()











