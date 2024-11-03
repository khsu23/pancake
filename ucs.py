import heapq
import copy
import timeit
import random

def main():
    # Randomized 10-long pancake stack
    stack = list(range(1, 11))
    random.shuffle(stack)

    # user input
    print("Enter pancake stack ")
    print("Enter \"r\" for a randomized 10-pancake stack.")
    user = input()

    # Input query loop
    valid_input = False
    while not valid_input:
        if not user.isdigit() and user != "r":
            print("Invalid input. Please try again: ")
            user = input()
        elif user != "r" and not valid_stack([int(digit) for digit in user]):
            user = input()
        else:
            valid_input = True

    # Convert input into an array
    if user.isdigit():
        stack = [int(digit) for digit in user]

    # Create UCS object
    UCS = ucs(stack)

    # Start the timer
    timer_start = timeit.default_timer()

    print("Running search...")
    # Run the search algorithm
    UCS.run()

    # Stop the timer
    timer_end = timeit.default_timer()

    # Print the solution with the time taken
    UCS.print_result()
    print("Uniform cost search time:", round(timer_end - timer_start, 2), "seconds")

def valid_stack(stack):
    # Check if the stack is valid, it should be largest num at btm
    if max(stack) != stack[-1]:
        print("Largest plate must be on the bottom. Please try again.")
        return False
    if sorted(stack) != list(range(min(stack), max(stack) + 1)):
        print("Pancake stack should consist only of consecutive numbers. Please try again.")
        return False
    return True

class ucs():
    # UCS implementation for sorting
    def __init__(self, initial_state):
        self.length = len(initial_state)
        self.steps = 0
        self.seen = []
        self.forward = PriorityQueue()
        self.root = Stack_State(initial_state, None, self.steps)
        self.forward.put(self.root)
        self.steps += 1

    def run(self):
        # run the UCS
        while True:
            if self.forward.empty():
                self.solution = False
                return

            curr = self.forward.get()
            self.seen.append(curr.state)

            if curr.goal_test() == 0:
                self.solution = curr
                return

            for i in range(2, self.length):
                temp = copy.deepcopy(curr)
                temp.flip(i)
                temp.prev = curr
                temp.steps = self.steps

                if not self.forward.contains_state(temp.state) and temp.state not in self.seen:
                    self.forward.put(temp)
                elif self.forward.contains_state(temp.state):
                    self.forward.better_cost(temp)

                self.steps += 1

    def print_result(self):
        # print the result
        if self.solution == False:
            print("Problem has no solution")
        else:
            path = []
            curr = self.solution
            while curr is not None:
                path.append(curr)
                curr = curr.prev

            if len(path) == 1:
                print("Pancake stack is already sorted!")
                return

            path.reverse()
            print("The pancake stack", path[0].state, "is solved by the following flip sequence:")
            for step in range(1, len(path) - 1):
                print("F", path[step].depth, ", ", end="", sep="")
            print("F", path[len(path) - 1].depth, sep="")

class Stack_State:
    def __init__(self, state, prev, steps):
        self.state = state
        self.prev = prev
        self.backward_cost = 0
        self.steps = steps

    def __lt__(self, other):
        # Define the less-than operator for priority queue
        return self.get_total() < other.get_total() or (self.get_total() == other.get_total() and self.steps < other.steps)

    def get_total(self):
        # total cost
        return self.backward_cost

    def flip(self, depth):
        # flip the depth
        self.depth = depth
        for i in range(depth // 2):
            self.state[i], self.state[depth - i - 1] = self.state[depth - i - 1], self.state[i]
        self.backward_cost += depth

    def goal_test(self):
        # test the goal
        hgap = 0
        for i in range(1, len(self.state)):
            if abs(self.state[i] - self.state[i - 1]) != 1:
                hgap += 1
        return hgap

class PriorityQueue:
    # heapg priority for the node
    def __init__(self):
        self.heap = []

    def empty(self):
        # Check if the priority queue is empty
        return len(self.heap) == 0

    def put(self, node):
        # Add a node to the priority queue
        heapq.heappush(self.heap, node)

    def get(self):
        # return the node with the lowest cost
        return heapq.heappop(self.heap)

    def contains_state(self, state):
        # check the state is already in the queue
        return any(node.state == state for node in self.heap)

    def better_cost(self, new_node):
        # update the best cost if found
        for node in self.heap:
            if node.state == new_node.state and node.get_total() > new_node.get_total():
                self.heap[self.heap.index(node)] = new_node

if __name__ == '__main__':
    main()

