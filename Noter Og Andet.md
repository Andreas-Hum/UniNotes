# Author
**Andreas Hummelmose**  
*Computer Science Student, 5th Semester, Aalborg University*  
[LinkedIn: Andreas Hummelmose](https://www.linkedin.com/in/andreas-hummelmose-77580a252/)

# Noter til AI der skal addes

Purpose agent,

organization (group of agents working together)

Trading agent (it gets goods and services for the user)

Design space (might be state space)

the world state so the state of the world 

belief state (internal state)

eviorment state



The ten dimensions

1 modularity

2 planning horizon

3 representation

relation and individiual vproperty

features of the state (could be position, direction or something) and why its good and sometimes easier to look for features instead of specific states

4  Computational limits

perfect rationality
bounded rationality

5 learning

Knowledge is given or learned

6 uncertainty

Sensing uncertainty

Fully observable means the agent knows the exact state of the world from the stimuli 
Partially observable the agent does not directly observer the world state, this occurs when there are many possible states that can result from the same stimuli or when stimuli are misleading

effect uncertainty

Determanistic when the state resulting from an action is determined by an action and  the prior state

Stochastic when there is a probability distribution over the resulting states

Symbolic vs subsymbolic

# 1. General Algorithms/Data Structures
## 1.1 Data Structures
### 1.1.1 Linear Data Structures

#### 1.1.1.1 Arrays
An **Array** is a collection of items stored at contiguous memory locations. Arrays are fundamental data structures used to store elements of the same type, such as integers or strings, and provide fast access to elements using an index. Arrays can be single-dimensional, multi-dimensional, and are commonly used due to their simplicity and efficiency in accessing elements.

##### **Operations:**
- **Accessing an element:** $O(1)$
- **Insertion (at a specific position):** $O(n)$
- **Deletion (at a specific position):** $O(n)$

##### **Applications:**
- **Static Data Storage:** Arrays are used when the number of elements is known and fixed, such as storing fixed-size collections like a list of students or an array of temperatures.

##### **Pseudocode:
```plaintext
CLASS Array
    VARIABLE elements
    VARIABLE size

    FUNCTION InitializeArray(size)
        elements ← new array of size
        size ← 0
    END FUNCTION

    FUNCTION AccessElement(index)
        RETURN elements[index]
    END FUNCTION

    FUNCTION InsertElement(index, value)
        IF size = length(elements) THEN
            PRINT "Array is full"
            RETURN
        END IF
        FOR i FROM size TO index BY -1 DO
            elements[i] ← elements[i-1]
        END FOR
        elements[index] ← value
        size ← size + 1
    END FUNCTION

    FUNCTION DeleteElement(index)
        FOR i FROM index TO size - 2 DO
            elements[i] ← elements[i+1]
        END FOR
        size ← size - 1
    END FUNCTION

    FUNCTION DisplayArray()
        FOR i FROM 0 TO size - 1 DO
            PRINT elements[i]
        END FOR
    END FUNCTION
END CLASS
```

---
#### 1.1.1.2 Linked Lists
##### 1.1.1.2.1 Node
A **Node** is the fundamental building block for linked lists. Each node contains data and a reference (or pointer) to the next node in the sequence. In the case of a doubly linked list, each node also contains a reference to the previous node.
###### **Pseudocode:**
```plaintext
CLASS Node
    VARIABLE data
    VARIABLE next

    FUNCTION InitializeNode(value)
        data ← value
        next ← NULL
    END FUNCTION
END CLASS
```

---
##### 1.1.1.2.2 Singly Linked List
A **Singly Linked List** is a type of linked list where each node points to the next node in the sequence, and the last node points to `NULL`. It allows for efficient insertion and deletion of elements at the beginning or end of the list.

###### **Operations:**
- **Insertion at the beginning:** $O(1)$
- **Insertion at the end:** $O(n)$
- **Deletion:** $O(1)$ (at the beginning), $O(n)$ (at the end or for specific nodes)
- **Search:** $O(n)$

###### **Applications:**
- **Dynamic Data Storage:** Singly linked lists are ideal when the data size is dynamic, and there is a frequent need for insertion and deletion of elements.
- **Stacks and Queues Implementation:** Singly linked lists can be used to implement stacks and queues dynamically.

###### **Pseudocode:**
```plaintext
CLASS SinglyLinkedList
    VARIABLE head

    FUNCTION InitializeLinkedList()
        head ← NULL
    END FUNCTION

    FUNCTION InsertAtBeginning(value)
        newNode ← Node(value)
        newNode.next ← head
        head ← newNode
    END FUNCTION

    FUNCTION InsertAtEnd(value)
        newNode ← Node(value)
        IF head IS NULL THEN
            head ← newNode
        ELSE
            current ← head
            WHILE current.next IS NOT NULL DO
                current ← current.next
            END WHILE
            current.next ← newNode
        END IF
    END FUNCTION

    FUNCTION DeleteNode(value)
        IF head IS NULL THEN
            RETURN
        END IF
        IF head.data = value THEN
            head ← head.next
            RETURN
        END IF
        current ← head
        WHILE current.next IS NOT NULL AND current.next.data ≠ value DO
            current ← current.next
        END WHILE
        IF current.next IS NOT NULL THEN
            current.next ← current.next.next
        END IF
    END FUNCTION

    FUNCTION Traverse()
        current ← head
        WHILE current IS NOT NULL DO
            PRINT current.data
            current ← current.next
        END WHILE
    END FUNCTION
END CLASS
```

---
##### 1.1.1.2.3 Doubly Linked List
A **Doubly Linked List** is a type of linked list where each node contains two pointers: one pointing to the next node and one pointing to the previous node. This allows traversal in both directions (forward and backward) and makes operations like deletion more efficient.

###### **Operations:**
- **Insertion at the beginning:** $O(1)$
- **Insertion at the end:** $O(1)$
- **Deletion:** $O(1)$ for known nodes
- **Search:** $O(n)$

###### **Applications:**
- **Browser History:** Doubly linked lists are used in applications like a web browser’s back and forward navigation.
- **Undo/Redo Operations:** Doubly linked lists are ideal for implementing undo/redo functionalities in software applications.

###### **Pseudocode:**
```plaintext
CLASS Node
    VARIABLE data
    VARIABLE next
    VARIABLE prev

    FUNCTION InitializeNode(value)
        data ← value
        next ← NULL
        prev ← NULL
    END FUNCTION
END CLASS

CLASS DoublyLinkedList
    VARIABLE head
    VARIABLE tail

    FUNCTION InitializeLinkedList()
        head ← NULL
        tail ← NULL
    END FUNCTION

    FUNCTION InsertAtBeginning(value)
        newNode ← Node(value)
        IF head IS NULL THEN
            head ← newNode
            tail ← newNode
        ELSE
            newNode.next ← head
            head.prev ← newNode
            head ← newNode
        END IF
    END FUNCTION

    FUNCTION InsertAtEnd(value)
        newNode ← Node(value)
        IF tail IS NULL THEN
            head ← newNode
            tail ← newNode
        ELSE
            tail.next ← newNode
            newNode.prev ← tail
            tail ← newNode
        END IF
    END FUNCTION

    FUNCTION DeleteNode(value)
        current ← head
        WHILE current IS NOT NULL AND current.data ≠ value DO
            current ← current.next
        END WHILE
        IF current IS NOT NULL THEN
            IF current.prev IS NOT NULL THEN
                current.prev.next ← current.next
            ELSE
                head ← current.next
            END IF
            IF current.next IS NOT NULL THEN
                current.next.prev ← current.prev
            ELSE
                tail ← current.prev
            END IF
        END IF
    END FUNCTION

    FUNCTION TraverseForward()
        current ← head
        WHILE current IS NOT NULL DO
            PRINT current.data
            current ← current.next
        END WHILE
    END FUNCTION

    FUNCTION TraverseBackward()
        current ← tail
        WHILE current IS NOT NULL DO
            PRINT current.data
            current ← current.prev
        END WHILE
    END FUNCTION
END CLASS
```

---
#### 1.1.1.3 Stacks
A **Stack** implemented using an array follows the Last In, First Out (LIFO) principle. This approach is straightforward and is often used when the maximum size of the stack is known beforehand. Using an array provides constant-time access to the top element and efficient push/pop operations.

##### **Operations:**
- **Push (Insertion at the top):** $O(1)$
- **Pop (Deletion from the top):** $O(1)$
- **Peek (Accessing the top element without removal):** $O(1)$

##### **Applications:**
- **Expression Evaluation:** Stacks are used in evaluating mathematical expressions, such as converting infix to postfix notation.
- **Backtracking:** Stacks are useful in algorithms that require exploring all possibilities, such as the depth-first search algorithm.

##### **Pseudocode:**
```plaintext
CLASS Stack
    VARIABLE elements
    VARIABLE top
    VARIABLE maxSize

    FUNCTION InitializeStack(maxSize)
        elements ← new array of size maxSize
        top ← -1
        this.maxSize ← maxSize
    END FUNCTION

    FUNCTION Push(value)
        IF top = maxSize - 1 THEN
            PRINT "Stack Overflow"
        ELSE
            top ← top + 1
            elements[top] ← value
        END IF
    END FUNCTION

    FUNCTION Pop()
        IF top = -1 THEN
            PRINT "Stack Underflow"
            RETURN NULL
        ELSE
            value ← elements[top]
            top ← top - 1
            RETURN value
        END IF
    END FUNCTION

    FUNCTION Peek()
        IF top = -1 THEN
            RETURN NULL
        ELSE
            RETURN elements[top]
        END IF
    END FUNCTION

    FUNCTION IsEmpty()
        RETURN top = -1
    END FUNCTION
END CLASS
```

---
#### 1.1.1.4 Queues
A **Queue** implemented using an array follows the First In, First Out (FIFO) principle. This method is efficient when the queue size is known and fixed. Arrays provide constant-time access for enqueue and dequeue operations when implemented properly.

##### **Operations:**
- **Enqueue (Insertion at the rear):** $O(1)$
- **Dequeue (Deletion from the front):** $O(1)$
- **Peek (Accessing the front element without removal):** $O(1)$

##### **Applications:**
- **Task Scheduling:** Queues are used in systems where tasks need to be processed in the order they arrive, such as in printer job scheduling or managing tasks in an operating system.

##### **Pseudocode:**
```plaintext
CLASS Queue
    VARIABLE elements
    VARIABLE front
    VARIABLE rear
    VARIABLE maxSize

    FUNCTION InitializeQueue(maxSize)
        elements ← new array of size maxSize
        front ← 0
        rear ← -1
        this.maxSize ← maxSize
    END FUNCTION

    FUNCTION Enqueue(value)
        IF rear = maxSize - 1 THEN
            PRINT "Queue Overflow"
        ELSE
            rear ← rear + 1
            elements[rear] ← value
        END IF
    END FUNCTION

    FUNCTION Dequeue()
        IF front > rear THEN
            PRINT "Queue Underflow"
            RETURN NULL
        ELSE
            value ← elements[front]
            front ← front + 1
            RETURN value
        END IF
    END FUNCTION

    FUNCTION Peek()
        IF front > rear THEN
            RETURN NULL
        ELSE
            RETURN elements[front]
        END IF
    END FUNCTION

    FUNCTION IsEmpty()
        RETURN front > rear
    END FUNCTION
END CLASS
```

---
### 1.1.2 Tree-Based Data Structures
#### 1.1.2.1 Heaps
A **Heap** is a specialized tree-based data structure that satisfies the heap property. It is commonly used to implement priority queues. A heap can be classified into two types:
- **Min Heap:** In a Min Heap, for any given node $i$, the value of the parent node is less than or equal to the value of the child nodes. The root node, therefore, contains the smallest value.
- **Max Heap:** In a Max Heap, for any given node $i$, the value of the parent node is greater than or equal to the value of the child nodes. The root node, therefore, contains the largest value.

##### **Operations:**
- **Insertion:** $O(\log n)$
- **Deletion (Extract-Min or Extract-Max):** $O(\log n)$
- **Peek (Access the minimum or maximum):** $O(1)$

##### **Applications:**
- **Priority Queue:** Heaps are often used to implement priority queues where the highest or lowest priority element is needed efficiently.
- **Heap Sort:** Heaps can be used in the Heap Sort algorithm, which is an efficient sorting algorithm with a time complexity of $O(n \log n)$.
- **Scheduling Algorithms:** Heaps are used in various scheduling algorithms to maintain the order of tasks or processes.
##### 1.1.2.1.1 Min Heap
###### **Pseudocode:**
```plaintext
CLASS MinHeap
    VARIABLE heap  # Array to store the heap elements
    VARIABLE size  # Number of elements in the heap

    FUNCTION InitializeHeap(capacity)
        heap ← new array of size capacity
        size ← 0
    END FUNCTION

    FUNCTION Parent(i)
        RETURN (i - 1) / 2
    END FUNCTION

    FUNCTION LeftChild(i)
        RETURN 2 * i + 1
    END FUNCTION

    FUNCTION RightChild(i)
        RETURN 2 * i + 2
    END FUNCTION

    FUNCTION Insert(value)
        IF size = length(heap) THEN
            PRINT "Heap Overflow"
            RETURN
        END IF

        size ← size + 1
        i ← size - 1
        heap[i] ← value

        # Fix the min heap property if it is violated
        WHILE i ≠ 0 AND heap[Parent(i)] > heap[i] DO
            SWAP heap[i] WITH heap[Parent(i)]
            i ← Parent(i)
        END WHILE
    END FUNCTION

    FUNCTION MinHeapify(i)
        left ← LeftChild(i)
        right ← RightChild(i)
        smallest ← i

        IF left < size AND heap[left] < heap[smallest] THEN
            smallest ← left
        END IF

        IF right < size AND heap[right] < heap[smallest] THEN
            smallest ← right
        END IF

        IF smallest ≠ i THEN
            SWAP heap[i] WITH heap[smallest]
            MinHeapify(smallest)
        END IF
    END FUNCTION

    FUNCTION ExtractMin()
        IF size ≤ 0 THEN
            RETURN NULL
        ELSE IF size = 1 THEN
            size ← size - 1
            RETURN heap[0]
        END IF

        # Store the minimum value and remove it from the heap
        root ← heap[0]
        heap[0] ← heap[size-1]
        size ← size - 1
        MinHeapify(0)

        RETURN root
    END FUNCTION

    FUNCTION GetMin()
        RETURN heap[0]
    END FUNCTION
END CLASS
```

##### 1.1.2.1.2 Max Heap
###### **Pseudocode:**
```plaintext
CLASS MaxHeap
    VARIABLE heap  # Array to store the heap elements
    VARIABLE size  # Number of elements in the heap

    FUNCTION InitializeHeap(capacity)
        heap ← new array of size capacity
        size ← 0
    END FUNCTION

    FUNCTION Parent(i)
        RETURN (i - 1) / 2
    END FUNCTION

    FUNCTION LeftChild(i)
        RETURN 2 * i + 1
    END FUNCTION

    FUNCTION RightChild(i)
        RETURN 2 * i + 2
    END FUNCTION

    FUNCTION Insert(value)
        IF size = length(heap) THEN
            PRINT "Heap Overflow"
            RETURN
        END IF

        size ← size + 1
        i ← size - 1
        heap[i] ← value

        # Fix the max heap property if it is violated
        WHILE i ≠ 0 AND heap[Parent(i)] < heap[i] DO
            SWAP heap[i] WITH heap[Parent(i)]
            i ← Parent(i)
        END WHILE
    END FUNCTION

    FUNCTION MaxHeapify(i)
        left ← LeftChild(i)
        right ← RightChild(i)
        largest ← i

        IF left < size AND heap[left] > heap[largest] THEN
            largest ← left
        END IF

        IF right < size AND heap[right] > heap[largest] THEN
            largest ← right
        END IF

        IF largest ≠ i THEN
            SWAP heap[i] WITH heap[largest]
            MaxHeapify(largest)
        END IF
    END FUNCTION

    FUNCTION ExtractMax()
        IF size ≤ 0 THEN
            RETURN NULL
        ELSE IF size = 1 THEN
            size ← size - 1
            RETURN heap[0]
        END IF

        # Store the maximum value and remove it from the heap
        root ← heap[0]
        heap[0] ← heap[size-1]
        size ← size - 1
        MaxHeapify(0)

        RETURN root
    END FUNCTION

    FUNCTION GetMax()
        RETURN heap[0]
    END FUNCTION
END CLASS
```

## 1.2 Searching Algorithms
### 1.2.1 Array Based
#### 1.2.1.1 Binary Search
Binary Search is an efficient algorithm for finding a target element in a sorted array or list. The algorithm repeatedly divides the search interval in half. If the value of the search key is less than the item in the middle of the interval, the algorithm narrows the interval to the lower half. Otherwise, it narrows it to the upper half. This process continues until the target value is found or the interval is empty.

##### Time- & Space complexity
- **Time complexity:** $O(\log n)$
- **Space complexity:** $O(1)$ for the iterative version, $O(\log n)$ for the recursive version due to the call stack.

Where $n$ is the number of elements in the array or list.

##### Optimality:
Binary Search guarantees an optimal solution in terms of time efficiency for searching in a sorted array, making it much faster than [[#1.2.1.2 Linear Search|linear search]] for large datasets. However, the array or list must be sorted for Binary Search to work correctly.

##### Example:
- **Finding an Element in a Sorted Array:** Binary Search can be used to quickly locate a specific value in a large, sorted array by eliminating half of the elements from consideration in each step.

##### Pseudocode:

```plaintext
FUNCTION BinarySearch(array, target)
    low ← 0
    high ← length(array) - 1
    
    WHILE low ≤ high DO
        mid ← (low + high) / 2
        
        IF array[mid] == target THEN
            RETURN mid
        ELSE IF array[mid] < target THEN
            low ← mid + 1
        ELSE
            high ← mid - 1
        END IF
    END WHILE
    
    RETURN failure
END FUNCTION
```

---
#### 1.2.1.2 Exponential Search
Exponential Search is an algorithm used to find the position of a target value within a sorted array. It combines the power of binary search with an exponential increase in search indices. The algorithm starts with a bound size of 1 and doubles it until the bound exceeds the target value or the end of the array is reached. Once the bound is found, Binary Search is performed within this range.

##### Time- & Space complexity
- **Time complexity:** $O(\log n)$
- **Space complexity:** $O(1)$

Where $n$ is the number of elements in the array or list.

##### Optimality:
Exponential Search is particularly effective when the target element is near the beginning of a sorted array. It is optimal for unbounded or infinite lists, where the size of the list is unknown, as it efficiently reduces the search space.

##### Example:
- **Searching in a Large, Sorted Array:** Exponential Search can quickly locate the position of a target element by first finding an appropriate range using exponential jumps and then applying Binary Search within that range.

##### Pseudocode:
```plaintext
FUNCTION ExponentialSearch(array, target)
    IF array[0] == target THEN
        RETURN 0
    END IF

    index ← 1
    WHILE index < length(array) AND array[index] ≤ target DO
        index = index * 2
    END WHILE

    RETURN BinarySearch(array, target, index / 2, min(index, length(array)-1))
END FUNCTION

FUNCTION BinarySearch(array, target, low, high)
    WHILE low ≤ high DO
        mid ← (low + high) / 2
        
        IF array[mid] == target THEN
            RETURN mid
        ELSE IF array[mid] < target THEN
            low ← mid + 1
        ELSE
            high ← mid - 1
        END IF
    END WHILE
    
    RETURN failure
END FUNCTION
```

---
#### 1.2.1.3 Interpolation Search
Interpolation Search is an algorithm used to find the position of a target value within a sorted, uniformly distributed array. The algorithm improves upon [[#1.2.1.1 Binary Search|binary search]] by calculating the likely position of the target based on the values at the bounds and the target value itself. It works similarly to how humans search for a value in a telephone book by estimating the position of the name they are looking for.

##### Time- & Space complexity
- **Time complexity: $O(\log \log n)$
- **Space complexity:** $O(1)$

Where $n$ is the number of elements in the array or list.

##### Optimality:

Interpolation Search is highly efficient for large, uniformly distributed datasets. It outperforms binary search in such scenarios due to its ability to estimate the likely position of the target value. However, it is less effective for non-uniformly distributed datasets, where it can degrade to linear search performance.

##### Example:

- **Searching in a Large, Uniformly Distributed Array:** Interpolation Search can be used to quickly locate the position of a target element in a large, sorted array where the elements are uniformly distributed, such as searching for a specific key in a large, ordered list of numerical values.

##### Pseudocode:

```plaintext
FUNCTION InterpolationSearch(array, target)
    low ← 0
    high ← length(array) - 1

    WHILE low ≤ high AND target ≥ array[low] AND target ≤ array[high] DO
        pos ← low + ((target - array[low]) * (high - low)) / (array[high] - array[low])

        IF array[pos] == target THEN
            RETURN pos
        ELSE IF array[pos] < target THEN
            low ← pos + 1
        ELSE
            high ← pos - 1
        END IF
    END WHILE

    RETURN failure
END FUNCTION
```

---
#### 1.2.1.4 Jump Search
Jump Search is an algorithm used to find a target value in a sorted array. The algorithm works by jumping ahead by fixed steps in the array rather than checking each element sequentially, like in linear search. Once a range where the target could be is identified, the algorithm performs a [[#1.2.1.2 Linear Search|linear search]] within that range.

##### Time- & Space complexity
- **Time complexity:** $O(\sqrt{n})$
- **Space complexity:** $O(1)$

Where $n$ is the number of elements in the array or list.

##### Optimality:
Jump Search is efficient for searching in large sorted arrays, particularly when the array is too large for binary search to be efficient due to memory access patterns. It balances the simplicity of [[#1.2.1.2 Linear Search|linear search]] with the efficiency of reducing the search interval in each step.

##### Example:
- **Searching in a Sorted Array:** Jump Search can be used to quickly locate the position of a target element by jumping ahead by a fixed number of steps (usually $\sqrt{n}$), thereby reducing the number of elements that need to be checked linearly within a smaller range.

##### Pseudocode:

```plaintext
FUNCTION JumpSearch(array, target)
    n ← length(array)
    step ← floor(sqrt(n))
    prev ← 0

    WHILE array[min(step, n) - 1] < target DO
        prev ← step
        step ← step + floor(sqrt(n))
        IF prev ≥ n THEN
            RETURN failure
        END IF
    END WHILE

    FOR i FROM prev TO min(step, n) - 1 DO
        IF array[i] == target THEN
            RETURN i
        END IF
    END FOR

    RETURN failure
END FUNCTION
```

---
#### 1.2.1.5 Linear Search
Linear search is a basic search algorithm used to find a specific element in an array or list. The algorithm sequentially checks each element, starting from the first, until it finds the target element or reaches the end of the array.

##### Time- & Space complexity

- **Time complexity:** $O(n)$
- **Space complexity:** $O(1)$ 

Where $n$ is the number of elements in the array or list.

##### Optimality:
Linear search does not guarantee an optimal solution in terms of time efficiency, especially when compared to more advanced search algorithms like binary search. However, it is straightforward and optimal in scenarios where the array or list is unsorted or very small.

##### Example:
- **Unsorted Array Search**: Linear search can be used to find a specific value in an unsorted array by checking each element one by one.

##### Pseudocode:

```plaintext
FUNCTION LinearSearch(array, target)
    FOR each element IN array DO
        IF element == target THEN
            RETURN index of element
        END IF
    END FOR
    RETURN failure
END FUNCTION
```

---
#### 1.2.1.6 Ternary Search
Ternary Search is a divide-and-conquer search algorithm used to find the maximum or minimum of a unimodal function, or it can be used to find a target value in a sorted array. The algorithm works by dividing the search space into three parts, then determining in which part the target or optimal value might lie, and recursively searching that part.

##### Time- & Space complexity
- **Time complexity:** $O(\log_3 n)$
- **Space complexity:** $O(1)$ 

Where $n$ is the number of elements in the array or list.

##### Optimality:
Ternary Search is efficient for searching in large, sorted arrays or optimizing unimodal functions. It is similar to [[#1.2.1.1 Binary Search|Binary Search]] but divides the array into three parts instead of two, which can be advantageous in certain types of search or optimization problems.

##### Example:
- **Finding an Element in a Sorted Array:** Ternary Search can be used to find a specific value in a large, sorted array by dividing the array into three sections, which reduces the search space more rapidly than binary search in some scenarios.

##### Pseudocode:

```plaintext
FUNCTION TernarySearch(array, target, low, high)
    IF high < low THEN
        RETURN failure
    END IF

    mid1 ← low + (high - low) / 3
    mid2 ← high - (high - low) / 3

    IF array[mid1] == target THEN
        RETURN mid1
    ELSE IF array[mid2] == target THEN
        RETURN mid2
    ELSE IF target < array[mid1] THEN
        RETURN TernarySearch(array, target, low, mid1 - 1)
    ELSE IF target > array[mid2] THEN
        RETURN TernarySearch(array, target, mid2 + 1, high)
    ELSE
        RETURN TernarySearch(array, target, mid1 + 1, mid2 - 1)
    END IF
END FUNCTION
```

 
### 1.2.2 Graph Based 
#### 1.2.1.1 A* Search
A* Search is an informed search algorithm that combines the [[#2.2.4 Path Cost|path cost]] from the start node to the current node $g(n)$ with a heuristic estimate of the cost from the current [[#2.1.4 Node|node]] to the goal $h(n)$. The algorithm expands the [[#2.1.4 Node|node]] with the lowest estimated total cost $f(n) = g(n) + h(n)$, ensuring that the first solution found is the optimal one if the [[#Heuristic Function|heuristic function]] is admissible and consistent.
##### Time- & Space complexity
- **Time complexity:** $O(|V|+log(|E|))$ 
- **Space complexity:** $O(|V|)$

Where $V$ are the vertices and $E$ the edges 
##### Optimality:
A* Search guarantees an optimal solution if the [[#Heuristic Function|heuristic function]] $h(n)$ is:
- **Admissible**: The heuristic never overestimates the true cost to reach the goal.
- **Consistent (Monotonicity)**: For every [[#2.1.4 Node|node]] $n$ and every neighbour $n'$ g the estimated cost of reaching the goal from $n$ is no greater than the cost of getting to $n'$ plus the estimated cost from $n'$ to the goal: 
  $$ h(n) \leq c(n, n') + h(n') $$
**Note:** In some implementations, actions leading to neighbors can be explicitly represented. If so, the cost function $c(n,n′)$ can include the cost of the action taken to reach $n′$ from $n$.
##### Example:
- **Pathfinding**: A* Search might be used to find the shortest path in a grid by considering both the actual distance travelled so far and an estimate of the remaining distance to the goal.
##### Pseudocode:

```plaintext
FUNCTION AStar(initial_node, goal_test, heuristic)
    frontier ← NEW PriorityQueue()
    frontier.AddNode(initial_node, 0)  # Start with the initial node, with 0 cost
    explored ← NEW SET()
    
    WHILE NOT frontier.IsEmpty() DO
        current_node ← frontier.RemoveNode()
        
        IF GoalTest(current_node) THEN
            RETURN ReconstructPath(current_node)
        END IF
        
        ADD current_node TO explored
        
        FOR each (neighbor, cost) IN current_node.neighbors DO
            path_cost ← current_node.path_cost + cost  # Cost to reach neighbor
            total_cost ← path_cost + heuristic(neighbor)  # Estimated total cost
            
            IF neighbor NOT IN explored OR path_cost < neighbor.path_cost THEN
                neighbor.parent ← current_node  # Record the best path
                neighbor.path_cost ← path_cost  # Update the cost to reach neighbor
                
                IF neighbor NOT IN frontier THEN
                    frontier.AddNode(neighbor, total_cost)
                ELSE
                    # Update the node with a new cost if it's already in the
                    # frontier  
                    frontier.UpdateNode(neighbor, total_cost)  
                END IF
            END IF
        END FOR
    END WHILE
    RETURN failure  # No valid path was found
```

#### 1.2.1.2 Bellman-Ford Algorithm
The Bellman-Ford Algorithm is another shortest path algorithm that, unlike [[#1.2.1.5 Dijkstra's Algorithm|Dijkstra's]] Algorithm, can handle graphs with negative edge weights. It iteratively relaxes all the edges, gradually finding the shortest paths from the start node to all other nodes. If a graph contains a negative weight cycle, the algorithm can detect it and report its presence.

##### Time- & Space complexity
- **Time complexity:** $O(|V| \cdot |E|)$
- **Space complexity:** $O(|V|)$

Where $V$ represents the vertices and $E$ the edges in the graph.

##### Optimality:
Bellman-Ford guarantees finding the shortest path if no negative weight cycles exist. If a negative weight cycle exists, the algorithm can identify this, indicating that no solution exists for the shortest path due to the cycle.

##### Example:
- **Currency Arbitrage:** Bellman-Ford can be used to detect arbitrage opportunities in currency exchange rates, where the presence of a negative weight cycle represents a series of trades that can lead to a profit.

##### Pseudocode:
```plaintext
FUNCTION BellmanFord(initial_node, graph)
    INITIALIZE all nodes with infinite cost, except the initial_node with 0
    SET initial_node.cost TO 0
    
	# Repeat |V| - 1 times, where |V| is the number of vertices
    FOR i FROM 1 TO |V| - 1 DO  
        FOR each edge (u, v) WITH weight w IN graph DO
            IF u.cost + w < v.cost THEN
                v.cost ← u.cost + w
                v.parent ← u
            END IF
        END FOR
    END FOR
    
    # Check for negative weight cycles
    FOR each edge (u, v) WITH weight w IN graph DO
        IF u.cost + w < v.cost THEN
            PRINT "Graph contains a negative weight cycle"
            RETURN failure
        END IF
    END FOR
    
    # If no negative weight cycle found, all shortest paths are determined
    RETURN success  
END FUNCTION
```
#### 1.2.1.3 Breadth-First Search (BFS)
Breadth-First Search (BFS) is an uninformed search algorithm that explores all [[#Node|nodes]] at the present depth level before moving on to [[#Node|nodes]] at the next depth level. It systematically expands the shallowest unexpanded [[#Node|nodes]] first, ensuring that the first solution found is the shortest path in terms of the number of steps if all actions have equal cost.

##### Time- & Space complexity
- **Time complexity:** $O(|V|+|E|)$
- **Space complexity:** $O(|V|)$

Where $V$ are the vertices and $E$ the edges
##### Optimality:
BFS guarantees an optimal solution if the [[#2.2.4 Path Cost|path cost]] is a non-decreasing function of the depth of the [[#2.1.4 Node|node]], meaning all steps have the same cost (non-weighted graph).
##### Example:
- **Maze-Solving**: In a grid-based maze, BFS can be used to find the shortest path from the start to the goal by exploring all possible paths one step at a time, ensuring that the first solution found is the shortest in terms of the number of steps.

##### Pseudocode:

```plaintext
FUNCTION BFS(initial_node, goal_test)
    frontier ← NEW Frontier()  # Typically a queue for BFS
    frontier.AddNode(initial_node)
    explored ← NEW SET()
    
    WHILE NOT frontier.IsEmpty() DO
        current_node ← frontier.RemoveNode()
        
        IF GoalTest(current_node) THEN
            RETURN Solution(current_node)
        END IF
        
        ADD current_node TO explored
        
        FOR each neighbor IN current_node.neighbors DO
            IF neighbor NOT IN explored AND neighbor NOT IN frontier THEN
                neighbor.parent ← current_node  # Record the path to the neighbor
                frontier.AddNode(neighbor)
            END IF
        END FOR
    END WHILE
    
    RETURN failure
END FUNCTION
```


#### 1.2.1.4 Depth-First Search (DFS)
Depth-First Search (DFS) is an uninformed search algorithm that explores as far down a branch as possible before backtracking. It systematically expands the deepest unexpanded [[#Node|nodes]] first, using a stack to manage the frontier.

##### Time- & Space complexity
- **Time complexity:** $O(|V|+|E|)$ 
- **Space complexity:** $O(|V|)$

Where $V$ are the vertices and $E$ the edges 

##### Optimality:
DFS does not guarantee an optimal solution since it can get trapped exploring deep paths that are not optimal. It is also not complete on infinite-depth spaces without additional mechanisms like depth limits.

##### Example:
- **Maze-Solving**: In a grid-based maze, DFS would follow a path from the start as far as it can go until it hits a dead-end or reaches the goal. If it hits a dead-end, it backtracks and explores alternative paths.

##### Pseudocode:

```plaintext
FUNCTION DFS(initial_node, goal_test)
    frontier ← NEW Stack()  # A stack is used to implement DFS
    frontier.Push(initial_node)
    explored ← NEW SET()
    
    WHILE NOT frontier.IsEmpty() DO
        current_node ← frontier.Pop()
        
        IF GoalTest(current_node) THEN
            RETURN Solution(current_node)
        END IF
        
        ADD current_node TO explored
        
        FOR each neighbor IN current_node.neighbors DO
            IF neighbor NOT IN explored AND neighbor NOT IN frontier THEN
                neighbor.parent ← current_node  # Record the path to the neighbor
                frontier.Push(neighbor)
            END IF
        END FOR
    END WHILE
    
    RETURN failure
END FUNCTION
```


#### 1.2.1.5 Dijkstra's Algorithm
Dijkstra's Algorithm is an uninformed search algorithm used to find the shortest path from a starting node to all other nodes in a graph with non-negative edge weights. Unlike A* Search, which uses a heuristic to guide its search, Dijkstra's Algorithm relies solely on the path cost to ensure that the shortest path to each node is found. It is particularly well-suited for graphs where the goal is to find the shortest paths to all nodes rather than just one.

##### Time- & Space complexity
- **Time complexity:** $O(|V| \log(|V|) + |E| \log(|V|))$ with a priority queue, or $O(|V|^2)$ with a simple array
- **Space complexity:** $O(|V| + |E|)$

Where $V$ represents the vertices and $E$ the edges in the graph.

##### Optimality:
Dijkstra's Algorithm guarantees an optimal solution in terms of the shortest path from the start node to any other node in the graph, provided all edge weights are non-negative.

##### Example:
- **Network Routing:** Dijkstra's Algorithm can be used to determine the shortest path for routing data packets between nodes in a network.

##### Pseudocode:
```plaintext
FUNCTION Dijkstra(initial_node)
    frontier ← NEW PriorityQueue()
    frontier.AddNode(initial_node, 0)  # Start with the initial node, with 0 path cost
    explored ← NEW SET()
    
    WHILE NOT frontier.IsEmpty() DO
        current_node ← frontier.RemoveNode()
        
        IF current_node NOT IN explored THEN
            ADD current_node TO explored
            
            FOR each (neighbor, edge_cost) IN GetNeighbors(current_node) DO
                new_cost ← current_node.cost + edge_cost
                
                IF neighbor NOT IN explored THEN
                    IF neighbor NOT IN frontier OR new_cost < neighbor.cost THEN
                        neighbor.cost ← new_cost
                        neighbor.parent ← current_node
                        
                        IF neighbor IN frontier THEN
                            frontier.UpdatePriority(neighbor, new_cost)
                        ELSE
                            frontier.AddNode(neighbor, new_cost)
                        END IF
                    END IF
                END IF
            END FOR
        END IF
    END WHILE
    
    RETURN failure  # If all nodes have been explored and no specific goal was reached
END FUNCTION
```

#### 1.2.1.6 Floyd-Warshall Algorithm
The Floyd-Warshall Algorithm is an all-pairs shortest path algorithm, meaning it computes the shortest paths between all pairs of nodes in a graph. It uses dynamic programming to iteratively improve the estimate of the shortest path between each pair of nodes by considering each possible intermediate node.
##### Time- & Space complexity
- **Time complexity:** $O(|V|^3)$
- **Space complexity:** $O(|V|^2)$

Where $V$ represents the vertices in the graph.
##### Optimality:
Floyd-Warshall guarantees finding the shortest path between all pairs of nodes in the graph, even if the graph contains negative edge weights, provided there are no negative weight cycles.
##### Example:
- **Network Analysis:** Floyd-Warshall can be used to compute the shortest paths for routing information between all nodes in a network or for analyzing all-pairs shortest paths in social networks.
##### Pseudocode:
```plaintext
FUNCTION FloydWarshall(graph)
    DISTANCE ← 2D array of size |V| x |V| initialized to infinity
    FOR each node v IN graph DO
        DISTANCE[v][v] ← 0
    END FOR
    
    FOR each edge (u, v) WITH weight w IN graph DO
        DISTANCE[u][v] ← w
    END FOR
    
    FOR k FROM 1 TO |V| DO  # Consider each node as an intermediate node
        FOR i FROM 1 TO |V| DO
            FOR j FROM 1 TO |V| DO
                IF DISTANCE[i][j] > DISTANCE[i][k] + DISTANCE[k][j] THEN
                    DISTANCE[i][j] ← DISTANCE[i][k] + DISTANCE[k][j]
                END IF
            END FOR
        END FOR
    END FOR
    
    RETURN DISTANCE  # This contains the shortest paths between all pairs of nodes
END FUNCTION
```
#### 1.2.1.7 Greedy Best-First Search (GBFS)
Greedy Best-First Search (GBFS) is an informed search algorithm that prioritizes the expansion of [[#Node|nodes]] that appear closest to the goal according to a heuristic function $h(n)$. It selects [[#Node|nodes]] based on their estimated proximity to the goal, but it does not guarantee finding the optimal solution, as it may overlook longer, but ultimately shorter, paths.

##### Time- & Space complexity
- **Time complexity:** Depends on the heuristic and the problem, typically $O(|V|)$ in the worst case.
- **Space complexity:** $O(|V|)$

Where $V$ are the vertices.

##### Optimality:
GBFS does not guarantee an optimal solution because it only considers the heuristic value, which might lead it down a non-optimal path if a [[#2.1.4 Node|node]] seems closer to the goal.

##### Example:
- **Pathfinding**: In a navigation problem, GBFS might use the straight-line distance (Euclidean distance) to the goal as its heuristic. The algorithm will always move towards the goal based on this distance, even if it doesn't result in the shortest path overall.

##### Pseudocode:

```plaintext
FUNCTION GreedyBFS(initial_node, goal_test, heuristic)
    frontier ← NEW PriorityQueue()
    frontier.AddNode(initial_node, heuristic(initial_node))
    explored ← NEW SET()
    
    WHILE NOT frontier.IsEmpty() DO
        current_node ← frontier.RemoveNode()
        
        IF GoalTest(current_node) THEN
            RETURN Solution(current_node)
        END IF
        
        ADD current_node TO explored
        
        FOR each neighbor IN current_node.neighbors DO
            heuristic_cost ← heuristic(neighbor)
            
            IF neighbor NOT IN explored AND neighbor NOT IN frontier THEN
                neighbor.parent ← current_node  # Record the path to the neighbor
                frontier.AddNode(neighbor, heuristic_cost)
            END IF
        END FOR
    END WHILE
    
    RETURN failure
END FUNCTION
```
#### 1.2.1.8 Uniform-Cost Search (UCS)
Uniform-Cost Search (UCS) is an uninformed search algorithm that expands the least-cost [[#2.1.4 Node|node]] first, ensuring that the path to the goal is the lowest-cost one in terms of the cumulative cost of actions. It uses a priority queue to manage the frontier, always selecting the [[#2.1.4 Node|node]] with the smallest path cost for expansion.

##### Time- & Space complexity
- **Time complexity:** $O(|V|+|E|)$
- **Space complexity:** $O(|V|)$

Where $V$ are the vertices and $E$ the edges.

##### Optimality:
UCS guarantees an optimal solution as it always expands the least-cost path first. This makes it particularly useful for weighted graphs where the cost of actions varies.

##### Example:
- **Route Planning**: In a network of roads with varying travel times, UCS can be used to find the shortest time path from one location to another by considering the cumulative travel cost.

##### Pseudocode:
```plaintext
FUNCTION UCS(initial_node, goal_test)
    frontier ← NEW PriorityQueue()
    frontier.AddNode(initial_node, 0)  # Start with the initial node, with 0 path cost
    explored ← NEW SET()
    
    WHILE NOT frontier.IsEmpty() DO
        current_node ← frontier.RemoveNode()
        
        IF GoalTest(current_node) THEN
            RETURN Solution(current_node)
        END IF
        
        ADD current_node TO explored
        
        FOR each (neighbor, step_cost) IN current_node.neighbors DO
            path_cost ← current_node.path_cost + step_cost
            
            IF neighbor NOT IN explored OR path_cost < neighbor.path_cost THEN
                neighbor.parent ← current_node 
                neighbor.path_cost ← path_cost
                
                IF neighbor NOT IN frontier THEN
                    frontier.AddNode(neighbor, path_cost)
                ELSE
                    frontier.UpdatePriority(neighbor, path_cost)  
                END IF
            END IF
        END FOR
    END WHILE
    
    RETURN failure
END FUNCTION
```

### 1.2.3 Decision-Making Algorithms
#### 1.2.3.1 Alpha-Beta Pruning
**Alpha-Beta Pruning** is an optimization technique for the [[#1.2.3.3 Minimax Algorithm|Minimax algorithm]] that reduces the number of nodes evaluated in the game tree. It accomplishes this by "pruning" branches that cannot possibly influence the final decision, thus improving the efficiency of the algorithm.

Although Alpha-Beta Pruning is most commonly associated with the Minimax algorithm, it is **not limited to Minimax**. The principles of Alpha-Beta Pruning can be applied to other algorithms that involve searching through a tree structure with adversarial components, including:

- **Expectiminimax Algorithm**: Used in games with elements of chance, such as backgammon, where the algorithm must account for both the player's decisions and random events.
- **Branch and Bound Algorithms**: Employed in optimization problems, where Alpha-Beta-like pruning techniques can be used to discard suboptimal branches in the search space.
- **Monte Carlo Tree Search (MCTS)**: Although MCTS typically uses more statistical and heuristic-based methods, concepts similar to Alpha-Beta Pruning can be adapted to prune less promising branches, thereby enhancing the efficiency of the search.

Alpha-Beta Pruning works by maintaining two values, **alpha** and **beta**:
- **Alpha** represents the best value that the maximizing player can guarantee.
- **Beta** represents the best value that the minimizing player can guarantee.

During the traversal of the game tree, if at any point the current node's evaluation falls outside the range set by alpha and beta, the search can be stopped along that branch because it cannot affect the final decision.

This pruning significantly reduces the time complexity of the Minimax algorithm, especially in deep game trees, as it prevents the algorithm from exploring nodes that will not be selected.

When the search is depth-limited, you can combine Alpha-Beta Pruning with an [[#1.2.3.2 Evaluation Function (for Depth-Limited Search)|evaluation function]] to estimate the utility of non-terminal states.
##### Pruning Logic:
- **Beta Cutoff**: If the value of a node being evaluated by the maximizing player is greater than or equal to the current value of **beta** (the best score that the minimizing player can achieve), then the minimizing player would never allow this path to be chosen. Therefore, there's no need to explore further down this branch, and it gets pruned. This is called a **beta cutoff**.
    
- **Alpha Cutoff**: Conversely, if the value of a node being evaluated by the minimizing player is less than or equal to the current value of **alpha** (the best score that the maximizing player can guarantee), then the maximizing player would never allow this path to be chosen. Therefore, this branch can be pruned as well, which is called an **alpha cutoff**.
##### Pseudocode: 
```plaintext
FUNCTION AlphaBeta(state, depth, α, β, maximizingPlayer) -> INTEGER
    IF depth = 0 OR TerminalState(state) THEN
        RETURN EvaluationFunction(state)
    END IF
    IF maximizingPlayer THEN
        maxEval ← -∞
        FOR each action IN Actions(state) DO
            eval ← AlphaBeta(Result(state, action), depth - 1, α, β, FALSE)
            maxEval ← MAX(maxEval, eval)
            α ← MAX(α, eval) 
            IF β ≤ α THEN # Beta pruning
                BREAK
            END IF
        END FOR
        RETURN maxEval
    ELSE
        minEval ← ∞
        FOR each action IN Actions(state) DO
            eval ← AlphaBeta(Result(state, action), depth - 1, α, β, TRUE)
            minEval ← MIN(minEval, eval)
            β ← MIN(β, eval)
            IF β ≤ α THEN # Alpha pruning
                BREAK
            END IF
        END FOR
        RETURN minEval
    END IF
END FUNCTION
```

---
#### 1.2.3.2 Evaluation Function (for Depth-Limited Search)
An **Evaluation Function** is used in depth-limited versions of the [[#1.2.3.3 Minimax Algorithm|Minimax algorithm]] to estimate the utility of a game state when the search is terminated before reaching a terminal state due to reaching a specified depth limit. However, it is important to note that **evaluation functions are not exclusive to Minimax**. They are a general tool used in various algorithms and scenarios where a complete search is impractical or impossible, and an approximation of the utility of non-terminal states is required.

In addition to their use in Minimax, evaluation functions are also applied in:

- **Monte Carlo Tree Search (MCTS)**: In MCTS, evaluation functions can be used to guide the exploration of the tree by estimating the value of non-terminal nodes, especially in the rollout phase or when dealing with large search spaces.
- **Expectiminimax**: In games involving chance, like backgammon, evaluation functions are used to estimate the utility of states where exact outcomes are uncertain due to randomness.
- **Heuristic Search Algorithms**: In various heuristic-based searches, evaluation functions play a critical role in estimating the "goodness" of nodes when the search is truncated or when exploring vast search spaces.

This function is crucial for guiding the search process when it is not feasible to evaluate every possible outcome fully. The evaluation function assigns a heuristic value to non-terminal game states, effectively simulating the expected utility of continuing from that state. In games like chess, an evaluation function might consider factors such as material count, piece mobility, and control of the board.

When used alongside [[#1.2.3.1 Alpha-Beta Pruning|Alpha-Beta Pruning]], the evaluation function enables more efficient searches by allowing the algorithm to make informed decisions without needing to explore every possible move to its conclusion.

##### Example:
- **Chess**: A common evaluation function in chess assigns point values to different pieces (e.g., pawns, knights, bishops) and also considers factors like board control and piece development.

##### Pseudocode:
In the context of a depth-limited Minimax search, the evaluation function is invoked when the search reaches its depth limit or encounters a terminal state:

```plaintext
FUNCTION Minimax(state, depth, maximizingPlayer) -> INTEGER
    IF depth = 0 OR TerminalState(state) THEN
        RETURN EvaluationFunction(state)
    END IF
    IF maximizingPlayer THEN
        maxEval ← -∞
        FOR each action IN Actions(state) DO
            eval ← Minimax(Result(state, action), depth - 1, FALSE)
            maxEval ← MAX(maxEval, eval)
        END FOR
        RETURN maxEval
    ELSE
        minEval ← ∞
        FOR each action IN Actions(state) DO
            eval ← Minimax(Result(state, action), depth - 1, TRUE)
            minEval ← MIN(minEval, eval)
        END FOR
        RETURN minEval
    END IF
END FUNCTION
```

---
#### 1.2.3.3 Minimax Algorithm
The Minimax algorithm is a recursive decision-making algorithm used for minimizing the possible loss for a worst-case scenario. In a two-player game, it is used to find the best move by assuming that the opponent will also play optimally.

##### Key Points:
1. **Decision Tree**: Minimax operates on a decision tree, where each node represents a possible game state.
2. **Maximizing Player**: The player who attempts to maximize the utility value (e.g., trying to win the game). In a game like chess, this might represent one player, say "Player A."
3. **Minimizing Player**: The opponent who attempts to minimize the utility value, effectively countering the maximizing player's strategy. In chess, this would be "Player B."
4. **Game Tree**: A tree structure where each node represents a possible game state, and each branch represents a possible move. The root node is the current game state, and the leaves are the terminal states (end of the game).
5. **Utility Function**: A function that assigns a numerical value to a terminal state. This value represents the desirability of that state for the maximizing player. For example, in a chess game:
    - A positive value could represent a win for the maximizing player.
    - A negative value could represent a loss.
    - Zero could represent a draw.
3. **Recursive Nature**: The algorithm is inherently recursive, breaking down the decision-making process into smaller subproblems.

##### Time- & Space Complexity:
- **Time Complexity**: $O(b^m)$, where $b$ is the branching factor (average number of legal moves per state) and $m$ is the maximum depth of the tree.
- **Space Complexity**: $O(m)$ for depth-limited minimax with recursion, where $m$ is the depth of the tree.

##### Optimality:
Minimax guarantees an optimal solution assuming both players are playing optimally. However, the time complexity can be high due to the exponential number of game states.

##### Example:
- **Game Strategy**: In a game like tic-tac-toe, the Minimax algorithm can be used to determine the optimal move that guarantees a win or a draw, assuming the opponent also plays optimally.

##### Pseudocode with nodes:
```plaintext
FUNCTION Minimax(node, depth, maximizingPlayer)
    IF depth == 0 OR node is a terminal node THEN
        RETURN the heuristic value of node
    END IF

    IF maximizingPlayer THEN
        maxEval ← -∞
        FOR each child of node DO
            eval ← Minimax(child, depth - 1, FALSE)
            maxEval ← max(maxEval, eval)
        END FOR
        RETURN maxEval
    ELSE
        minEval ← ∞
        FOR each child of node DO
            eval ← Minimax(child, depth - 1, TRUE)
            minEval ← min(minEval, eval)
        END FOR
        RETURN minEval
    END IF
END FUNCTION
```

You can also present the algorithm in an alternative format, which includes handling actions and results:

```plaintext
FUNCTION Minimax(state, depth, maximizingPlayer) -> INTEGER
    IF depth = 0 OR TerminalState(state) THEN
        RETURN Utility(state)
    END IF
    IF maximizingPlayer THEN
        maxEval ← -∞
        FOR each action IN Actions(state) DO
            eval ← Minimax(Result(state, action), depth - 1, FALSE)
            maxEval ← MAX(maxEval, eval)
        END FOR
        RETURN maxEval
    ELSE
        minEval ← ∞
        FOR each action IN Actions(state) DO
            eval ← Minimax(Result(state, action), depth - 1, TRUE)
            minEval ← MIN(minEval, eval)
        END FOR
        RETURN minEval
    END IF
END FUNCTION
```

##### Applications:
- **Game Theory**: Used to make optimal decisions in competitive environments like chess, checkers, and tic-tac-toe.
- **Artificial Intelligence**: Forms the basis for AI agents that need to make decisions in adversarial environments.
## 1.3 General Concepts
### 1.3.1 Heuristic Functions
A heuristic function, denoted as $h(n)$, estimates the cost from the current [[#2.1.4 Node|node]] $n$ to the [[#2.1.7 State Goal State / Final State|goal]]. The effectiveness of an [[#2.3.2 Informed Search|informed search]] algorithm heavily depends on the quality of this heuristic. 
#### Admissibility and Consistency 
- **Admissibility**: A heuristic is admissible if it never overestimates the actual cost to reach the goal. This ensures that the solution found by algorithms like [[#1.2.1.1 A* Search|A*]] is optimal. 
  Formally:  for all nodes $n$, $$h(n) \leq h^*(n)$$ where $h^*(n)$ is the true cost to reach the goal from $n$. 

- **Consistency (Monotonicity)**: A heuristic is consistent if, for every [[#2.1.4 Node|node]] $n$ and every successor $n'$ of $n$ generated by any [[#2.1.1 Action (Data Structure)|action]] $a$, the estimated cost of reaching the goal from $n$ is no greater than the cost of getting to $n'$ plus the estimated cost from $n'$ to the goal. 
  Formally: $$h(n) \leq c(n, a, n') + h(n')$$where $c(n, a, n')$ is the cost of the action $a$ leading from $n$ to $n'$. Consistency implies admissibility.
#### Common Heuristics
##### Euclidean Distance
- **Euclidean Distance**: The straight-line distance between two points in a plane. It’s often used in problems where the movement is not restricted to grid lines. The Euclidean distance between two points $(x_1, y_1)$ and $(x_2, y_2)$ is calculated as:
  $$h(n) = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
###### Pseudocode:
```plaintext
FUNCTION EuclideanDistance(node, goal)
	RETURN sqrt((goal.x - node.x)^2 + (goal.y - node.y)^2)
END FUNCTION
```
##### Manhattan Distance
- **Manhattan Distance**: The distance between two points measured along axes at right angles. It’s used in grid-based problems where movement is restricted to horizontal and vertical directions. The Manhattan distance between two points $(x_1, y_1)$ and $(x_2, y_2)$ is calculated as:
  $$h(n) = |x_2 - x_1| + |y_2 - y_1|$$
###### Pseudocode:
```plaintext
FUNCTION ManhattanDistance(node, goal)
	RETURN abs(goal.x - node.x) + abs(goal.y - node.y)
END FUNCTION
```

##### Hamming Distance 
- **Hamming Distance**: The Hamming distance between two strings of equal length is defined as the number of positions at which the corresponding symbols differ. It is commonly used in problems like the 8-puzzle, binary data comparison, and other scenarios where elements are compared positionally. Mathematically, for two strings $a$ and $b$ of length $n$, the Hamming distance $h(a, b)$ is given by: $$h(a, b) = \sum_{i=1}^{n} \delta(a_i, b_i) $$ where $\delta(a_i, b_i)$ is: $$\delta(a_i, b_i) = \begin{cases} 0 & \text{if } a_i = b_i \\ 1 & \text{if } a_i \neq b_i \end{cases} $$In other words, the Hamming distance is the sum of the differences between corresponding elements of the two strings.

###### Pseudocode:
```
FUNCTION HammingDistance(node, goal)
    distance = 0
    FOR i FROM 1 TO length(node)
        IF node[i] ≠ goal[i] THEN
            distance = distance + 1
        END IF
    END FOR
    RETURN distance
END FUNCTION
```

#### Applications of Heuristic Functions

##### 1. [[#1.2.1.1 A* Search|**A* Search**]]
A* Search uses both the path cost $g(n)$ from the start node to the current node $n$ and the heuristic cost $h(n)$ from $n$ to the goal to determine the next node to expand. The node with the lowest combined cost $$f(n) = g(n) + h(n)$$ is selected. This guarantees finding the shortest path if the heuristic is admissible and consistent.

- **Example**: Pathfinding in a grid where the Euclidean or Manhattan distance is used as a heuristic to guide the search towards the goal efficiently.

##### 2. [[#1.2.1.7 Greedy Best-First Search (GBFS)|**Greedy Best-First Search**]]
Greedy Best-First Search uses only the heuristic function $h(n)$ to select the next node to expand, choosing the node that appears closest to the goal. While this approach can be faster, it does not guarantee an optimal solution, as it may ignore shorter paths with higher immediate costs.

- **Example**: Navigation problems where the algorithm selects the next location based purely on straight-line distance, potentially missing more optimal routes.\

---
### 1.3.2 Optimal Solution
An optimal solution is a solution that yields the best possible outcome according to a specific criterion or objective function. It represents the most efficient or effective solution among all possible solutions, whether in terms of [[#2.2.4 Path Cost|cost]], time, accuracy, or other relevant metrics.
#### Formal Definition
Given an optimization problem with an objective function $f(x)$, where $x$ represents a potential solution, an optimal solution $x_{\text{opt}}$ is one that either minimizes or maximizes the objective function, depending on the problem's requirements.

- For minimization problems:
  $$x_{\text{opt}} = \text{argmin}_{x \in X} \ f(x)$$
- For maximization problems:
  $$x_{\text{opt}} = \text{argmax}_{x \in X} \ f(x)$$

Where $X$ is the set of all possible solutions.
#### Example:
- In an AI [[#1.5.1.2 Search Problems For AI|search problem]], the optimal solution is the sequence of actions that leads the agent from the initial state to the goal state with the minimum [[#2.2.4 Path Cost]].
- In a machine learning model, the optimal solution could be the set of parameters that minimizes the loss function, resulting in the most accurate predictions.
#### Pseudocode:
```plaintext
FUNCTION OptimalSolution(solution_set)
	RETURN solution with the minimum path cost from solution_set
END FUNCTION
```

---
## 1.4 Common Programming Patterns
### 1.4.1 Monotonic Stack Pattern
A monotonic stack is a stack data structure that maintains its elements in a strictly increasing or decreasing order. It is particularly useful for solving problems that involve finding the next greater or smaller element or calculating spans.

#### Key Points

1. Monotonic stacks can solve certain problems in `O(n)` time, which might otherwise require `O(n^2)` time.
2. They are especially useful for problems involving comparisons with previous elements.
3. The choice between an increasing or decreasing monotonic stack depends on the specific problem.
4. Monotonic stacks often use indices instead of values to handle duplicates and retrieve additional information.

#### Basic Concept

The monotonic stack maintains its order (either increasing or decreasing) by popping elements that violate this order before pushing a new element. This allows for efficient solutions to problems that involve comparisons with previous elements.

#### Types of Monotonic Stacks

1. **Monotonic Increasing Stack**: Each element in the stack is smaller than or equal to the element on top of it.
2. **Monotonic Decreasing Stack**: Each element in the stack is larger than or equal to the element on top of it.

#### Pseudocode for Monotonic Stack

Here is the general structure for using a monotonic increasing stack:

```plaintext
FUNCTION monotonicStackIncreasing(arr)
    n = LENGTH(arr)
    stack = EMPTY STACK
    result = NEW array of size n
    
    FOR i FROM 0 TO n-1 DO
        WHILE stack IS NOT EMPTY AND arr[stack.TOP()] <= arr[i] DO
            stack.POP()
        END WHILE
        
        IF stack IS EMPTY THEN
            result[i] = -1  // or any default value
        ELSE
            result[i] = stack.TOP()
        END IF
        
        stack.PUSH(i)
    END FOR
    
    RETURN result
END FUNCTION
```

#### Common Applications

1. Next Greater Element problems.
2. Next Smaller Element problems.
3. Largest Rectangle in Histogram.
4. Daily Temperatures.
5. Stock Span Problem.

#### Example: Next Greater Element

```plaintext
FUNCTION nextGreaterElement(arr)
    n = LENGTH(arr)
    stack = EMPTY STACK
    result = NEW array of size n, initialized with -1
    
    FOR i FROM n-1 TO 0 DO
        WHILE stack IS NOT EMPTY AND stack.TOP() <= arr[i] DO
            stack.POP()
        END WHILE
        
        IF stack IS NOT EMPTY THEN
            result[i] = stack.TOP()
        END IF
        
        stack.PUSH(arr[i])
    END FOR
    
    RETURN result
END FUNCTION
```

---
### 1.4.2 Modified Binary Search Pattern
The Modified Binary Search pattern extends the classic binary search algorithm to solve a variety of problems in sorted arrays. It retains the `O(log n)` time complexity of standard binary search but adapts to handle different scenarios.

#### Key Points
1. Modified binary search retains the `O(log n)` time complexity of standard binary search.
2. The key is to adjust the `left` and `right` pointers based on the specific problem requirements.
3. It’s crucial to handle edge cases and ensure the search space is reduced in each iteration.
4. Modified binary search can be applied to problems that aren’t immediately recognizable as binary search problems.

#### Basic Concept
While the standard binary search looks for an exact match, modified binary search can be adapted to find:

- The first or last occurrence of an element.
- The closest element to a target.
- An element satisfying certain conditions.

#### Pseudocode for Standard Binary Search

```plaintext
FUNCTION binarySearch(arr, target)
    left = 0
    right = LENGTH(arr) - 1
    
    WHILE left <= right DO
        mid = left + (right - left) / 2
        IF arr[mid] == target THEN
            RETURN mid
        ELSE IF arr[mid] < target THEN
            left = mid + 1
        ELSE
            right = mid - 1
        END IF
    END WHILE
    
    RETURN -1  // Element not found
END FUNCTION
```

#### Common Modifications
1. Finding the first occurrence of an element.
2. Finding the last occurrence of an element.
3. Finding the ceiling of an element (smallest element greater than or equal to the target).
4. Finding the floor of an element (largest element smaller than or equal to the target).
5. Searching in a rotated sorted array.
6. Finding the peak element.

#### Example: First Occurrence of an Element

```plaintext
FUNCTION findFirstOccurrence(arr, target)
    left = 0
    right = LENGTH(arr) - 1
    result = -1
    
    WHILE left <= right DO
        mid = left + (right - left) / 2
        IF arr[mid] == target THEN
            result = mid
            right = mid - 1  // Continue searching on the left side
        ELSE IF arr[mid] < target THEN
            left = mid + 1
        ELSE
            right = mid - 1
        END IF
    END WHILE
    
    RETURN result
END FUNCTION
```

#### Example: Search in Rotated Sorted Array

```plaintext
FUNCTION searchRotatedArray(arr, target)
    left = 0
    right = LENGTH(arr) - 1
    
    WHILE left <= right DO
        mid = left + (right - left) / 2
        IF arr[mid] == target THEN
            RETURN mid
        
        // Check which half is sorted
        IF arr[left] <= arr[mid] THEN
            // Left half is sorted
            IF arr[left] <= target < arr[mid] THEN
                right = mid - 1
            ELSE
                left = mid + 1
            END IF
        ELSE
            // Right half is sorted
            IF arr[mid] < target <= arr[right] THEN
                left = mid + 1
            ELSE
                right = mid - 1
            END IF
        END IF
    END WHILE
    
    RETURN -1  // Element not found
END FUNCTION
```

---
### 1.4.3 Prefix Sum Pattern
The prefix sum pattern is a technique for efficiently calculating cumulative sums in an array. It's particularly useful for solving problems that involve range sum queries, allowing for fast queries after a preprocessing step.

#### Basic Concept
Given an array `A` of `n` elements, the prefix sum array `P` is defined as: 
```
P[i] = A[0] + A[1] + ... + A[i]
```

Here, `P[i]` represents the sum of all elements in `A` from index `0` to `i`. 
#### Pseudocode for Computing Prefix Sum
```plaintext
FUNCTION computePrefixSum(A)
    n = LENGTH(A)
    P = NEW array of size n
    P[0] = A[0]
    FOR i FROM 1 TO n-1 DO
        P[i] = P[i-1] + A[i]
    END FOR
    RETURN P
END FUNCTION
```

#### Formulas
1. Computing the i-th prefix sum:
	```plaintext
    P[i] = P[i-1] + A[i]
    ```

2. Range sum query (sum of elements from index L to R, inclusive):
   ```plaintext
     sum(L, R) = P[R] - P[L-1]  (if L > 0) 
     sum(L, R) = P[R]           (if L = 0)
    ```

#### Applications
Prefix sums are particularly useful for:

1. Range sum queries in `O(1)` time.
2. Finding subarrays with a given sum.
3. Calculating moving averages.
4. Solving problems involving cumulative data.

#### Problem Example
Given an integer array `nums`, implement a class `NumArray` to handle multiple queries that calculate the sum of elements between indices `left` and `right` (inclusive).

**Example:**

```plaintext
Input:
["NumArray", "sumRange", "sumRange", "sumRange"]
[[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]

Output:
[null, 1, -1, -3]
```

#### Solution in Python3

```python
class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.p = nums[:]

        for i in range(1, len(nums)):
            self.p[i] = self.p[i - 1] + nums[i]

    def sumRange(self, left: int, right: int) -> int:
        if left == 0:
            return self.p[right]
        else:
            return self.p[right] - self.p[left - 1]
```

---
### 1.4.4 Pointer: Two-Pointer Pattern
The two-pointer pattern is an efficient technique that involves using two pointers to iterate through a data structure, such as an array or a linked list. This method can often reduce time complexity from `O(n^2)` to `O(n)` for certain problems.

#### Basic Concept
Two pointers are used to traverse the data structure in one of the following ways:

1. **Moving towards each other** (opposite directions).
2. **Moving in the same direction** at different speeds.
3. **One pointer is stationary**, and the other moves.

#### Pseudocode for Common Two-Pointer Scenarios

##### 1. Pointers Moving Towards Each Other

```plaintext
FUNCTION twoPointersOpposite(arr)
    left = 0
    right = LENGTH(arr) - 1
    WHILE left < right DO
        // Process or compare arr[left] and arr[right]
        IF condition THEN
            left++
        ELSE
            right--
        END IF
    END WHILE
    RETURN result
END FUNCTION
```

##### 2. Pointers Moving in Same Direction

```plaintext
FUNCTION twoPointersSameDirection(arr)
    slow = 0
    fast = 0
    WHILE fast < LENGTH(arr) DO
        // Process elements
        IF condition THEN
            slow++
        END IF
        fast++
    END WHILE
    RETURN result
END FUNCTION
```

#### Common Applications
1. Checking for palindromes.
2. Reversing an array or string.
3. Solving the Two Sum problem (finding a pair with a given sum).
4. Removing duplicates from a sorted array.
5. Solving the Container with Most Water problem.
6. Sliding window problems.

#### Example: Two Sum Problem
Here's a specific example of how the two-pointer pattern can be used to solve the Two Sum problem:

```plaintext
function twoSum(arr, target):
    left = 0
    right = length(arr) - 1
    sort(arr)  // Assume arr is sorted
    while left < right:
        currentSum = arr[left] + arr[right]
        if currentSum == target:
            return [arr[left], arr[right]]
        else if currentSum < target:
            left++
        else:
            right--
    return null  // No solution found
```

This approach has a time complexity of $O(n log n)$ due to sorting, or $O(n)$ if the array is already sorted.
#### Problem Example
Given a **1-indexed** array of integers `numbers` that is already **_sorted in non-decreasing order_**, find two numbers such that they add up to a specific `target` number. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

Return _the indices of the two numbers,_ `index1` _and_ `index2`_, **added by one** as an integer array_ `[index1, index2]` _of length 2._

The tests are generated such that there is **exactly one solution**. You **may not** use the same element twice.

Your solution must use only constant extra space.

**Example 1:**

**Input:** `numbers = [2,7,11,15], target = 9`
**Output:**`[1,2]`
**Explanation:** The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return `[1, 2]`.

#### Solution in Python3

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        i = 0
        j = len(nums) - 1
        
        for x in range(0, len(nums)):
            pointer_sum = nums[i] + nums[j]
            if pointer_sum == target: 
	            # We need to add one since they want it not zero index based
                return [i+1,j+1] 
            elif pointer_sum > target: 
	            # Since the list is sorted we know that if it is larger
	            # then we have to choose a smaller number which is why we
	            # degrement the rightmost pointer
                j-=1
            else:
                i+=1
```

---
### 1.4.5 Pointer: Fast and Slow Pointer Pattern
The fast and slow pointer pattern involves using two pointers that move at different speeds through a sequence. This pattern is particularly useful for detecting cycles in linked lists and solving other related problems efficiently.

#### Key Points
1. The fast and slow pointer pattern is efficient for cycle detection, requiring only `O(1)` extra space.
2. It is commonly used in linked list problems.
3. The pattern can be adapted to solve various other problems beyond cycle detection.
4. In cycle detection, if there’s a cycle, the pointers will eventually meet; if there’s no cycle, the fast pointer will reach the end.

#### Basic Concept
Two pointers traverse the data structure:

1. The slow pointer moves one step at a time.
2. The fast pointer moves two steps at a time.

If there’s a cycle, the fast pointer will eventually meet the slow pointer.

#### Pseudocode for Fast and Slow Pointer

``` plaintext
FUNCTION fastSlowPointer(head)
    slow = head
    fast = head
    
    WHILE fast IS NOT null AND fast.next IS NOT null DO
        slow = slow.next
        fast = fast.next.next
        
        IF slow == fast THEN
            RETURN true  // Cycle detected
        END IF
    END WHILE
    
    RETURN false  // No cycle
END FUNCTION
```

#### Common Applications
1. Detecting cycles in linked lists.
2. Finding the middle of a linked list.
3. Determining if a number is happy (in number theory).
4. Finding the start of a cycle in a linked list.

#### Example: Finding the Middle of a Linked List

```plaintext
FUNCTION findMiddle(head)
    IF head IS null THEN
        RETURN null
    END IF
    
    slow = head
    fast = head
    
    WHILE fast.next IS NOT null AND fast.next.next IS NOT null DO
        slow = slow.next
        fast = fast.next.next
    END WHILE
    
    RETURN slow  // This is the middle node
END FUNCTION
```

---
### 1.4.6 Reverse Linked List Pattern
Reversing a linked list is a fundamental operation that frequently arises in algorithms and coding interviews. It involves changing the direction of pointers in the list so that the last node becomes the first and vice versa.

#### Key Points
1. Reversing a linked list is an in-place operation, requiring no extra space.
2. Both iterative and recursive solutions are available, with the iterative approach generally preferred for its constant space complexity.
3. This pattern is often used as a building block for more complex linked list operations.
4. It's important to handle edge cases like empty lists or lists with only one node.

#### Basic Concept
To reverse a linked list, you need to change the `next` pointer of each node to point to its previous node. This is typically done by iterating through the list and keeping track of three pointers: previous, current, and next.

#### Pseudocode for Reversing a Linked List

```plaintext
FUNCTION reverseLinkedList(head)
    prev = null
    current = head
    
    WHILE current IS NOT null DO
        next = current.next
        current.next = prev
        prev = current
        current = next
    END WHILE
    
    RETURN prev  // New head of the reversed list
END FUNCTION
```

#### Applications
1. Checking if a linked list is a palindrome.
2. Reversing portions of a linked list (e.g., every k elements).
3. Reordering linked lists.
4. Detecting cycles (in combination with the fast-slow pointer pattern).

---
### 1.4.7 Sliding Window Pattern
The sliding window pattern is a technique used to process sequential data efficiently by maintaining a subset of elements (the "window") that moves through the data. This pattern can significantly reduce time complexity in many problems, particularly those involving arrays and strings.

#### Key Points
1. The sliding window pattern can reduce time complexity from `O(n^2)` or `O(n^3)` to `O(n)` in many cases.
2. It is particularly useful for problems involving arrays, strings, or other sequential data structures.
3. The window size can be fixed or variable, depending on the problem.
4. The pattern often involves maintaining a data structure (like a hash map) to track the window's contents efficiently.

#### Basic Concept
A "window" is defined as a range of elements in the array or string. This window can be fixed-size or variable-size. As the window slides through the data, the elements within it are processed.

#### Types of Sliding Windows
1. Fixed-size window.
2. Variable-size window.

#### Pseudocode for Sliding Window

##### Fixed-size Window

```plaintext
FUNCTION fixedSlidingWindow(arr, k)
    n = LENGTH(arr)
    window = NEW Window()
    
    // Initialize the first window
    FOR i FROM 0 TO k-1 DO
        window.add(arr[i])
    END FOR
    
    result = [window.getResult()]
    
    // Slide the window
    FOR i FROM k TO n-1 DO
        window.remove(arr[i-k])
        window.add(arr[i])
        result.append(window.getResult())
    END FOR
    
    RETURN result
END FUNCTION
```

##### Variable-size Window
```plaintext
FUNCTION variableSlidingWindow(arr, condition)
    n = LENGTH(arr)
    start = 0
    end = 0
    window = NEW Window()
    result = initialValue
    
    WHILE end < n DO
        window.add(arr[end])
        
        WHILE window.violatesCondition() DO
            window.remove(arr[start])
            start++
        END WHILE
        
        result = updateResult(result, window)
        end++
    END WHILE
    
    RETURN result
END FUNCTION
```

#### Common Applications
1. Finding the maximum sum subarray of size k.
2. Longest substring with k distinct characters.
3. Finding string anagrams.
4. Minimum window substring.
5. Maximum of all subarrays of size k.
6. Sequential sums or other similar problems.

#### Example: Maximum Sum Subarray of Size K

```plaintext
FUNCTION maxSumSubarray(arr, k)
    n = LENGTH(arr)
    IF n < k THEN
        RETURN null
    END IF
    
    windowSum = SUM(arr[0] TO arr[k-1])
    maxSum = windowSum
    
    FOR i FROM k TO n-1 DO
        windowSum = windowSum - arr[i-k] + arr[i]
        maxSum = MAX(maxSum, windowSum)
    END FOR
    
    RETURN maxSum
END FUNCTION
```

#### Problem Example
Given an integer array `nums` consisting of `n` elements, find a contiguous subarray of length `k` that has the maximum average value and return this value.

**Example:**

```plaintext
Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75
```

#### Solution in Python3

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        n = len(nums)

        max_sum = sum(nums[:k])
        window_sum = max_sum

        for i in range(1, n - k + 1):
            window_sum = window_sum - nums[i - 1] + nums[i + k - 1]
            max_sum = max(window_sum, max_sum)

        return max_sum / k
```

---
### 1.4.8 Top K Elements Pattern
The Top K Elements pattern is used to find the k largest or smallest elements in a collection. This pattern is frequently employed in problems involving sorting, prioritization, or identifying the most or least frequent elements.

#### Key Points
1. For the top k largest elements, use a min-heap of size k.
2. For the top k smallest elements, use a max-heap of size k.
3. The time complexity is typically `O(n log k)`, which is more efficient than sorting the entire array when k is much smaller than n.
4. This pattern can be adapted to solve a wide range of problems involving "top k" or "bottom k" elements.

#### Basic Concept
The core idea is to maintain a collection of the k most extreme (largest or smallest) elements encountered while processing the input. This is usually done using a heap data structure.

#### Pseudocode for Top K Elements
Here is the general structure for finding the k largest elements:

```plaintext
FUNCTION findTopKElements(arr, k)
    minHeap = NEW MinHeap()
    
    FOR element IN arr DO
        IF minHeap.SIZE() < k THEN
            minHeap.PUSH(element)
        ELSE IF element > minHeap.TOP() THEN
            minHeap.POP()
            minHeap.PUSH(element)
        END IF
    END FOR
    
    RETURN minHeap.ELEMENTS()
END FUNCTION
```

#### Common Applications
1. Finding the k largest or smallest elements in an array.
2. K closest points to the origin.
3. Top k frequent elements.
4. Kth largest element in a stream.
5. Sorting a nearly sorted array.

#### Example: Kth Largest Element in an Array

```plaintext
FUNCTION findKthLargest(nums, k)
    minHeap = NEW MinHeap()
    
    FOR num IN nums DO
        IF minHeap.SIZE() < k THEN
            minHeap.PUSH(num)
        ELSE IF num > minHeap.TOP() THEN
            minHeap.POP()
            minHeap.PUSH(num)
        END IF
    END FOR
    
    RETURN minHeap.TOP()
END FUNCTION
```

#### Example: Top K Frequent Elements
```plaintext
FUNCTION topKFrequent(nums, k)
    freqMap = NEW HashMap()
    FOR num IN nums DO
        freqMap[num] = freqMap.GET(num, 0) + 1
    END FOR
    
    minHeap = NEW MinHeap()
    FOR num, freq IN freqMap.ITEMS() DO
        IF minHeap.SIZE() < k THEN
            minHeap.PUSH((freq, num))
        ELSE IF freq > minHeap.TOP()[0] THEN
            minHeap.POP()
            minHeap.PUSH((freq, num))
        END IF
    END FOR
    
    RETURN [num FOR freq, num IN minHeap.ELEMENTS()]
END FUNCTION
```

## 1.5 Common Programming Problems
### 1.5.1 Search Problems

#### 1.5.1.1 Adversarial Search
Adversarial search refers to a type of problem-solving in AI where multiple agents, typically two, are competing against each other, and the outcome depends on the actions of all participants. This is common in zero-sum games, where one player's gain is another player's loss, such as in chess, checkers, and tic-tac-toe. The goal of adversarial search is to find the best strategy for a player, assuming that the opponent is also playing optimally.

##### Formal Definition
An adversarial search problem can be defined by the tuple $(S, A, \delta, P, U, s_0, T)$, where:
- **$S$** is the set of all possible [[#State|states]].
- **$A$** is the set of all possible [[#Action|actions]].
- **$\delta: S \times A \rightarrow S$** is the transition function that describes the result of applying an action to a state.
- **$P: S \rightarrow { \text{Player 1}, \text{Player 2}, \dots }$** is the function determining which player’s turn it is.
- **$U: S \rightarrow \mathbb{R}$** is the utility function that assigns a value to terminal states, representing the outcome for the players (e.g., win, lose, or draw).
- **$s_0 \in S$** is the [[#Initial State|initial state]] of the game.
- **$T: S \rightarrow \text{bool}$** is the test to determine if the state is terminal, meaning the game has ended.

##### Objective
The objective in adversarial search is to determine a sequence of actions that leads to an optimal outcome for the player considering the possible responses of the opponent.

---
#### 1.5.1.2 General Search Problem
A general search problem involves finding a target item, value, or configuration starting from a given initial state or condition. This type of problem is common in various fields such as data retrieval, navigation, and puzzle solving.
##### Formal Definition
A general search problem can be defined by the 3-tuple $(S, s_0, G)$, where:
- $S$: Set of all possible states or configurations.
- $s_0 \in S$: Initial state, representing the starting condition.
- $G \subseteq S$: Set of goal state(s) that represent the desired end conditions.

##### Objective
The objective of a general search problem is to determine whether a goal state $s_g \in G$ exists within the state space $S$, and if so, to identify the sequence of steps that leads from the initial state $s_0$ to the goal state $s_g$. The solution is not concerned with minimizing costs but rather with simply reaching the goal.

---
#### 1.5.1.3 Search Problems For AI 
A problem defined by a set of [[#2.1.5 State State|states]], an [[#2.1.6 State Initial State|initial state]], [[#2.1.1 Action (Data Structure)|actions]], a [[#2.2.5 Transition Model/Function|transition model]], a [[#2.2.3 Goal Test|goal test]], and a [[#2.2.4 Path Cost|path cost]] function. The objective of a search problem is to find a sequence of actions that leads from the initial state to a [[#2.1.7 State Goal State / Final State|final state]] (goal state) with the minimum path cost.
##### Formal Definition
A search problem is defined by the 6-tuple $(S, A, \delta, s_0, G, c)$, where:
- $S$ is the set of all possible [[#2.1.5 State State|states]].
- $A$ is the set of all possible [[#2.1.1 Action (Data Structure)|actions]].
- $\delta: S \times A \rightarrow S$ is the [[#2.2.5 Transition Model/Function|transition function]], which defines the result of applying an action to a state.
- $s_0 \in S$ is the [[#2.1.6 State Initial State|initial state]] from which the search begins.
- $G \subseteq S$ is the set of goal states that satisfy the [[#2.2.3 Goal Test|goal test]].
- $c: S \times A \times S \rightarrow \mathbb{R}$ is the [[#2.2.2 Cost Function|cost function]], which defines the cost of transitioning from one state to another via an action, contributing to the [[#2.2.4 Path Cost|path cost]].

##### Objective
The objective of a search problem is to find a solution, which is a sequence of actions ${a_1, a_2, \dots, a_n}$ that transforms the [[#2.1.6 State Initial State|initial state]] $s_0$ into a goal state $s_g \in G$, such that the path cost $g(s_g)$ is minimized.

---
# 2. AI 
## 2.1 Core Concepts

### 2.1.1 Non-Knowledge-Based AI Concepts
This section covers the foundational concepts and data structures used in AI that do not involve explicit knowledge representation or logical reasoning.

#### 2.1.1.1 Action (Data Structure)
The **Action** data structure represents a specific choice or operation that can be applied to a [[#State|state]]. It defines what can be done in a given state to transition to another state.

##### Components
- **Name**: A string or identifier that represents the action.
- **Parameters**: Any additional information needed to perform the action.

##### Example:
- In a grid world, an action might be "Move North," with parameters defining the specific move.
- Action structure:
  - **Name**: "Move"
  - **Parameters**: "North"

##### Pseudocode
```plaintext
// Action structure
STRUCT Action
	VARIABLE name
	VARIABLE parameters

	FUNCTION Action(name, parameters)
	    THIS.name ← name
	    THIS.parameters ← parameters
	END FUNCTION
END STRUCT
```

---
#### 2.1.1.2 Agent
An agent is an entity that perceives its environment and acts upon that environment.

##### Example:
- A robot navigating through a maze is an agent. It perceives its surroundings using sensors (like detecting walls) and acts by moving in different directions to find the exit.

##### Pseudocode:
```plaintext
// Agent
STRUCT Agent
    state: State
    FUNCTION PerceiveEnvironment() -> Percept
    FUNCTION SelectAction(percept: Percept) -> Action
    FUNCTION UpdateState(action: Action, percept: Percept)
END STRUCT
```

---
#### 2.1.1.3 Frontier
The frontier is a data structure used in search algorithms to keep track of the nodes that have been generated but not yet explored. It is often implemented as a queue, stack, priority queue, or other data structure depending on the search strategy being used (e.g., breadth-first search, depth-first search, or uniform-cost search).

##### Components
- **Nodes**: The frontier contains a collection of [[#Node|nodes]], each representing a [[#State|state]] in the search space.
- **Data Structure**: The specific data structure used to implement the frontier depends on the search strategy. For example:
  - **Queue**: For breadth-first search.
  - **Stack**: For depth-first search.
  - **Priority Queue**: For uniform-cost search or A* search.

##### Example:
- In a breadth-first search, the frontier is implemented as a queue that stores nodes to be explored in the order they were generated. The node at the front of the queue is expanded first.

##### Pseudocode:
```plaintext
// Frontier
STRUCT Frontier
	VARIABLE nodes ← []
	FUNCTION AddNode(node)
	    APPEND node TO nodes
	END FUNCTION
	
	FUNCTION RemoveNode()
		// Depending on the search strategy
		// this could be a pop from the front, back, or based on priority
		// Stack for DFS for example and queue for BFS
	    RETURN POP nodes  
	END FUNCTION
	
	FUNCTION IsEmpty()
	    RETURN LENGTH(nodes) = 0
	END FUNCTION
END STRUCT
```

---
#### 2.1.1.4 Node
A node is a data structure used in search algorithms to represent a specific [[#State|state]] in the search space. Each node contains information about the state it represents, its parent node, the action that was applied to the parent to generate this node, and the cumulative [[#2.2.4 Path Cost|path cost]] to reach this node, if applicable.

##### Components
- **State**: The [[#State|state]] represented by the node.
- **Parent**: The node corresponding to the previous state (i.e., the state from which this node was generated).
- **Action**: The [[#Action|action]] that was applied to the parent node to generate this node.
- **Path Cost**: The cumulative [[#2.2.4 Path Cost|path cost]] from the [[#Initial State|initial state]] to this node. This is often denoted as $g(n)$ where $n$ is the node.

##### Example:
- In a pathfinding algorithm, a node might represent a specific position on a grid (the state), with a reference to the previous position (the parent), the movement direction taken (the action), and the total distance traveled from the start (the path cost).

##### Pseudocode:
```plaintext
// Node structure
STRUCT Node
	VARIABLE state
	VARIABLE parent
	VARIABLE action
	VARIABLE path_cost

	FUNCTION Node(state, parent, action, path_cost)
	    THIS.state ← state
	    THIS.parent ← parent
	    THIS.action ← action
	    THIS.path_cost ← path_cost
	END FUNCTION

	FUNCTION GetPath() -> LIST OF Action
	    path ← EMPTY LIST
	    currentNode ← THIS
	    
	    WHILE currentNode.parent IS NOT NULL DO
	        INSERT currentNode.action AT BEGINNING OF path
	        currentNode ← currentNode.parent
	    END WHILE
	    
	    RETURN path
	END FUNCTION
END STRUCT
```

---
#### 2.1.1.5 State: State
A configuration of the [[#Agent|agent]] and its environment.

##### Example:
- In a video game, a state might represent the position of the player, the health level, the positions of enemies, and other relevant details at a particular moment.

##### Pseudocode:
```plaintext
// State
STRUCT State
    // Properties that define the state
    // For example, in a grid world:
    x: Integer
    y: Integer
    // Other relevant properties
END STRUCT
```

---
#### 2.1.1.6 State: Initial State
The [[#States|state]] in which the agent begins.

##### Example:
- In a chess game, the initial state is the standard starting position of all the pieces on the board.

##### Pseudocode:
```plaintext
// Initial State
initialState = State(x: 0, y: 0)  // Example for a grid world
```

---
#### 2.1.1.7 State: Goal State / Final State
The [[#States|state]] in which the [[#Agent|agent]] ends, e.g., has reached its goal or reached an ending condition.

##### Example:
- In a maze, the final state is when the agent reaches the exit.
- In a game of chess, the final state could be a checkmate, stalemate, or draw.

##### Pseudocode:
```plaintext
// Final State
finalState = State(x: 10, y: 10)  // Example for a grid world
```

---
#### 2.1.1.8 State: State Space
The set of all [[#State|states]] reachable from the [[#Initial State|initial state]] by any sequence of [[#Action|actions]].

##### Formal Definition
Given a set of [[#State|states]] $S$ and a set of [[#Action|actions]] $A$, the state space $\mathcal{S}$ is defined as the set of all states that can be reached from the [[#Initial State|initial state]] $s_0$ through any sequence of actions. Formally, the state space $\mathcal{S}$ is the closure of $s_0$ under the transition function $\delta$.

$$\mathcal{S}=\{s\in S | s= \delta(s_0,a_1,a_2,\dots ,a_n)\texttt{ for some sequence of actions } a_1 a_2, \dots ,a_n \in A\}$$

##### Example:
- In a sliding puzzle (like the 8-puzzle), the state space consists of all possible arrangements of the puzzle pieces on the grid. Each state represents a specific configuration of the tiles, including the position of the empty space. The state space includes every possible configuration that can be reached by sliding the tiles around from the initial state.

##### Pseudocode:
```plaintext
// State Space
FUNCTION StateSpace(s_0) 
    state_space ← {s_0}
    FOR each action sequence a_1, a_2, ..., a_n
        s ← ApplyActions(s_0, a_1, a_2, ..., a_n)
        state_space ← state_space ∪ {s}
    END FOR
RETURN state_space
```

### 2.1.2 Knowledge-Based AI Concepts
This section focuses on AI concepts that involve reasoning, knowledge representation, and logical inference.

#### 2.1.2.1 Knowledge-Based Agent
A knowledge-based agent is an entity that maintains a knowledge base, uses reasoning mechanisms to derive new knowledge, and makes decisions based on this internal representation of knowledge.

##### Knowledge Base
The **Knowledge Base** is a set of [[#3.1 Sentences in Propositional Logic|sentences]] known by the knowledge-based agent. These sentences represent the facts, rules, and general knowledge that the agent uses to make decisions and draw inferences. The knowledge base is typically stored in a formal language, such as propositional logic or first-order logic, allowing the agent to perform logical reasoning.

- **Updating the Knowledge Base**: The agent continuously updates its knowledge base as it perceives new information from the environment. This new information could either add new sentences to the knowledge base or modify existing ones.
    
- **Using the Knowledge Base for Reasoning**: The agent uses the knowledge base to reason about the world, derive new knowledge, and make informed decisions. Logical inference mechanisms are applied to the sentences in the knowledge base to determine the truth of new propositions or to guide decision-making processes.

##### Example:
- A medical diagnosis system that suggests treatments. The system maintains a knowledge base of symptoms, diseases, and treatments. When presented with a patient's symptoms, it reasons through the knowledge base to diagnose the disease and suggest the best treatment.

##### Pseudocode:
```plaintext
// Knowledge-Based Agent
STRUCT KnowledgeBasedAgent
    knowledgeBase: KnowledgeBase
    state: State
    
    FUNCTION PerceiveEnvironment() -> Percept
        // Perceive the environment and update the knowledge base
        percept = GetPerceptFromEnvironment()
        knowledgeBase.Update(percept)
        RETURN percept
    
    FUNCTION ReasonAndInfer(percept: Percept) -> Inference
        // Use reasoning mechanisms (e.g., logic inference) to derive new knowledge
        inference = knowledgeBase.Infer(percept)
        RETURN inference
    
    FUNCTION SelectAction(inference: Inference) -> Action
        // Select the best action based on inferred knowledge
        action = DecideAction(inference)
        RETURN action
    
    FUNCTION UpdateState(action: Action, inference: Inference)
        // Update the agent's internal state based on action and inference
        state.Update(action, inference)
END STRUCT
```

---
#### 2.1.2.2 Entailment
[[#3.6 Entailment in Propositional Logic|Entailment]] is a fundamental concept in logic, representing a relationship between sentences where one sentence logically follows from another. If a set of sentences $\Gamma$ entails a sentence $\phi$, it means that whenever all the sentences in $\Gamma$ are true, the sentence $\phi$ must also be true.

##### Formal Definition
Entailment is denoted as $\Gamma \models \phi$, meaning that $\phi$ is a logical consequence of $\Gamma$. Formally:
$$\Gamma \models \phi \text{ if and only if every model of } \Gamma \text{ is also a model of } \phi.$$
- **$\Gamma$**: A set of sentences (also known as premises).
- **$\phi$**: A single sentence (also known as the conclusion).

##### Example
- Let $\Gamma$ be a set of two sentences: $\{P \rightarrow Q, P\}$.
- If $\Gamma$ entails $\phi = Q$, then whenever $P \rightarrow Q$ and $P$ are true, $Q$ must also be true.

This concept is crucial in AI for determining whether certain conclusions can be logically derived from a set of known facts.

##### Pseudocode for Entailment Check:
```plaintext
// Function to check if a set of sentences Γ entails a sentence φ
FUNCTION CheckEntailment(Γ, φ) -> Boolean
    FOR each model m in all possible models:
        IF m satisfies Γ THEN
            IF m does not satisfy φ THEN
                RETURN False
        END IF
    END FOR
    RETURN True
END FUNCTION
```

---
#### 2.1.2.3 Inference
[[#3.7 Inference|Inference]] is the process of deriving logical conclusions from premises or known facts. In AI, inference is used by knowledge-based agents to deduce new information and make decisions based on existing knowledge.

##### Modus Ponens
One of the most common forms of inference is **modus ponens**:
- **Given**: $P \rightarrow Q$ (If $P$, then $Q$) and $P$ (Premise).
- **Infer**: $Q$ (Therefore, $Q$).

###### Pseudocode:
```plaintext
// Pseudocode for Modus Ponens
FUNCTION ModusPonens(Premise1, Premise2)
    IF (Premise1 == (P -> Q)) AND (Premise2 == P) THEN
        RETURN Q
    ELSE
        RETURN "No Inference Possible"
    END IF
END FUNCTION
```

##### Example
- If it is known that "If it is raining, then the ground is wet" ($P \rightarrow Q$) and "It is raining" ($P$), then we can infer "The ground is wet" ($Q$).

##### Types of Inference

###### **Deductive Inference**:
This involves deriving specific conclusions from general principles or premises. If the premises are true, the conclusion must also be true.

- **Example**: All humans are mortal (general). Socrates is a human (specific). Therefore, Socrates is mortal.

###### Pseudocode:
```plaintext
// Pseudocode for Deductive Inference
FUNCTION DeductiveInference(GeneralRule, SpecificCase)
    IF (GeneralRule == "All X are Y") AND (SpecificCase == "Z is X") THEN
        RETURN "Z is Y"
    ELSE
        RETURN "No Inference Possible"
    END IF
END FUNCTION
```

###### **Inductive Inference**:
This involves deriving general conclusions from specific examples or observations. The conclusion is probable but not guaranteed.

- **Example**: The sun has risen every day in history. Therefore, the sun will rise tomorrow.

###### Pseudocode:
```plaintext
// Pseudocode for Inductive Inference
FUNCTION InductiveInference(Observations)
    COUNT = 0
    FOR each Observation IN Observations DO
        IF Observation == "X happened" THEN
            COUNT += 1
        END IF
    END FOR
    
    IF COUNT == LENGTH(Observations) THEN
        RETURN "X is likely to happen again"
    ELSE
        RETURN "Conclusion is uncertain"
    END IF
END FUNCTION
```

###### **Abductive Inference**:
This involves inferring the most likely explanation or hypothesis for a set of observations. It is often used in diagnostic reasoning.

- **Example**: The ground is wet. The most likely explanation is that it has rained.

###### Pseudocode:
```plaintext
// Pseudocode for Abductive Inference
FUNCTION AbductiveInference(Observation)
    POSSIBLE_EXPLANATIONS = GetPossibleExplanations(Observation)
    
    BEST_EXPLANATION = SELECT BestExplanation FROM POSSIBLE_EXPLANATIONS
    
    RETURN BEST_EXPLANATION
END FUNCTION
```

---
#### 2.1.2.4 Inference by Resolution
**Inference by Resolution** is a powerful technique used in artificial intelligence, particularly in logic-based reasoning systems, to determine entailment by systematically resolving clauses. This approach is commonly employed in automated theorem proving, logic programming, and reasoning systems to prove the validity of statements or to find contradictions. It is fundamentally a **proof by contradiction** method, where the negation of the desired conclusion is shown to lead to an inconsistency.

##### Purpose
The purpose of inference by resolution in AI is to prove that a set of premises entails a conclusion by attempting to derive an empty clause (a contradiction). This method is particularly useful for demonstrating that a given statement cannot coexist with the premises, proving entailment or unsatisfiability.

##### Important Requirement: Conversion to CNF
Before applying inference by resolution, the entire knowledge base, including the negation of the desired conclusion, **must be converted to Conjunctive Normal Form (CNF)**. CNF is a standardized format in propositional logic where a formula is expressed as a conjunction of disjunctions (ANDs of ORs). This conversion is crucial because the resolution rule operates directly on clauses in CNF.

##### Process
1. **Convert to CNF**: Ensure that all statements in the knowledge base and the negation of the conclusion are in CNF.
2. **Start with Clauses**: Begin with a set of CNF clauses derived from the knowledge base, including the negation of the statement you want to prove.
3. **Resolution**: Iteratively resolve pairs of clauses that contain complementary literals (e.g., $P$ and $\neg P$) to form new clauses.
4. **Derive the Empty Clause**: Continue resolving until you either derive the empty clause, indicating a contradiction (thus proving the original statement by refutation), or reach a point where no further resolutions are possible.
5. **Prove Entailment**: If the empty clause is derived, the original statement is entailed by the premises, confirming the conclusion via proof by contradiction.

##### Example
Suppose we want to prove that a conclusion $Q$ is entailed by a set of premises.

**Given**:
- Premises: $(P \rightarrow Q)$ and $(\neg Q)$.
- Convert implications to disjunctive form: $(\neg P \lor Q)$.
- To prove $Q$, negate it and add $\neg Q$ to the set.

**Resolution Steps**:
1. Convert all premises and the negated conclusion into CNF.
2. Resolve $(\neg P \lor Q)$ with $(\neg Q)$.
3. The result is $\neg P$.
4. Since no further resolutions are possible without deriving an empty clause, we conclude that $Q$ was necessary to avoid contradiction.

##### AI Focused Application
**Proving by Contradiction**:
- In AI, inference by resolution is used as a proof by contradiction. You start by assuming the negation of what you want to prove and resolve clauses systematically. If the resolution process leads to the empty clause, it indicates that the assumption was false, thereby proving the original statement.

**In Proving Entailment**:
- Resolution is used in AI systems to prove entailment by showing that the negation of the desired conclusion leads to a contradiction.
- This approach is foundational in logic programming, where clauses are systematically resolved to derive new information or verify the truth of a statement.

**Automated Reasoning**:
- In AI, automated reasoning systems use resolution as a core technique for tasks like SAT solving, where the goal is to determine if a set of logical statements can be satisfied simultaneously.
- The system iterates through possible resolutions, either confirming the statements are consistent or identifying contradictions.

##### Pseudocode for Inference by Resolution
```plaintext
// Function for Inference by Resolution
FUNCTION Resolve(Clauses) -> Boolean
    REPEAT UNTIL no new clauses can be derived:
        SELECT pair of clauses (C1, C2) with complementary literals
        RESOLVENT ← ResolveClauses(C1, C2)
        
        IF RESOLVENT is the empty clause THEN
            RETURN True // Contradiction found, proving entailment
        END IF
        
        ADD RESOLVENT to the set of clauses
    END REPEAT
    
    RETURN False // No contradiction found, entailment not proven
END FUNCTION

FUNCTION ResolveClauses(C1, C2) -> Clause
    // Example: If C1 = (P ∨ Q) and C2 = (¬P ∨ R), resolve them
    REMOVE complementary literals (P, ¬P)
    RETURN new clause combining remaining literals (Q ∨ R)
END FUNCTION
```

## 2.2 Key Functions
### 2.2.1 Action (Function)
Choices that the agent can take in a given [[#State|state]], an action will lead to a transition from the current [[#State|state]] to a new [[#State|state]].
#### Formal Definition
Given a [[#State|state]] $s$, the function $\texttt{Actions}(s)$ returns the set of all possible actions that can be taken from the [[#State|state]] $s$.

Formally we have that:$$\texttt{Actions}: S \rightarrow \mathcal{P}(A)$$
Where $\mathcal{P}(A)$ is the [[Math definitions#Powerset ($\mathcal{P}(X)$)|powerset]] of $A$, meaning that $\texttt{Actions}(s)$ returns the [[Math definitions#Subset ($A \subseteq B$)|subset]] of actions available in [[#State|state]] $s$  
#### Example:
- In a grid world, if the agent is at position (2, 2), the possible actions might be:
    - Move North
    - Move South
    - Move East
    - Move West
- Here, $\texttt{Actions}((2, 2))$ might return the set $\{ \text{"North"}, \text{"South"}, \text{"East"}, \text{"West"} \}$.
#### Pseudocode
```plaintext
// Action
FUNCTION Actions(s)
	RETURN set of possible actions from state s
END FUNCTION
```

---
### 2.2.2 Cost Function
A function that assigns a numerical cost to performing an [[#Action|action]] in a given [[#State|state]], leading to a transition to another state. The cost function is used to evaluate the cost of different paths and is essential for determining the [[#2.2.4 Path Cost|path cost]] in a [[#Search Problem|search problem]].
#### Formal Definition
Given a [[#State|state]] $s$, an [[#Action|action]] $a$, and a resulting state $s'$, the cost function $c(s, a, s')$ returns the cost of performing the action $a$ in state $s$ to reach state $s'$.
$$c: S \times A \times S \rightarrow \mathbb{R}$$
Where:
- $S$ is the set of all possible [[#State|states]].
- $A$ is the set of all possible [[#Action|actions]].
- $\mathbb{R}$ represents the set of real numbers (indicating the cost).
#### Example:
- In a grid-based pathfinding problem, if moving from one cell to an adjacent cell has a cost of 1, then for any state $s$ and adjacent state $s'$, $c(s, \text{"Move"}, s') = 1$.
- In a road navigation problem, the cost function might represent the distance between two cities. If the cost of driving from city $A$ to city $B$ is 50 miles, then $c(\text{City A}, \text{"Drive"}, \text{City B}) = 50$.
#### Pseudocode:
```plaintext
// Cost Function
FUNCTION CostFunction(s, a, s_prime)
	RETURN cost of transitioning from state s to state s_prime using action a
END FUNCTION
```

---
### 2.2.3 Goal Test
A test that determines whether a given [[#State|state]] is a [[#Final State|final state]] or meets the criteria for solving the problem.
#### Formal Definition
Given a set of [[#State|states]] $S$, a goal test is a function $\texttt{GoalTest}(s)$ that returns `True` if the [[#State|state]] $s \in S$ is a [[#Final State|final state]] and `False` otherwise.

Formally, we have: $$\texttt{GoalTest}: S \rightarrow \{ \texttt{True}, \texttt{False} \}$$
#### Example:
- In a maze-solving problem, the goal test checks if the agent has reached the exit. If the agent's current position corresponds to the exit position, `GoalTest(s)` returns `True`; otherwise, it returns `False`.
- In a chess game, the goal test might check if the game is in a checkmate position. If the current state represents a checkmate, `GoalTest(s)` returns `True`.
#### Pseudocode:
```plaintext
// Goal State
FUNCTION GoalTest(s)
	IF s meets the goal criteria THEN
		RETURN TRUE
	ELSE
		RETURN FALSE
	END IF
END FUNCTION
```

---
### 2.2.4 Path Cost
The total cost associated with a sequence of [[#Action|actions]] taken to reach a particular [[#State|state]] from the [[#Initial State|initial state]].
#### Formal Definition
Given a sequence of [[#Action|actions]] $a_1, a_2, \dots, a_n$ that transforms the [[#initial state|initial state]] $s_0$ into a [[#State|state]] $s_n$, the path cost $g(s_n)$ is the sum of the costs associated with each [[#Action|action]] in that sequence.

Formally, if $c(s, a, s')$ represents the cost of performing [[#Action|action]] $a$ in [[#State|state]] $s$ to reach [[#State|state]] $s'$, then the path cost $g(s_n)$ is defined as: 
$$g(s_n)=\sum_{i=1} ^{n} c(s_{i-1},a_i,s_i)$$
Where $s_i$ is the [[#State|state]] reached after performing the [[#Action|action]] $a_i$ from [[#State|state]] $s_{i-1}$.
#### Example:
- In a grid-based pathfinding problem, if moving from one cell to an adjacent cell has a cost of 1, and the agent moves from the initial state `(0, 0)` to the goal state `(2, 2)` by moving right twice and up twice, the path cost would be $4$.
- In a weighted graph, where each edge has a different cost, the path cost is the sum of the weights of the edges in the path from the start node to the goal node. If the agent follows a path with edges of weights 2, 3, and 5, the path cost would be $10$.
#### Pseudocode:
```plaintext
// Path Cost
FUNCTION PathCost(actions)
	total_cost ← 0
	FOR each action IN actions
	    total_cost ← total_cost + cost of action
	END FOR
	
	RETURN total_cost
END FUNCTION
```

---
### 2.2.5 Transition Model/Function
A description of what [[#State|state]] results from performing any applicable [[#Action|action]] in any [[#State|state.]] An example of transition function can be the transition function for a [[Automata and Languages Definitions#Nondeterministic Finite Automata|NFA]].

![[Automata and Languages Definitions#Nondeterministic Finite Automata#$\delta Q \times \Sigma_\epsilon \rightarrow \mathcal{P}(Q)$ Is the transition function]]

#### Formal Definition
Given the set of [[#State|states]] $S$, the set of [[#Action|actions]] $A$ we have that 
$$\delta: S \times A \rightarrow S$$
#### Examples:
- In a grid world, if the agent is at (2, 2) and performs the action "Move North," the transition model might say the agent moves to (2, 3). If there’s a wall to the north, the transition model might keep the agent at (2, 2).
- If $s=(2,2)$ and $a = \text{"Move North"}$ then $\delta((2, 2), \text{"Move North"}) = (2, 3)$ (assuming no obstacles).
#### Pseudocode:
```plaintext
// Transition Model
FUNCTION TransitionModel(s, a)
	s_prime ← result of applying action a in state s
	RETURN s_prime
END FUNCTION
```

## 2.3 Search Algorithms
### 2.3.1 Informed Search
Informed search, also known as heuristic search, is a type of search strategy that uses problem-specific knowledge, typically in the form of heuristics, to guide the search process more efficiently toward the goal. This approach can significantly reduce the search space and lead to faster solutions compared to [[#2.3.2 Uninformed Search|uninformed search]] strategies.
#### Common Informed Search Algorithms
##### Greedy Best-First Search
![[#1.2.1.7 Greedy Best-First Search (GBFS)]]
##### A* Search
![[#1.2.1.1 A* Search]]

### 2.3.2 Uninformed Search
Uninformed search, also known as blind search, is a type of search strategy that explores the search space without any additional information about the goal's location beyond the problem's definition. These algorithms only use the information available in the problem definition, such as the [[#2.1.5 State State|states]], [[#2.1.1 Action (Data Structure)|actions]], and [[#2.2.5 Transition Model/Function|transition model]], to guide the search process.
#### Common Uninformed Search Algorithms

##### Breadth-First Search (BFS)
 ![[#1.2.1.3 Breadth-First Search (BFS)]] 
##### Depth-First Search (DFS) 
 ![[#1.2.1.4 Depth-First Search (DFS)|Depth-First Search (DFS)]]
##### Uniform-Cost Search (UCS) 
![[#1.2.1.8 Uniform-Cost Search (UCS)|Uniform-Cost Search (UCS)]]
#### Example:
- In a maze-solving problem, a breadth-first search would explore all possible paths one step at a time, ensuring that the first solution found is the shortest in terms of the number of steps.


### 2.3.3 Adversarial Search
Adversarial search refers to a type of problem-solving in AI where multiple agents, typically two, are competing against each other, and the outcome depends on the actions of all participants. This is common in zero-sum games, where one player's gain is another player's loss, such as in chess, checkers, and tic-tac-toe. The goal of adversarial search is to find the best strategy for a player, assuming that the opponent is also playing optimally.

#### Formal Definition
An adversarial search problem can be defined by the tuple $(S, A, \delta, P, U, s_0, T)$, where:
- **$S$** is the set of all possible [[#State|states]].
- **$A$** is the set of all possible [[#Action|actions]].
- **$\delta: S \times A \rightarrow S$** is the transition function that describes the result of applying an action to a state.
- **$P: S \rightarrow { \text{Player 1}, \text{Player 2}, \dots }$** is the function determining which player’s turn it is.
- **$U: S \rightarrow \mathbb{R}$** is the utility function that assigns a value to terminal states, representing the outcome for the players (e.g., win, lose, or draw).
- **$s_0 \in S$** is the [[#Initial State|initial state]] of the game.
- **$T: S \rightarrow \text{bool}$** is the test to determine if the state is terminal, meaning the game has ended.
#### Objective
The objective in adversarial search is to determine a sequence of actions that leads to an optimal outcome for the player considering the possible responses of the opponent.
#### Key Components:
- **Minimax Algorithm**: The [[#1.2.3.3 Minimax Algorithm|Minimax algorithm]] is a foundational method used in adversarial search to determine the optimal move by considering all possible moves by both the player and the opponent. It recursively evaluates the game tree to find the move that maximizes the player's minimum gain, hence the name "Minimax."
- **Alpha-Beta Pruning**: [[#1.2.3.1 Alpha-Beta Pruning|Alpha-Beta Pruning]] is an optimization technique used to enhance the efficiency of the Minimax algorithm. It prunes branches of the game tree that do not need to be explored because they cannot influence the final decision, thereby reducing the number of nodes that need to be evaluated.
- **Optimal Solution**: In the context of adversarial search, an [[#1.3.2 Optimal Solution|optimal solution]] is the strategy or sequence of moves that leads to the best possible outcome for a player, assuming perfect play by both sides. The Minimax algorithm is designed to find this optimal solution by evaluating all possible game states.

#### Examples:
- **Chess**: Using adversarial search, an AI can determine the best possible move in a chess game by considering all potential responses from the opponent.
- [[Tic Tac Toe Understanding Adversarial Search and the Minimax AlgorithmUntitled|Tic-Tac-Toe]]: Even in simpler games like tic-tac-toe, adversarial search helps in determining a strategy that guarantees a win or a draw.

In adversarial search, finding an optimal solution involves not just minimizing your losses but also anticipating and countering your opponent's best moves. This is why the concepts of Minimax and Alpha-Beta Pruning are so integral—they enable the AI to efficiently find the best strategy by exploring the most relevant parts of the game tree.

---
### 2.3.4 Theorem Proving as a Search Problem
Theorem proving can be modeled as a search problem where the goal is to find a proof of a statement (A) given a set of axioms or known facts (the knowledge base, KB). The process involves exploring the space of possible inferences to determine whether the statement can be logically derived from the knowledge base.

#### Search Problem Components

- **Initial State (Starting Knowledge Base):** The initial state is the knowledge base (KB), which contains the axioms and facts. For example, consider the knowledge base:
  $$
  \text{KB} = (A \lor B) \land (\neg B \lor C) \land (\neg C)
  $$

- **Actions (Inference Rules):** The actions are the inference rules that can be applied to the knowledge base to derive new information. Common inference rules include [[#3.7.13 Unit Resolution|unit Resolution]], which allows for simplifying clauses by eliminating complementary literals.

- **Transition Model/Function (New Knowledge Base After Inference):** The transition model describes how the knowledge base changes after applying an inference rule. For example, resolving the clauses $(\neg B \lor C)$ and $(\neg C)$ in the KB leads to the new clause $\neg B$, updating the knowledge base to:
  $$
  \text{KB} = (A \lor B) \land \neg B
  $$

- **Goal Test (Check Statement to Prove):** The goal test checks whether the desired statement $A$ is entailed by the current knowledge base. In our example, we want to prove $A$.

- **Path Cost Function (Number of Steps in Proof):** The path cost function measures the number of inference steps required to reach the proof of $A$. The fewer steps taken, the more efficient the proof.

#### Example: Theorem Proving by Contradiction

To prove $A$ using **proof by contradiction** [[#3.6 Entailment in Propositional Logic|Entailment in Propositional Logic]], we assume the negation of $A$ and attempt to derive a contradiction.

1. **Assume a Contradiction:** Add the negation of $A$ to the knowledge base:
   $$
   \text{KB} \models \neg A
   $$
   Now, the knowledge base is:
   $$
   \text{KB} = (A \lor B) \land (\neg B \lor C) \land (\neg C) \land \neg A
   $$

2. **Apply Inference Rules:** Use [[#3.7.13 Unit Resolution|unit Resolution]] to simplify the knowledge base:
   - Resolve $(\neg B \lor C)$ with $(\neg C)$ to get $\neg B$.
   - Resolve $(A \lor B)$ with $\neg B$ to get $A$.

3. **Check for Contradiction:** The derived clause $A$ contradicts $\neg A$ (which was added earlier), leading to a contradiction. Therefore, $A$ is proven to be true.

4. **Path Cost:** In this example, two inference steps were taken to prove $A$, so the path cost is 2.

#### Pseudocode

```plaintext
FUNCTION TheoremProvingByContradiction(KB, A) -> Boolean
    // Add the negation of A to the knowledge base
    KB.Add(Negation(A))
    
    REPEAT UNTIL no new clauses can be derived:
        SELECT pair of clauses with complementary literals
        RESOLVENT ← ResolveClauses(pair)
        
        IF RESOLVENT is the empty clause THEN
            RETURN True // Contradiction found, A is proven
        END IF
        
        ADD RESOLVENT to KB
    END REPEAT
    
    RETURN False // No contradiction found, A is not proven
END FUNCTION
```
# 3. Propositional Logic
Propositional logic, also known as propositional calculus or sentential logic, is a branch of logic that deals with propositions—statements that are either true or false. It forms the foundation for more complex logical systems and is widely used in fields like mathematics, computer science, and artificial intelligence for reasoning and knowledge representation.

## 3.1 Sentences in Propositional Logic
In propositional logic, a **sentence** (also called a proposition) is a declarative statement that can be either true or false, but not both. Sentences are the basic building blocks of propositional logic, and they represent assertions about the world.

### 3.1.1 Assertions about the World
A sentence in propositional logic represents an assertion about the state of the world. For example, the sentence "It is raining" asserts the fact that it is raining. These assertions can be combined and manipulated using logical connectives to form more complex statements.

#### Example of Simple Sentences:
- **P**: "It is raining."
- **Q**: "The ground is wet."
- An example sentence could be: "If it is raining, then the ground is wet," represented as $P \rightarrow Q$.

#### Role in Knowledge-Based Systems:
Sentences are fundamental components in knowledge-based systems, as they represent the facts and rules that an agent uses to make decisions and draw conclusions. By combining multiple sentences and applying logical inference, an agent can derive new knowledge or validate existing information, ultimately leading to intelligent decision-making.

## 3.2 Logical Connectives

Propositional logic uses several basic logical connectives to combine sentences into more complex propositions. Below are the main logical connectives, their meanings, and truth tables.

### 3.2.1 Negation (¬)
- **Description**: The negation of a sentence is true if the sentence is false, and false if the sentence is true.
- **Example**: If $P$ is "It is raining," then $\neg P$ is "It is not raining."

| **P** | **$\neg P$** |
| ----- | ------------ |
| T     | F            |
| F     | T            |
### 3.2.2 Conjunction (∧)
- **Description**: The conjunction of two sentences is true if both sentences are true.
- **Example**: $P \land Q$ is true if both "It is raining" and "The ground is wet" are true.

| **P** | **Q** | **$P \land Q$** |
| ----- | ----- | --------------- |
| T     | T     | T               |
| T     | F     | F               |
| F     | T     | F               |
| F     | F     | F               |

### 3.2.3 Disjunction (∨)
- **Description**: The disjunction of two sentences is true if at least one of the sentences is true.
- **Example**: $P \lor Q$ is true if either "It is raining" or "The ground is wet" is true (or both).

| **P** | **Q** | **$P \lor Q$** |
| ----- | ----- | -------------- |
| T     | T     | T              |
| T     | F     | T              |
| F     | T     | T              |
| F     | F     | F              |

### 3.2.4 Implication (→)
- **Description**: The implication represents a conditional statement where the first sentence (antecedent) implies the second sentence (consequent). It is false only when the antecedent is true and the consequent is false.
- **Example**: $P \rightarrow Q$ is true unless "It is raining" is true and "The ground is wet" is false.

| **P** | **Q** | **$P \rightarrow Q$** |
| ----- | ----- | --------------------- |
| T     | T     | T                     |
| T     | F     | F                     |
| F     | T     | T                     |
| F     | F     | T                     |

### 3.2.5 Biconditional (↔)
- **Description**: The biconditional is true if both sentences have the same truth value.
- **Example**: $P \leftrightarrow Q$ is true if "It is raining" and "The ground is wet" are both true or both false.

| **P** | **Q** | **$P \leftrightarrow Q$** |
| ----- | ----- | ------------------------- |
| T     | T     | T                         |
| T     | F     | F                         |
| F     | T     | F                         |
| F     | F     | T                         |
## 3.3 Logical Equivalences
Logical equivalences are rules that show when two propositions are logically equivalent, meaning they have the same truth value in every possible scenario. Some common logical equivalences include:

- **De Morgan's Laws**:
  - $\neg (P \land Q) \equiv \neg P \lor \neg Q$
  - $\neg (P \lor Q) \equiv \neg P \land \neg Q$
  
- **Implication Equivalence**:
  - $P \rightarrow Q \equiv \neg P \lor Q$
  
- **Biconditional Equivalence**:
  - $P \leftrightarrow Q \equiv (P \rightarrow Q) \land (Q \rightarrow P)$

These equivalences are used to simplify complex logical expressions and to prove logical relationships.

## 3.4 Truth Tables
Truth tables are used to define the truth values of complex sentences based on the truth values of their components. They are a key tool for understanding the behavior of logical connectives and for performing logical reasoning.

### Example of Truth Table for Biconditional ($P \leftrightarrow Q$)

| **P** | **Q** | **$P \leftrightarrow Q$** |
| ----- | ----- | ------------------------- |
| T     | T     | T                         |
| T     | F     | F                         |
| F     | T     | F                         |
| F     | F     | T                         |
This table shows that $P \leftrightarrow Q$ is true when both $P$ and $Q$ have the same truth value (both true or both false).

## 3.5 Model in Propositional Logic
In propositional logic, a **model** is an assignment of truth values to the propositional variables (sentences). It represents a possible state of the world where each proposition is either true or false.

#### Definition of a Model
A model for a set of propositions is a specific assignment of truth values to all propositional variables in that set. For example, consider the propositions $P$, $Q$, and $R$. A model might assign the following truth values:

- $P = \text{True}$
- $Q = \text{False}$
- $R = \text{True}$

This specific assignment is one possible model for the set $\{P, Q, R\}$.

#### Role of Models in Propositional Logic
Models are used to evaluate the truth of complex propositions formed by combining simpler propositions with logical connectives. By checking all possible models, we can determine whether a proposition is true in all models (a tautology), false in all models (a contradiction), or true in some but not all models (a contingency).

####  Example
Consider the following proposition:
$$ (P \land Q) \rightarrow R $$
To evaluate this proposition, we can examine all possible models for $P$, $Q$, and $R$:

| **P** | **Q** | **R** | **$P \land Q$** | **$(P \land Q) \rightarrow R$** |
|:----:|:----:|:----:|:---------------:|:--------------------------:|
|  T   |  T   |  T   |        T        |              T             |
|  T   |  T   |  F   |        T        |              F             |
|  T   |  F   |  T   |        F        |              T             |
|  T   |  F   |  F   |        F        |              T             |
|  F   |  T   |  T   |        F        |              T             |
|  F   |  T   |  F   |        F        |              T             |
|  F   |  F   |  T   |        F        |              T             |
|  F   |  F   |  F   |        F        |              T             |
This table shows that the proposition $(P \land Q) \rightarrow R$ is false only in the model where $P$ and $Q$ are true, and $R$ is false. In all other models, the proposition is true.

#### Importance of Models in Knowledge Representation
In knowledge-based systems, models are crucial because they allow the system to reason about different possible states of the world. By considering all possible models, the system can determine whether a given proposition or set of propositions holds under various conditions, thereby enabling it to make informed decisions and draw valid conclusions.


## 3.6 Entailment in Propositional Logic
**Entailment** is a fundamental concept in logic that refers to the relationship between sentences where one sentence logically follows from one or more other sentences. If a set of sentences (premises) entails a particular conclusion, then whenever the premises are true, the conclusion must also be true.

### Formal Definition:
Given a set of sentences $\Gamma$ and a sentence $\varphi$, we say that $\Gamma$ **entails** $\varphi$ (written as $\Gamma \models \varphi$) if in every model where all the sentences in $\Gamma$ are true, $\varphi$ is also true.

### Example:
- Suppose $\Gamma = \{P \rightarrow Q, P\}$. If $\Gamma$ is true, then $Q$ must also be true. Therefore, $\Gamma \models Q$.

### Role in Logical Reasoning:
Entailment is central to logical reasoning because it allows us to derive new truths from known truths. In a knowledge-based system, entailment is used to infer new facts from existing knowledge, enabling intelligent decision-making and problem-solving.

### Pseudocode for Entailment Check:
```plaintext
// Function to check if a set of sentences Γ entails a sentence φ
FUNCTION CheckEntailment(Γ, φ) -> Boolean
    FOR each model m in all possible models:
        IF m satisfies Γ THEN
            IF m does not satisfy φ THEN
                RETURN False
        END IF
    END FOR
    RETURN True
END FUNCTION
```

### Understanding Entailment in Propositional Logic (more details)
**Entailment** in propositional logic is about the logical relationship between a set of propositions (sentences) and a conclusion that can be drawn from them. It expresses a kind of "guarantee" that if certain propositions are true, then another proposition must also be true.

### Key Concepts:

1. **Set of Sentences ($\Gamma$):**
    - Imagine you have a group of statements or sentences that you know to be true. For example:
        - $P \rightarrow Q$ (If it is raining, then the ground is wet)
        - $P$ (It is raining)
    - This group of sentences is collectively called $ \Gamma $.
2. **Entailment ($\models$):**
    - Entailment is represented by the symbol $\models$.
    - We say that $\Gamma$ **entails** a conclusion $\varphi$ if, whenever all the sentences in $\Gamma$ are true, the conclusion $\varphi$ must also be true.
    - For example, if we know that "If it is raining, then the ground is wet" ($P \rightarrow Q$) and "It is raining" ($P$), we can **entail** that "The ground is wet" ($Q$).
3. **Logical Consequence:**
    - The sentence $\varphi$ is called a **logical consequence** of the set $\Gamma$. This means that $\varphi$ follows logically from the statements in $\Gamma$.
4. [[#3.5 Model in Propositional Logic|Models:]]
    - A **model** in logic is a specific assignment of truth values (true or false) to the propositions involved.
    - For entailment to hold, $\varphi$ must be true in **every model** where all the sentences in $ \Gamma $ are true.

### Example Walkthrough:

Let’s take the following sentences:
- $P \rightarrow Q$: "If it is raining, then the ground is wet."
- $P$: "It is raining."

Now, if these two sentences are both true, what can we conclude about $Q$ ("The ground is wet")?
- **Entailment** tells us that $Q$ must also be true. This is because, according to the rules of logic, if $P \rightarrow Q$ is true and $P$ is true, then $Q$ must also be true. Thus, we say $\{P \rightarrow Q, P\} \models Q$.

In simpler terms, entailment is like a guarantee: if certain conditions (the premises) are true, then the conclusion must necessarily be true.

### Why Entailment Matters:
In reasoning, particularly in fields like artificial intelligence and mathematics, entailment is crucial because it allows us to derive new knowledge from what we already know. By understanding and using entailment, we can make logical deductions, solve problems, and create systems that can think logically and make decisions.

For example, in a knowledge-based system, if an AI knows a set of rules and facts (like $P \rightarrow Q$ and $P$), it can automatically infer new facts (like $Q$) without needing to be explicitly told every possible fact.

## 3.7 Inference
Inference is the process of deriving logical conclusions from a set of premises or known facts. It plays a crucial role in logical reasoning, allowing us to deduce new information from what we already know. In propositional logic, inference rules are applied to propositions to derive valid conclusions.

### 3.7.1 Absorption
**Absorption** simplifies expressions by absorbing redundant terms, reducing the logical expression without altering its truth value.

- **Given**: $P \rightarrow Q$.
- **Conclusion**: $P \rightarrow (P \land Q)$.

Alternatively:

- **Given**: $P \lor (P \land Q)$.
- **Conclusion**: $P$.

#### Absorption Inference Form
$$
\begin{array}{c}
P \rightarrow Q \\
\hline
P \rightarrow (P \land Q)
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \rightarrow Q) \land P$:
   - Recognize $P \rightarrow Q$ implies $Q$ when $P$ is true.
   - Combine $P$ with $Q$: $(P \land Q)$.
   - **Final Simplification**: $P \land Q$.

2. Simplify $P \rightarrow (P \land Q)$:
   - Absorb $Q$ into the implication without changing the truth value of $P \rightarrow Q$.
   - **Final Simplification**: $P \rightarrow (P \land Q)$.

3. Simplify $P \lor (P \land Q)$:
   - Since $P$ is already present, the expression simplifies to just $P$.
   - **Final Simplification**: $P$.

---
### 3.7.2 And Elimination
**And Elimination** allows us to infer individual statements from a conjunction.

- **Given**: $P \land Q$ (Both $P$ and $Q$ are true).
- **Conclusion**: $P$ (Therefore, $P$) and separately, $Q$ (Therefore, $Q$).

#### And Elimination Inference Form
$$
\begin{array}{c}
P \land Q \\
\hline
P \\
Q
\end{array}
$$

**Simplifying Examples**:
1. Simplify $P \land (Q \land R)$:
   - Break $Q \land R$ into $Q$ and $R$.
   - Conclude $P$ from the first part and then infer $Q$ and $R$ separately.
   - **Final Simplification**: $P, Q, R$.

2. Simplify $(P \land Q) \land (R \land S)$:
   - Break down the conjunction: first simplify to $P, Q$, then $R, S$.
   - **Final Simplification**: $P, Q, R, S$.

3. Simplify $(P \land Q) \rightarrow R$:
   - Recognize $P \land Q$ as a single combined premise to conclude $R$.
   - **Final Simplification**: $R$.

---
### 3.7.3 Biconditional (Bi-implication) Transformation
**Biconditional Transformation** allows us to rewrite a biconditional ($P \leftrightarrow Q$) as two implications combined.

- **Given**: $P \leftrightarrow Q$ ($P$ if and only if $Q$).
- **Transformation**: $(P \rightarrow Q) \land (Q \rightarrow P)$.

#### Biconditional Transformation Inference Form
$$
\begin{array}{c}
P \leftrightarrow Q \\
\hline
(P \rightarrow Q) \land (Q \rightarrow P)
\end{array}
$$

**Simplifying Examples**:
1. Simplify $P \leftrightarrow Q$:
   - Rewrite as $(P \rightarrow Q) \land (Q \rightarrow P)$.
   - **Final Simplification**: $(P \rightarrow Q) \land (Q \rightarrow P)$.

2. Simplify $(P \leftrightarrow Q) \leftrightarrow R$:
   - Rewrite $(P \leftrightarrow Q)$ as $(P \rightarrow Q) \land (Q \rightarrow P)$ and combine with $R$.
   - **Final Simplification**: $(P \rightarrow Q) \land (Q \rightarrow P) \leftrightarrow R$.

3. Simplify $(P \leftrightarrow Q) \lor R$:
   - Expand $(P \leftrightarrow Q)$ and then combine with $R$.
   - **Final Simplification**: $(P \rightarrow Q) \land (Q \rightarrow P) \lor R$.

---
### 3.7.4 Conjunction
**Conjunction** allows the combination of two statements into a single conjunction.

- **Given**: $P$.
- **Given**: $Q$.
- **Conclusion**: $P \land Q$.

#### Conjunction Inference Form
$$
\begin{array}{c}
P \\
Q \\
\hline
P \land Q
\end{array}
$$

**Simplifying Examples**:
1. Combine $P$, $Q$, and $R$:
   - Combine them together: $P \land Q \land R$.
   - **Final Simplification**: $P \land Q \land R$.

2. Simplify $P \land (Q \lor R)$:
   - Keep the terms together without additional manipulation.
   - **Final Simplification**: $P \land (Q \lor R)$.

3. Combine $(P \lor Q)$ and $(R \rightarrow S)$:
   - Combine as $(P \lor Q) \land (R \rightarrow S)$ directly.
   - **Final Simplification**: $(P \lor Q) \land (R \rightarrow S)$.

---
### 3.7.5 Constructive Dilemma
**Constructive Dilemma** combines two conditional statements and a disjunction, allowing for a combined conclusion.

- **Given**: $(P \rightarrow Q) \land (R \rightarrow S)$.
- **Given**: $P \lor R$.
- **Conclusion**: $Q \lor S$.

#### Constructive Dilemma Inference Form
$$
\begin{array}{c}
(P \rightarrow Q) \land (R \rightarrow S) \\
P \lor R \\
\hline
Q \lor S
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \rightarrow Q) \land (R \rightarrow S)$:
   - Directly infer from the given structure: $(Q \lor S)$.
   - **Final Simplification**: $Q \lor S$.

2. Simplify $(P \rightarrow Q) \land R$:
   - Recognize the implication: infer $Q$ from $P$ and keep $R$ separate.
   - **Final Simplification**: $Q \land R$.

3. Simplify $(P \rightarrow Q) \lor (R \rightarrow S)$:
   - Recognize each implication and infer $Q$ and $S$ independently.
   - **Final Simplification**: $Q \lor S$.

---
### 3.7.6 De Morgan’s Laws
**De Morgan’s Laws** provide rules for the negation of conjunctions and disjunctions.

- **Given**: $\neg (P \land Q)$.
- **Conclusion**: $\neg P \lor \neg Q$.

or

- **Given**: $\neg (P \lor Q)$.
- **Conclusion**: $\neg P \land \neg Q$.

#### De Morgan’s Laws Inference Form
1.
$$
\begin{array}{c}
\neg (P \land Q) \\
\hline
\neg P \lor \neg Q
\end{array}
$$

2.
$$
\begin{array}{c}
\neg (P \lor Q) \\
\hline
\neg P \land \neg Q
\end{array}
$$

**Simplifying Examples**:
1. Simplify $\neg (P \land Q) \lor R$:
   - Apply De Morgan’s: $\neg P \lor \neg Q$.
   - Combine with $R$: $\neg P \lor \neg Q \lor R$.
   - **Final Simplification**: $\neg P \lor \neg Q \lor R$.

2. Simplify $\neg (P \lor (Q \land R))$:
   - Apply De Morgan’s inside: rewrite as $\neg P \land \neg Q \lor \neg R$.
   - **Final Simplification**: $\neg P \land (\neg Q \lor \neg R)$.

3. Simplify $(\neg P \land \neg Q) \lor S$:
   - Keep terms separated.
   - **Final Simplification**: $(\neg P \land \neg Q) \lor S$.

---
### 3.7.7 Disjunctive Syllogism
**Disjunctive Syllogism** allows one to eliminate a disjunct when the negation of the other is known.

- **Given**: $P \lor Q$.
- **Given**: $\neg P$.
- **Conclusion**: $Q$.

#### Disjunctive Syllogism Inference Form
$$
\begin{array}{c}
P \lor Q \\
\neg P \\
\hline
Q
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \lor Q) \land \neg P$:
   - Apply negation: since $\neg P$, infer $Q$.
   - **Final Simplification**: $Q$.

2. Simplify $(P \lor Q) \lor R$:
   - Recognize $Q$ independently after $P$ is eliminated.
   - **Final Simplification**: $Q \lor R$.

3. Simplify $(P \lor Q) \rightarrow R$:
   - Use the remaining disjunction to conclude $R$ when $P$ is negated.
   - **Final Simplification**: $Q \rightarrow R$.

---
### 3.7.8 Hypothetical Syllogism
**Hypothetical Syllogism** allows chaining implications together.

- **Given**: $P \rightarrow Q$.
- **Given**: $Q \rightarrow R$.
- **Conclusion**: $P \rightarrow R$.

#### Hypothetical Syllogism Inference Form
$$
\begin{array}{c}
P \rightarrow Q \\
Q \rightarrow R \\
\hline
P \rightarrow R
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \rightarrow Q) \rightarrow R$:
   - Recognize the direct chain from $P$ to $R$.
   - **Final Simplification**: $P \rightarrow R$.

2. Simplify $P \rightarrow (Q \rightarrow R)$:
   - Use $Q$ to infer $R$, linking $P$ directly to $R$.
   - **Final Simplification**: $P \rightarrow R$.

3. Simplify $P \rightarrow (R \rightarrow S)$:
   - Chain implications directly from $P$ to $S$.
   - **Final Simplification**: $P \rightarrow S$.

---
### 3.7.9 Implication Transformation
**Implication Transformation** allows us to rewrite an implication as a disjunction.

- **Given**: $P \rightarrow Q$.
- **Transformation**: $\neg P \lor Q$.

#### Implication Transformation Inference Form
$$
\begin{array}{c}
P \rightarrow Q \\
\hline
\neg P \lor Q
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \rightarrow Q) \rightarrow R$:
   - Transform $(P \rightarrow Q)$ into $\neg P \lor Q$ and combine with $R$.
   - **Final Simplification**: $(\neg P \lor Q) \rightarrow R$.

2. Simplify $(P \rightarrow (Q \lor R))$:
   - Rewrite inside as $\neg P \lor (Q \lor R)$.
   - **Final Simplification**: $\neg P \lor Q \lor R$.

3. Simplify $P \rightarrow (Q \rightarrow S)$:
   - Separate implications into disjunctive forms.
   - **Final Simplification**: $\neg P \lor Q \lor S$.

---
### 3.7.10 Modus Ponens
**Modus Ponens** applies when you have an implication and its premise.

- **Given**: $P \rightarrow Q$.
- **Given**: $P$.
- **Conclusion**: $Q$.

#### Modus Ponens Inference Form
$$
\begin{array}{c}
P \rightarrow Q \\
P \\
\hline
Q
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \rightarrow Q) \land P$:
   - Recognize that $P$ satisfies the condition, leading directly to $Q$.
   - **Final Simplification**: $Q$.

2. Simplify $P \rightarrow (Q \land R)$:
   - Apply $P$, leading to the combined conclusion of $Q \land R$.
   - **Final Simplification**: $Q \land R$.

3. Simplify $P \rightarrow (Q \rightarrow S)$:
   - Chain the implications step-by-step to conclude $S$.
   - **Final Simplification**: $S$.

---
### 3.7.11 Modus Tollens
**Modus Tollens** concludes the negation of a premise from the negation of its conclusion.

- **Given**: $P \rightarrow Q$.
- **Given**: $\neg Q$.
- **Conclusion**: $\neg P$.

#### Modus Tollens Inference Form
$$
\begin{array}{c}
P \rightarrow Q \\
\neg Q \\
\hline
\neg P
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \rightarrow Q) \land \neg Q$:
   - Recognize that $\neg Q$ directly negates $P$.
   - **Final Simplification**: $\neg P$.

2. Simplify $P \rightarrow (\neg Q \rightarrow S)$:
   - Utilize the negated condition and simplify further.
   - **Final Simplification**: $\neg P \rightarrow S$.

3. Simplify $(P \rightarrow \neg Q) \rightarrow S$:
   - Chain implications leading to $S$.
   - **Final Simplification**: $\neg P \rightarrow S$.

---
### 3.7.12 Or Elimination
**Or Elimination** infers a conclusion from a disjunction when one disjunct is negated.

- **Given**: $P \lor Q$.
- **Given**: $\neg P$.
- **Conclusion**: $Q$.

#### Or Elimination Inference Form
$$
\begin{array}{c}
P \lor Q \\
\neg P \\
\hline
Q
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \lor Q) \land (\neg P \land \neg R)$:
   - Eliminate $P$ using $\neg P$, leaving $Q$ and $\neg R$.
   - **Final Simplification**: $Q \land \neg R$.

2. Simplify $(P \lor Q) \rightarrow R$:
   - Recognize that $P$ is eliminated, allowing $Q \rightarrow R$.
   - **Final Simplification**: $Q \rightarrow R$.

3. Simplify $P \lor (\neg Q \land R)$:
   - Eliminate $P$, inferring directly from $Q$ and $R$.
   - **Final Simplification**: $Q \lor R$.

---
### 3.7.13 Unit Resolution
**Unit Resolution** resolves clauses containing complementary literals.

- **Given**: $P \lor Q_1 \lor \ldots$.
- **Given**: $\neg P \lor R_1 \lor \ldots$.
- **Conclusion**: $Q_1 \lor R_1 \lor \ldots$.

#### Unit Resolution Inference Form
$$
\begin{array}{c}
P \lor Q_1 \lor Q_2 \lor \ldots \\
\neg P \lor R_1 \lor R_2 \lor \ldots \\
\hline
Q_1 \lor Q_2 \lor \ldots \lor R_1 \lor R_2 \lor \ldots
\end{array}
$$

**Simplifying Examples**:
1. Simplify $(P \lor Q) \land (\neg P \lor R)$:
   - Resolve $P$ with $\neg P$, leaving $Q$ and $R$.
   - **Final Simplification**: $Q \lor R$.

2. Simplify $(P \lor (Q \land R))$:
   - Resolve $P$, considering $Q \land R$ as an independent clause.
   - **Final Simplification**: $Q \lor R$.

3. Simplify $(P \lor \neg Q) \lor R$:
   - Combine independently, eliminating $P$ using $\neg P$ when available.
   - **Final Simplification**: $\neg Q \lor R$.


## 3.8 Conjunctive Normal Form (CNF)
**Conjunctive Normal Form (CNF)** is a standardized format in propositional logic used to express logical formulas as a conjunction of disjunctions of literals. CNF plays a crucial role in logical reasoning, particularly in automated theorem proving, satisfiability testing, and inference methods like resolution. Converting formulas into CNF simplifies their manipulation and analysis, making CNF a cornerstone of logic-based systems in artificial intelligence.

### 3.8.1 Definition of CNF
A formula is in Conjunctive Normal Form if it is expressed as a conjunction (AND) of clauses, where each clause is a disjunction (OR) of literals (variables or their negations). For example:
- $(P \lor Q) \land (\neg P \lor R)$ is in CNF.

### 3.8.2 Importance of CNF
CNF is essential in logical reasoning because it provides a uniform structure that simplifies the application of inference rules, particularly the resolution method. This format is required for many logic algorithms, including SAT solvers, which determine if a set of logical statements is satisfiable.

### 3.8.3 Converting a Formula to CNF
To apply inference methods like resolution, logical formulas must first be converted into CNF. The conversion process involves several steps to restructure the formula while preserving its logical equivalence:

1. **Eliminate Biconditionals and Implications**:
   - Replace biconditionals ($P \leftrightarrow Q$) with $(P \rightarrow Q) \land (Q \rightarrow P)$.
   - Replace implications ($P \rightarrow Q$) with $\neg P \lor Q$.

2. **Move Negations Inward** (Using De Morgan’s Laws):
   - Apply De Morgan’s Laws to push negations inside: convert $\neg (P \land Q)$ to $\neg P \lor \neg Q$ and $\neg (P \lor Q)$ to $\neg P \land \neg Q$.

3. **Standardize to Conjunctions and Disjunctions**:
   - Ensure that all remaining logical connectives inside the formula are standardized into ANDs and ORs.

4. **Distribute Disjunctions over Conjunctions**:
   - Use distribution rules to achieve a conjunction of disjunctions, e.g., convert $(P \land Q) \lor R$ into $(P \lor R) \land (Q \lor R)$.

5. **Simplify**:
   - Remove redundant literals and merge similar terms where possible to achieve the simplest CNF representation.

### 3.8.4 Example Conversion to CNF
**Example**: Convert the formula $(P \rightarrow Q) \land (\neg Q \rightarrow R)$ to CNF.

1. **Eliminate Implications**:
   - Convert implications to disjunctions: $(\neg P \lor Q) \land (Q \lor R)$.

2. **No Further Negations or Distributions Needed**:
   - The formula is already in the required structure without needing additional transformations.

3. **Final CNF Form**:
   - $(\neg P \lor Q) \land (Q \lor R)$.

### 3.8.5 Applications of CNF
- **Automated Reasoning**: CNF is essential in systems that perform logical inference, such as SAT solvers and theorem provers.
- **Resolution**: The resolution method, used in proof systems, relies on formulas being in CNF to systematically eliminate literals and derive conclusions.
- **Knowledge Representation**: In AI, CNF is often used to represent complex logical relationships in a standardized form, facilitating the application of logical rules.

### 3.8.6 Why CNF Matters
Converting logical statements to CNF ensures that they can be efficiently processed by algorithms that require a consistent format, making CNF a critical tool in the toolkit of logical reasoning. Understanding and using CNF enables the application of powerful inference methods, ensuring that complex logical problems can be tackled systematically.

## 3.9 Types of Inference
In the context of formal logic, different types of inference can be classified based on the nature of the reasoning and the strength of the conclusions they allow. Understanding these types is crucial for applying logical reasoning effectively in various contexts, including mathematics, computer science, and everyday decision-making.

### 3.9.1 Abductive Inference
**Abductive Inference** involves reasoning to the best explanation. It starts with an observation and seeks the simplest and most likely explanation for that observation. Abduction is often used when there is incomplete information.

- **Example**:
  - Observation: "The ground is wet."
  - Possible Explanation: "It must have rained."

- **Key Characteristics**:
  - The conclusion is not necessarily true but is a plausible explanation.
  - Used in diagnostic reasoning, hypothesis generation, and problem-solving.

---
### 3.9.2 Analogical Inference
**Analogical Inference** involves reasoning based on the similarities between two situations or objects. If two things are similar in some respects, it is inferred that they may be similar in other respects as well.

- **Example**:
  - Premise: "The heart pumps blood like a pump moves water."
  - Conclusion: "The heart functions like a pump."

- **Key Characteristics**:
  - Relies on observed similarities.
  - Useful for making predictions or understanding unfamiliar situations.

---
### 3.9.3 Causal Inference
**Causal Inference** involves reasoning about cause and effect relationships. It seeks to determine whether a particular factor is responsible for an observed outcome.

- **Example**:
  - Observation: "Smoking is correlated with lung cancer."
  - Causal Inference: "Smoking causes lung cancer."

- **Key Characteristics**:
  - Requires careful analysis to distinguish correlation from causation.
  - Used in scientific research, public health, and policy-making.

---
### 3.9.4 Counterfactual Inference
**Counterfactual Inference** involves reasoning about what would happen if a certain condition were different. It examines alternative scenarios that did not actually occur to understand causal relationships.

- **Example**:
  - Scenario: "If I had left the house earlier, I would not have missed the bus."
  
- **Key Characteristics**:
  - Explores hypothetical alternatives to reality.
  - Useful in decision analysis, planning, and understanding causal dynamics.

---
### 3.9.5 Defeasible Inference
**Defeasible Inference** involves reasoning that can be revised or defeated by new evidence. It allows for conclusions that are reasonable given the current information but can be overridden if new facts emerge.

- **Example**:
  - Initial Inference: "Birds can fly."
  - New Evidence: "Penguins are birds that cannot fly."

- **Key Characteristics**:
  - Conclusions are provisional and open to revision.
  - Common in legal reasoning, AI, and dynamic decision-making.

---
### 3.9.6 Deductive Inference
**Deductive Inference** involves reasoning from general premises to specific conclusions that must necessarily follow if the premises are true. Deductive reasoning is characterized by its certainty; the conclusion is logically entailed by the premises.

- **Example**:
  - Premises: "All humans are mortal. Socrates is a human."
  - Conclusion: "Socrates is mortal."
  
- **Key Characteristics**:
  - The truth of the premises guarantees the truth of the conclusion.
  - Often used in formal proofs, mathematics, and logical arguments.

---
### 3.9.7 Inference by Resolution
**Inference by Resolution** is a rule that combines two clauses containing complementary literals (a literal and its negation) to produce a new clause. This type of inference is extensively used in logic programming and automated reasoning systems, such as Prolog and SAT solvers.

- **Definition**:
  - Given two clauses, $C_1$ and $C_2$, where $C_1$ contains a literal $L$ and $C_2$ contains the negation $\neg L$, the resolution rule produces a new clause $C_3$ that includes all the literals from $C_1$ and $C_2$, except $L$ and $\neg L$.

- **Resolution Rule**:
  - If $C_1 = (P \lor Q)$ and $C_2 = (\neg P \lor R)$, then the resolvent $C_3 = (Q \lor R)$.

#### Resolution Inference Form
$$
\begin{array}{c}
P \lor Q \\
\neg P \lor R \\
\hline
Q \lor R
\end{array}
$$

#### Example of Inference by Resolution:
1. **Simplify** $(P \lor Q) \land (\neg P \lor R)$:-
   - **Step 1**: Convert to CNF (if not already in CNF).
   - **Step 2**: Identify complementary literals: $P$ in the first clause and $\neg P$ in the second clause.
   - **Step 3**: Apply the resolution rule by removing $P$ and $\neg P$.
   - **Step 3*4: Combine the remaining literals $Q$ and $R$.
   - **Final Simplification**: $Q \lor R$.

3. **Application in Automated Reasoning**:
   - In theorem proving, resolution is used iteratively to simplify clauses until a contradiction is found (an empty clause), proving the unsatisfiability of a set of clauses or to infer new information.

4. **Application in Prolog**:
   - Prolog uses resolution to solve queries by matching goals with rules in its knowledge base, using backtracking to find resolutions that satisfy the query.

#### Key Characteristics of Inference by Resolution
- **Conversion to CNF**: Essential for applying the resolution method, ensuring that the logical expressions are in a standardized, manageable form.
- **Completeness**: Resolution is complete for propositional and first-order logic, capable of deriving any logical consequence if the premises are sufficient.
- **Refutation-Based**: Often used in a refutation-based approach, where the negation of the desired conclusion is shown to lead to a contradiction, thus proving the original statement.
- **Efficiency**: Computational efficiency can be achieved when combined with strategies like unit propagation and clause learning in SAT solvers.
- **Usage in AI**: Widely used for reasoning under uncertainty, logic programming, and expert systems, enabling complex decision-making and problem-solving.
---
### 3.9.8 Inductive Inference
**Inductive Inference** involves reasoning from specific observations to broader generalizations. Unlike deductive reasoning, inductive reasoning does not guarantee the conclusion but instead suggests it with some level of probability.

- **Example**:
  - Observations: "The sun has risen every day in recorded history."
  - Conclusion: "The sun will rise tomorrow."

- **Key Characteristics**:
  - The conclusion is probable but not certain.
  - Commonly used in scientific reasoning and everyday decision-making.

---
### 3.9.9 Statistical Inference
**Statistical Inference** uses data and statistical methods to make predictions or generalizations about a population based on a sample. This type of inference quantifies uncertainty through probabilities.

- **Example**:
  - Data: "In a survey, 60% of respondents prefer product A over product B."
  - Conclusion: "It is likely that a majority of the general population prefers product A."

- **Key Characteristics**:
  - Involves probability and statistical analysis.
  - Widely used in data science, research, and decision-making under uncertainty.

# 4. Probability Theory

## 4.1 Basic Concepts of Probability

### 4.1.1 Sample Space

**Definition**: The sample space, denoted as $S$, is the set of all possible outcomes of a random experiment. It encompasses everything that could possibly happen when the experiment is conducted.

**Example**: For a fair six-sided die, the sample space is $S = \{1, 2, 3, 4, 5, 6\}$, representing all possible outcomes when rolling the die.

**Notation**: $S = \{s_1, s_2, \dots, s_n\}$, where each $s_i$ represents a possible outcome.

**Conceptual Insight**: In the context of AI and probability theory, the sample space represents all possible scenarios or "worlds" that the system might consider. Clearly defining the sample space is crucial to avoid ambiguities in probability calculations.

### 4.1.2 Events

**Definition**: An event is a subset of the sample space, representing one or more outcomes of interest. Events are what we assign probabilities to.

**Example**: Rolling an even number with a die can be considered an event, $E = \{2, 4, 6\}$. This event represents the outcomes where the die shows an even number.

**Types of Events**:
- **Simple Events**: Events with a single outcome. For example, rolling a 3 is a simple event.
- **Compound Events**: Events with multiple outcomes. For example, rolling an even number is a compound event.

**Property**: The sum of probabilities of all possible events in the sample space is 1.

### 4.1.3 Probability of an Event

**Definition**: The probability of an event $E$, denoted as $P(E)$, is a measure of the likelihood that $E$ will occur. It quantifies how "likely" an event is, given the defined sample space.

**Formula**: $P(E) = \frac{|E|}{|S|}$, where $|E|$ is the number of favorable outcomes, and $|S|$ is the total number of possible outcomes in the sample space.

**Example**: For a fair six-sided die, the probability of rolling an even number (event $E = \{2, 4, 6\}$) is calculated as:

$$
P(E) = \frac{|E|}{|S|} = \frac{3}{6} = 0.5
$$

**Properties**:
- $0 \leq P(E) \leq 1$: The probability of any event is between 0 and 1.
- $P(S) = 1$: The probability of the sample space itself is 1, meaning that something in the sample space must occur.
- $P(\emptyset) = 0$: The probability of the empty set (an impossible event) is 0.
- **Total Probability**: The sum of the probabilities of all simple events (outcomes) in the sample space is 1.

## 4.2 Conditional Probability and Independence

### 4.2.1 Conditional Probability

**Definition**: The probability of an event $A$ given that another event $B$ has occurred is called conditional probability, denoted $P(A|B)$. This measures how the probability of $A$ is affected by knowing that $B$ has happened.

**Formula**: $P(A|B) = \frac{P(A \cap B)}{P(B)}$, assuming $P(B) > 0$. This formula tells us how to adjust the probability of $A$ when $B$ is known to have occurred.

**Example**: Consider a deck of 52 cards. If we know a card drawn is a face card (event $B$), the probability of it being an ace (event $A$) changes. Normally, there are 4 aces in a deck, so $P(A) = \frac{4}{52}$. But given that the card is a face card (which includes 12 cards: 4 Jacks, 4 Queens, 4 Kings), the conditional probability is:

$$
P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{0}{12} = 0
$$

Thus, if a card is known to be a face card, the probability that it is an ace is 0.

### 4.2.2 Independent Events

**Definition**: Two events $A$ and $B$ are independent if the occurrence of one does not affect the probability of the other. This is a key concept when events do not influence each other.

**Formula**: $P(A \cap B) = P(A) \cdot P(B)$ if $A$ and $B$ are independent.

**Example**: Suppose you roll two fair six-sided dice. Let $A$ be the event that the first die shows a 4, and $B$ be the event that the second die shows a 4. The probability of each event is $P(A) = \frac{1}{6}$ and $P(B) = \frac{1}{6}$. Since the outcome of one die does not affect the other, the probability that both dice show a 4 is:

$$
P(A \cap B) = P(A) \cdot P(B) = \frac{1}{6} \cdot \frac{1}{6} = \frac{1}{36} \approx 0.0278
$$

### 4.2.3 Bayes' Rule

**Definition**: Bayes' Rule, also known as Bayes' Theorem, is a fundamental result in probability theory that describes how to update the probability of a hypothesis based on new evidence. It relates the conditional probability of a hypothesis given observed data to the likelihood of the data under the hypothesis and the prior probability of the hypothesis.

**Formula**:

$$
P(H|E) = \frac{P(E|H) \cdot P(H)}{P(E)}
$$

where:
- $P(H|E)$ is the **posterior probability**, or the probability of the hypothesis $H$ given the evidence $E$.
- $P(E|H)$ is the **likelihood**, or the probability of observing the evidence $E$ given that the hypothesis $H$ is true.
- $P(H)$ is the **prior probability** of the hypothesis before observing the evidence.
- $P(E)$ is the **marginal likelihood** or the total probability of observing the evidence under all possible hypotheses.

**Example**: Suppose a doctor is trying to diagnose a rare disease that affects 1 in 1000 people. There is a test for this disease that is 99% accurate, meaning that the probability of a positive test result given that a person has the disease is 0.99, and the probability of a positive test result given that a person does not have the disease is 0.01.

- Let $H$ represent the event that a person has the disease.
- Let $E$ represent the event that the test result is positive.

We want to find the probability that a person has the disease given that their test result is positive, i.e., $P(H|E)$.

First, we identify the components of Bayes' Rule:
- The prior probability $P(H)$ is 0.001 (since the disease is rare).
- The likelihood $P(E|H)$ is 0.99 (the test correctly identifies the disease).
- The marginal likelihood $P(E)$ can be calculated as:

$$
P(E) = P(E|H) \cdot P(H) + P(E|\neg H) \cdot P(\neg H)
$$

where $P(\neg H)$ is the probability that the person does not have the disease (0.999) and $P(E|\neg H)$ is the probability of a positive test result given the person does not have the disease (0.01). Therefore:

$$
P(E) = (0.99 \cdot 0.001) + (0.01 \cdot 0.999) = 0.00099 + 0.00999 = 0.01098
$$

Now, applying Bayes' Rule:

$$
P(H|E) = \frac{0.99 \cdot 0.001}{0.01098} \approx 0.0902
$$

So, even with a positive test result, the probability that the person actually has the disease is approximately 9.02%. This example illustrates how a rare condition combined with a positive test result still leads to a relatively low probability due to the rarity of the disease, demonstrating the importance of considering prior probabilities.

**Applications of Bayes' Rule**:
- **Medical Diagnosis**: Updating the probability of a disease based on symptoms and test results.
- **Spam Filtering**: Determining whether an email is spam based on the presence of certain words.
- **Machine Learning**: Naive Bayes classifiers use Bayes' Rule for classification tasks.
- **Decision-Making Under Uncertainty**: Making informed decisions by continuously updating the likelihood of outcomes based on new data.

**Importance in AI**: Bayes' Rule is fundamental in many AI systems, especially in areas like natural language processing, predictive analytics, and decision-making systems. It allows these systems to make better decisions by incorporating new data in a principled way.

## 4.3 Joint Probability and Joint Probability Distributions

### 4.3.1 Joint Probability

**Definition**: Joint probability refers to the probability of two (or more) events occurring simultaneously. If $A$ and $B$ are two events, the joint probability of $A$ and $B$ is denoted by $P(A \cap B)$ or simply $P(A, B)$.

**Formula**:

For independent events $A$ and $B$, the joint probability is calculated as:

$$
P(A \cap B) = P(A) \cdot P(B)
$$

For dependent events, where the occurrence of one affects the probability of the other, the joint probability is given by:

$$
P(A \cap B) = P(A|B) \cdot P(B) = P(B|A) \cdot P(A)
$$

**Example**: Consider two events: $A$ is the event that a randomly chosen person is female, and $B$ is the event that the person has brown hair. Suppose $P(A) = 0.51$ (51% of the population is female), and $P(B|A) = 0.4$ (40% of females have brown hair). The joint probability that a person is both female and has brown hair is:

$$
P(A \cap B) = P(A) \cdot P(B|A) = 0.51 \cdot 0.4 = 0.204
$$

This means that there's a 20.4% chance that a randomly selected person is both female and has brown hair.

### 4.3.2 Joint Probability Distribution

**Definition**: A joint probability distribution represents the probabilities of all possible combinations of outcomes for two or more random variables. For two discrete random variables $X$ and $Y$, the joint probability distribution is typically presented in the form of a table, where each cell contains the probability $P(X = x_i, Y = y_j)$.

For continuous random variables, the joint distribution is described by a joint probability density function (PDF), denoted as $f_{X,Y}(x, y)$, which gives the likelihood that $X$ is near $x$ and $Y$ is near $y$.

**Properties**:
1. **Non-negativity**: $P(X = x_i, Y = y_j) \geq 0$ for all $x_i$ and $y_j$.
2. **Normalization**: The sum of all joint probabilities for discrete variables (or the integral for continuous variables) must equal 1:

   For discrete variables:
   $$
   \sum_{i}\sum_{j} P(X = x_i, Y = y_j) = 1
   $$

   For continuous variables:
   $$ 
   \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dx \, dy = 1
   $$

**Example (Discrete)**: Consider two discrete random variables, $X$ (representing the outcome of a fair die roll) and $Y$ (representing the outcome of flipping a fair coin, where 0 is tails and 1 is heads). The joint probability distribution could be represented in a table as follows:

|   | $Y=0$ (Tails) | $Y=1$ (Heads) |
|---|---------------|---------------|
| $X=1$ | $\frac{1}{12}$ | $\frac{1}{12}$ |
| $X=2$ | $\frac{1}{12}$ | $\frac{1}{12}$ |
| $X=3$ | $\frac{1}{12}$ | $\frac{1}{12}$ |
| $X=4$ | $\frac{1}{12}$ | $\frac{1}{12}$ |
| $X=5$ | $\frac{1}{12}$ | $\frac{1}{12}$ |
| $X=6$ | $\frac{1}{12}$ | $\frac{1}{12}$ |

Here, each combination of $X$ and $Y$ has a probability of $\frac{1}{12}$ since the die roll and coin flip are independent, and there are 12 possible outcomes in total.

**Example (Continuous)**: For two continuous random variables $X$ and $Y$, their joint probability distribution could be given by a joint PDF, such as:

$$
f_{X,Y}(x, y) = \frac{1}{2\pi \sigma_X \sigma_Y \sqrt{1-\rho^2}} \exp\left(-\frac{1}{2(1-\rho^2)}\left[\left(\frac{x-\mu_X}{\sigma_X}\right)^2 - 2\rho\left(\frac{x-\mu_X}{\sigma_X}\right)\left(\frac{y-\mu_Y}{\sigma_Y}\right) + \left(\frac{y-\mu_Y}{\sigma_Y}\right)^2\right]\right)
$$

This formula represents the joint PDF of two normally distributed variables $X$ and $Y$ with means $\mu_X$ and $\mu_Y$, standard deviations $\sigma_X$ and $\sigma_Y$, and correlation $\rho$.

### 4.3.3 Marginal Probability Distribution

**Definition**: The marginal probability distribution gives the probabilities of a single random variable irrespective of the values of other variables. It is derived from the joint probability distribution by summing (or integrating) over the possible values of the other variable(s).

**Formula (Discrete)**:

For random variable $X$:

$$
P(X = x_i) = \sum_{j} P(X = x_i, Y = y_j)
$$

For random variable $Y$:

$$
P(Y = y_j) = \sum_{i} P(X = x_i, Y = y_j)
$$

**Formula (Continuous)**:

For random variable $X$:

$$
f_X(x) = \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dy
$$

For random variable $Y$:

$$
f_Y(y) = \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dx
$$

**Example**: Using the discrete joint probability table from earlier, the marginal probability of $X = 1$ is calculated as:

$$
P(X = 1) = P(X = 1, Y = 0) + P(X = 1, Y = 1) = \frac{1}{12} + \frac{1}{12} = \frac{1}{6}
$$

This marginal probability gives the likelihood of rolling a 1 on the die, regardless of the coin flip's outcome.

## 4.4 Fundamental Probability Laws and Rules

### 4.4.1 Law of Total Probability

**Definition**: The Law of Total Probability is a fundamental rule that provides a way to calculate the probability of an event based on its conditional probabilities with respect to a partition of the sample space. Essentially, it breaks down the probability of an event into contributions from different scenarios that cover all possibilities.

**Formula**:

$$
P(A) = \sum_{i} P(A|B_i) \cdot P(B_i)
$$

where $\{B_1, B_2, \dots, B_n\}$ is a partition of the sample space, meaning that the $B_i$ events are mutually exclusive and exhaustive.

**Example**: Suppose you want to find the probability that a randomly chosen student passed an exam ($A$), but you only know the probabilities for different study habits. Let $B_1$ be the event that the student studied, and $B_2$ be the event that the student did not study. Assume $P(A|B_1) = 0.9$, $P(A|B_2) = 0.2$, $P(B_1) = 0.7$, and $P(B_2) = 0.3$. Then:

$$
P(A) = P(A|B_1) \cdot P(B_1) + P(A|B_2) \cdot P(B_2) = (0.9 \cdot 0.7) + (0.2 \cdot 0.3) = 0.63 + 0.06 = 0.69
$$

### 4.4.2 Law of Total Probability and Bayes' Rule Combined

**Explanation**: The Law of Total Probability is often used in conjunction with Bayes' Rule. To calculate the posterior probability $P(H|E)$ using Bayes' Rule, the marginal likelihood $P(E)$ is often determined using the Law of Total Probability.

**Formula**:

$$
P(H|E) = \frac{P(E|H) \cdot P(H)}{\sum_{i} P(E|H_i) \cdot P(H_i)}
$$

where $\{H_1, H_2, \dots, H_n\}$ are the mutually exclusive hypotheses that together make up the entire sample space.

**Example**: Continuing from the disease testing example, suppose there are two diseases, $H_1$ and $H_2$, that can cause a positive test result. The test's likelihoods and prior probabilities are as follows: $P(E|H_1) = 0.99$, $P(E|H_2) = 0.95$, $P(H_1) = 0.001$, and $P(H_2) = 0.002$. The marginal likelihood $P(E)$ can be calculated as:

$$
P(E) = P(E|H_1) \cdot P(H_1) + P(E|H_2) \cdot P(H_2) + P(E|\neg H_1 \cap \neg H_2) \cdot P(\neg H_1 \cap \neg H_2)
$$

where $P(E|\neg H_1 \cap \neg H_2) = 0.01$ and $P(\neg H_1 \cap \neg H_2) = 0.997$. Substituting the values:

$$
P(E) = (0.99 \cdot 0.001) + (0.95 \cdot 0.002) + (0.01 \cdot 0.997) = 0.00099 + 0.0019 + 0.00997 = 0.01286
$$

Using Bayes' Rule for $H_1$:

$$
P(H_1|E) = \frac{0.99 \cdot 0.001}{0.01286} \approx 0.0769
$$

### 4.4.3 Complementary Rule

**Definition**: The Complementary Rule states that the probability of an event not occurring is 1 minus the probability of the event occurring.

**Formula**:

$$
P(A^c) = 1 - P(A)
$$

where $A^c$ is the complement of event $A$.

**Example**: If the probability of raining tomorrow is $P(A) = 0.7$, then the probability that it does not rain is:

$$
P(A^c) = 1 - 0.7 = 0.3
$$

### 4.4.4 Inclusion-Exclusion Principle

**Definition**: The Inclusion-Exclusion Principle is used to calculate the probability of the union of multiple events by accounting for the overlaps between events.

**Formula (for two events)**:

$$
P(A \cup B) = P(A) + P(B) - P(A \cap B)
$$

**Example**: Suppose the probability of a student passing Math is $P(A) = 0.6$, and the probability of passing English is $P(B) = 0.5$. The probability of passing both subjects is $P(A \cap B) = 0.3$. The probability of passing at least one subject is:

$$
P(A \cup B) = 0.6 + 0.5 - 0.3 = 0.8
$$

**Formula (for three events)**:

$$
P(A \cup B \cup C) = P(A) + P(B) + P(C) - P(A \cap B) - P(B \cap C) - P(C \cap A) + P(A \cap B \cap C)
$$

**Example**: If $P(A) = 0.4$, $P(B) = 0.5$, $P(C) = 0.6$, $P(A \cap B) = 0.2$, $P(B \cap C) = 0.25$, $P(C \cap A) = 0.15$, and $P(A \cap B \cap C) = 0.1$, then the probability of passing at least one of the subjects is:

$$
P(A \cup B \cup C) = 0.4 + 0.5 + 0.6 - 0.2 - 0.25 - 0.15 + 0.1 = 1.0
$$

## 4.5 Discrete and Continuous Random Variables

### 4.5.1 Discrete Random Variables

**Definition**: A random variable that can take on a finite or countably infinite number of distinct values. Each value represents a possible outcome of a random process.

**Example**: The number of heads in three tosses of a coin is a discrete random variable because it can only take values from the set $\{0, 1, 2, 3\}$.

**Probability Mass Function (PMF)**: A function $P(X = x_i)$ that gives the probability that the discrete random variable $X$ takes on the specific value $x_i$.

**Properties**:
- $\sum_{i} P(X = x_i) = 1$: The sum of the probabilities of all possible values of $X$ must equal 1, ensuring that one of the possible outcomes occurs.
- $P(X = x_i) \geq 0$ for all $x_i$: Probabilities must be non-negative.

**Example**: For the discrete random variable representing the number of heads in three coin tosses, the PMF might look like this:

$$
P(X = 0) = \frac{1}{8}, \, P(X = 1) = \frac{3}{8}, \, P(X = 2) = \frac{3}{8}, \, P(X = 3) = \frac{1}{8}
$$

This satisfies the requirement that the total probability across all possible outcomes is 1.

### 4.5.2 Continuous Random Variables

**Definition**: A continuous random variable can take any value within a given range or interval. Unlike discrete random variables, continuous random variables are not countable and can take on infinitely many values.

**Example**: The exact height of individuals in a population is a continuous random variable. Height can take any value within a range, such as between 150 cm and 200 cm.

**Probability Density Function (PDF)**: A function $f(x)$ that describes the likelihood of $X$ taking on a value within an infinitesimally small interval. The probability that $X$ takes on a value within a certain interval $[a, b]$ is given by the area under the curve of $f(x)$ between $a$ and $b$:

$$
P(a \leq X \leq b) = \int_{a}^{b} f(x) \, dx
$$

**Properties**:
- $f(x) \geq 0$ for all $x$: The PDF cannot be negative.
- $\int_{-\infty}^{\infty} f(x) \, dx = 1$: The total area under the PDF curve is 1, ensuring that the probability over the entire sample space is 1.

**Example**: The height distribution of adult males in a population might be modeled by a normal distribution with a specific mean (e.g., $\mu = 175$ cm) and standard deviation (e.g., $\sigma = 10$ cm). The PDF describes the probability density over the range of possible heights.

## 4.6 Expectation and Variance

### 4.6.1 Expected Value (Expectation)

**Definition**: The expected value or mean of a random variable $X$, denoted $E(X)$, is the long-run average value of repetitions of the experiment it represents. It provides a measure of the "center" of the distribution of the random variable.

**Formula (Discrete)**: 

$$
E(X) = \sum_{i} x_i \cdot P(X = x_i)
$$

where $x_i$ are the possible values of $X$, and $P(X = x_i)$ is the probability of each value.

**Formula (Continuous)**:

$$
E(X) = \int_{-\infty}^{\infty} x \cdot f(x) \, dx
$$

where $f(x)$ is the probability density function.

**Example**: If $X$ represents the number of heads in three coin tosses, the expected value would be:

$$
E(X) = 0 \cdot \frac{1}{8} + 1 \cdot \frac{3}{8} + 2 \cdot \frac{3}{8} + 3 \cdot \frac{1}{8} = 1.5
$$

### 4.6.2 Variance and Standard Deviation

**Definition**: Variance measures the spread of a random variable's values around the mean, denoted $Var(X)$. It quantifies how much the values of the random variable differ from the expected value.

**Formula**:

$$
Var(X) = E[(X - E(X))^2]
$$

**Standard Deviation**: The square root of the variance, denoted $\sigma(X)$, which provides a measure of spread in the same units as $X$:

$$
\sigma(X) = \sqrt{Var(X)}
$$

**Example**: If the expected value of the number of heads in three coin tosses is 1.5, and the variance is calculated as 0.75, then the standard deviation would be:

$$
\sigma(X) = \sqrt{0.75} \approx 0.87
$$

## 4.7 Probability Distributions

### 4.7.1 Introduction to Probability Distributions

**Definition**: A probability distribution describes how the values of a random variable are distributed. It gives the probabilities of occurrence of different possible outcomes in an experiment.

- **Discrete Probability Distributions**: These distributions apply to discrete random variables, which can take on a finite or countably infinite set of values. Examples include the number of heads in a series of coin tosses, or the number of students who pass an exam.
  
- **Continuous Probability Distributions**: These distributions apply to continuous random variables, which can take on any value within a given range. Examples include the exact height of individuals in a population or the amount of time it takes to complete a task.

### 4.7.2 Probability Mass Function (PMF)

**Definition**: The Probability Mass Function (PMF) is a function that gives the probability that a discrete random variable is exactly equal to some value. It provides a complete description of the distribution of a discrete random variable.

**Formula**:

$$
P(X = x_i) = \text{PMF}(x_i)
$$

where $X$ is a discrete random variable, and $x_i$ is a possible value that $X$ can take.

**Properties of PMF**:
1. **Non-negativity**: $P(X = x_i) \geq 0$ for all $x_i$.
2. **Normalization**: The sum of the probabilities for all possible values must be 1:
   $$
   \sum_{i} P(X = x_i) = 1
   $$

**Example**: Consider the random variable $X$ representing the number of heads in three tosses of a fair coin. The possible values of $X$ are 0, 1, 2, and 3. The PMF is given by:

$$
P(X = 0) = \frac{1}{8}, \, P(X = 1) = \frac{3}{8}, \, P(X = 2) = \frac{3}{8}, \, P(X = 3) = \frac{1}{8}
$$

This tells us, for example, that the probability of getting exactly 2 heads in three tosses is $P(X = 2) = \frac{3}{8}$.

### 4.7.3 Probability Density Function (PDF)

**Definition**: The Probability Density Function (PDF) is a function that describes the likelihood of a continuous random variable taking on a particular value. Unlike a PMF, a PDF does not give probabilities directly but rather a density, which must be integrated over an interval to yield a probability.

**Formula**:

$$
f(x) = \text{PDF}(x)
$$

where $X$ is a continuous random variable, and $f(x)$ is the value of the density function at $x$.

**Properties of PDF**:
1. **Non-negativity**: $f(x) \geq 0$ for all $x$.
2. **Normalization**: The total area under the PDF curve must be 1:
   $$
   \int_{-\infty}^{\infty} f(x) \, dx = 1
   $$
3. **Probability Calculation**: The probability that $X$ lies within an interval $[a, b]$ is given by the integral of the PDF over that interval:
   $$
   P(a \leq X \leq b) = \int_{a}^{b} f(x) \, dx
   $$

**Example**: Consider a random variable $X$ representing the height of adult males in a population, which is normally distributed with a mean $\mu = 175$ cm and a standard deviation $\sigma = 10$ cm. The PDF of $X$ is given by:

$$
f(x) = \frac{1}{\sqrt{2\pi \sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

For this normal distribution, to find the probability that a randomly selected adult male has a height between 170 cm and 180 cm, you would calculate:

$$
P(170 \leq X \leq 180) = \int_{170}^{180} f(x) \, dx
$$

This integral represents the area under the PDF curve between 170 cm and 180 cm.

### 4.7.4 Cumulative Distribution Function (CDF)

**Definition**: The Cumulative Distribution Function (CDF) gives the probability that a random variable $X$ will take a value less than or equal to $x$. The CDF applies to both discrete and continuous random variables.

**Formula (Discrete)**:

$$
F(x) = P(X \leq x) = \sum_{x_i \leq x} P(X = x_i)
$$

**Formula (Continuous)**:

$$
F(x) = P(X \leq x) = \int_{-\infty}^{x} f(t) \, dt
$$

**Properties of CDF**:
1. **Non-decreasing**: $F(x)$ is a non-decreasing function.
2. **Limits**:
   $$
   \lim_{x \to -\infty} F(x) = 0, \, \lim_{x \to \infty} F(x) = 1
   $$
3. **Relationship with PDF**: For continuous random variables, the PDF is the derivative of the CDF:
   $$
   f(x) = \frac{dF(x)}{dx}
   $$

**Example (Discrete)**: For the random variable $X$ representing the number of heads in three coin tosses, the CDF at $x = 2$ is:

$$
F(2) = P(X \leq 2) = P(X = 0) + P(X = 1) + P(X = 2) = \frac{1}{8} + \frac{3}{8} + \frac{3}{8} = \frac{7}{8} = 0.875
$$

**Example (Continuous)**: For the normal distribution example with $\mu = 175$ cm and $\sigma = 10$ cm, the CDF can be used to find the probability that a randomly selected adult male is shorter than 180 cm:

$$
P(X \leq 180) = F(180) = \int_{-\infty}^{180} f(x) \, dx
$$

This would give the total area under the PDF curve to the left of 180 cm.

### 4.7.5 Common Probability Distributions

#### 4.7.5.1 Discrete Distributions

- **Binomial Distribution**: Describes the number of successes in a fixed number of independent Bernoulli trials, each with the same probability of success. The PMF is:

  $$
  P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}
  $$

  **Example**: The number of heads in 10 coin flips, where $p = 0.5$ and $n = 10$.

- **Poisson Distribution**: Models the number of times an event occurs in a fixed interval of time or space. The PMF is:

  $$
  P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}
  $$

  **Example**: The number of emails received in an hour, where $\lambda = 3$.

#### 4.7.5.2 Continuous Distributions

- **Normal Distribution**: A continuous distribution characterized by a symmetric, bell-shaped curve. The PDF is:

  $$
  f(x) = \frac{1}{\sqrt{2\pi \sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
  $$

  **Example**: Heights of adult males, where $\mu = 175$ cm and $\sigma = 10$ cm.

- **Exponential Distribution**: Models the time between events in a Poisson process. The PDF is:

  $$
  f(x) = \lambda e^{-\lambda x}, \quad x \geq 0
  $$

  **Example**: The time until the next earthquake, where $\lambda = 0.1$ per year.

### 4.7.6 Summary

Probability distributions are foundational in probability theory, describing how random variables behave and how their probabilities are allocated. Understanding PMFs, PDFs, and CDFs is crucial for analyzing both discrete and continuous random variables, allowing for the computation of probabilities, expectations, and variances, and forming the basis for statistical inference and modeling.

## 4.8 Law of Large Numbers and Central Limit Theorem

### 4.8.1 Law of Large Numbers (LLN)

**Definition**: The LLN states that as the number of trials increases, the sample mean of the observed values converges to the expected value. It ensures that the average of the results obtained from a large number of trials should be close to the expected value, and will tend to become closer as more trials are performed.

**Example**: Suppose you repeatedly flip a fair coin. The expected value of the proportion of heads is 0.5. According to the LLN, as the number of flips increases, the observed proportion of heads will get closer and closer to 0.5.

### 4.8.2 Central Limit Theorem (CLT)

**Definition**: The CLT states that, for a large enough sample size, the distribution of the sample mean will be approximately normally distributed, regardless of the original distribution of the population. This is a cornerstone of statistics because it justifies the use of the normal distribution in many practical situations.

**Example**: Consider rolling a fair six-sided die 100 times. The sum of the results is a random variable that, according to the CLT, will be approximately normally distributed with a mean of $E(X) = 100 \times 3.5 = 350$ and a standard deviation of $\sigma(X) = \sqrt{100 \times \frac{35}{12}} \approx 5.77$, even though the distribution of a single roll is not normal.

## 4.9 Applications of Probability Theory

### 4.9.1 Monte Carlo Simulations

**Definition**: A computational algorithm that uses repeated random sampling to estimate numerical results. Monte Carlo methods are widely used in fields like finance, engineering, and physics to solve problems that might be deterministic in principle but are too complex to solve directly.

**Example**: To estimate the value of $\pi$, you could randomly generate points within a square that bounds a quarter-circle. The ratio of points that fall inside the quarter-circle to the total number of points, multiplied by 4, approximates $\pi`. If 100,000 points are generated and 78,600 fall inside the quarter-circle, the estimate for $\pi$ would be $\frac{4 \times 78,600}{100,000} = 3.144$, which is close to the actual value of $\pi$.

### 4.9.2 Bayesian Inference

**Definition**: Bayesian inference is a method of statistical inference that updates the probability for a hypothesis as more evidence or information becomes available. It relies on Bayes' theorem to revise beliefs in light of new data.

**Bayes' Theorem**:

$$
P(H|E) = \frac{P(E|H) \cdot P(H)}{P(E)}
$$

where $P(H|E)$ is the posterior probability of the hypothesis $H$ given the evidence $E$, $P(E|H)$ is the likelihood of observing $E$ given that $H$ is true, $P(H)$ is the prior probability of the hypothesis before observing the evidence, and $P(E)$ is the marginal likelihood of the evidence.

**Example**: Bayesian inference is commonly used in medical diagnosis. For instance, if a patient tests positive for a disease, Bayesian methods can be applied to update the probability of the disease being present, taking into account the accuracy of the test (sensitivity and specificity) and the prior probability of the disease in the population.

## 4.10 Bayesian Networks

### 4.10.1 Introduction to Bayesian Networks

**Definition**: A Bayesian Network (also known as a Belief Network or Probabilistic Directed Acyclic Graph) is a graphical model that represents a set of variables and their conditional dependencies via a directed acyclic graph (DAG). Each node in the graph represents a random variable, while the edges represent conditional dependencies; the absence of an edge between two nodes implies a conditional independence between the variables.

**Purpose**: Bayesian Networks are powerful tools for reasoning under uncertainty and are widely used in areas such as diagnostics, decision support systems, machine learning, and natural language processing.

**Example**: Consider a simplified medical diagnosis scenario involving three variables: `Disease`, `Symptom1`, and `Symptom2`. The presence of a disease can influence the occurrence of certain symptoms. The Bayesian Network could represent this as follows:
- `Disease` is the parent node, with directed edges pointing to `Symptom1` and `Symptom2`.
- The graph structure suggests that knowing whether the disease is present affects the probability of observing the symptoms.

### 4.10.2 Structure of Bayesian Networks

**Nodes**: Each node in the network represents a random variable, which could be discrete (e.g., binary outcomes like True/False) or continuous (e.g., height, weight).

**Edges**: Directed edges between nodes represent conditional dependencies. If there is an edge from node $A$ to node $B$, then $B$ is conditionally dependent on $A$. This means that knowing the value of $A$ gives us information about the likelihood of $B$.

**Conditional Probability Tables (CPTs)**: Each node has an associated CPT that specifies the probability distribution of the node given its parent nodes. For nodes without parents, the CPT represents the prior probability of the variable. The CPT for a node is crucial in defining how the probability of that node changes given different states of its parent nodes.

**Example**:
Consider the following CPT for the `Disease` node:

- $P(\text{Disease=True}) = 0.01$
- $P(\text{Disease=False}) = 0.99$

Now, consider the CPT for `Symptom1` given the state of `Disease`:

- $P(\text{Symptom1=True} \mid \text{Disease=True}) = 0.8$
- $P(\text{Symptom1=False} \mid \text{Disease=True}) = 0.2$
- $P(\text{Symptom1=True} \mid \text{Disease=False}) = 0.1$
- $P(\text{Symptom1=False} \mid \text{Disease=False}) = 0.9$

This table tells us that if the disease is present, there is an 80% chance of `Symptom1` occurring, but if the disease is absent, the chance of `Symptom1` is only 10%.

### 4.10.3 Inference in Bayesian Networks

**Objective**: Inference in Bayesian Networks involves computing the posterior probabilities of certain variables given evidence about others. This process is essential for updating our beliefs about the state of a system when new information becomes available.

#### Example 1: Posterior Probability Calculation

Suppose we observe that `Symptom1=True`. We want to compute the updated probability that `Disease=True`.

Using Bayes' theorem:

$$
P(\text{Disease=True} \mid \text{Symptom1=True}) = \frac{P(\text{Symptom1=True} \mid \text{Disease=True}) \cdot P(\text{Disease=True})}{P(\text{Symptom1=True})}
$$

First, calculate the marginal probability of $\text{Symptom1=True}$:

$$
P(\text{Symptom1=True}) = P(\text{Symptom1=True} \mid \text{Disease=True}) \cdot P(\text{Disease=True}) + P(\text{Symptom1=True} \mid \text{Disease=False}) \cdot P(\text{Disease=False})
$$

$$
P(\text{Symptom1=True}) = (0.8 \times 0.01) + (0.1 \times 0.99) = 0.008 + 0.099 = 0.107
$$

Now, calculate the posterior probability:

$$
P(\text{Disease=True} \mid \text{Symptom1=True}) = \frac{0.8 \times 0.01}{0.107} \approx 0.0748
$$

So, even with `Symptom1` present, the probability of having the disease is approximately 7.48%.

#### Example 2: Joint Probability Calculation

Let's calculate the joint probability of observing both `Symptom1=True` and `Symptom2=True` given the presence of the disease:

$$
P(\text{Symptom1=True}, \text{Symptom2=True} \mid \text{Disease=True}) = P(\text{Symptom1=True} \mid \text{Disease=True}) \cdot P(\text{Symptom2=True} \mid \text{Disease=True})
$$

$$
P(\text{Symptom1=True}, \text{Symptom2=True} \mid \text{Disease=True}) = 0.8 \times 0.7 = 0.56
$$

This result shows that if the disease is present, the probability of both `Symptom1` and `Symptom2` occurring together is 56%.

### 4.10.4 Learning Bayesian Networks

**Structure Learning**: The process of determining the structure of the network from data. Structure learning can be performed using:
- **Constraint-based methods**: These methods rely on conditional independence tests to build the structure of the network. For example, if two variables are conditionally independent given a third variable, there might not be a direct edge between them.
- **Score-based methods**: These methods assign a score to different possible network structures based on how well they fit the data and then search for the structure that maximizes this score. Common scoring functions include the Bayesian Information Criterion (BIC) and Akaike Information Criterion (AIC).

**Parameter Learning**: Once the structure is known, the next step is to learn the CPTs. This can be done using:
- **Maximum Likelihood Estimation (MLE)**: Estimates the parameters that maximize the likelihood of the observed data.
- **Bayesian Estimation**: Incorporates prior distributions over parameters and updates these priors based on observed data.

**Example**:
Suppose we have a dataset of patient records with information about `Disease`, `Symptom1`, and `Symptom2`. Using structure learning algorithms, we could determine the network structure that best captures the dependencies among these variables. Then, using parameter learning, we estimate the CPTs that describe how likely the symptoms are given the presence or absence of the disease.

For instance, if our data shows that out of 100 patients with the disease, 80 show `Symptom1` and 70 show `Symptom2`, MLE would set:

$$
P(\text{Symptom1=True} \mid \text{Disease=True}) = \frac{80}{100} = 0.8
$$

$$
P(\text{Symptom2=True} \mid \text{Disease=True}) = \frac{70}{100} = 0.7
$$

### 4.10.5 Applications of Bayesian Networks

- **Medical Diagnosis**: Bayesian Networks are used to model the probabilistic relationships between diseases and symptoms, aiding in diagnostic decisions. For example, a network could represent how different symptoms are related to various diseases, allowing doctors to update the probability of a disease as symptoms are observed.
  
- **Decision Support Systems**: They provide a framework for making decisions under uncertainty, often used in finance, engineering, and environmental management. For example, a Bayesian Network might be used in finance to assess the likelihood of different economic outcomes based on various indicators.

- **Machine Learning**: Bayesian Networks are employed in classification tasks, anomaly detection, and causal inference. For example, in anomaly detection, a Bayesian Network might model the normal operation of a system, and deviations from this model could indicate anomalies.

- **Natural Language Processing (NLP)**: Used in tasks such as part-of-speech tagging, speech recognition, and machine translation by modeling the probabilistic relationships between linguistic variables. For instance, a Bayesian Network could model the probability of word sequences in a sentence, helping to improve the accuracy of speech recognition systems.

### 4.10.6 Advantages and Limitations

**Advantages**:
- **Interpretability**: The graphical structure of Bayesian Networks makes it easy to understand and visualize the relationships between variables. This is particularly useful in fields like healthcare, where understanding the reasoning behind a decision is critical.
  
- **Flexibility**: They can model complex probabilistic relationships and handle missing data naturally. For instance, even if we don't have complete information about all variables in a network, we can still make inferences based on the available data.

- **Scalability**: Bayesian Networks can be applied to large, high-dimensional datasets, making them suitable for complex real-world problems, such as modeling gene interactions in bioinformatics.

**Limitations**:
- **Computational Complexity**: Exact inference can be computationally expensive, especially in networks with a large number of variables or dense connections. In such cases, approximate inference methods might be necessary, but these can introduce errors.

- **Structure Learning**: Determining the correct structure from data can be challenging and computationally intensive, particularly in the presence of many variables. Even with powerful algorithms, the learned structure might not always perfectly represent the true dependencies.

- **Sensitivity to Prior Information**: The results can be sensitive to the choice of prior distributions, which may introduce biases if not chosen carefully. This is particularly relevant in Bayesian Estimation, where the priors need to be chosen based on domain knowledge or subjective judgment.

### 4.10.7 Summary

Bayesian Networks are a fundamental tool in probabilistic reasoning, offering a structured way to model and infer relationships among random variables. Their ability to incorporate both prior knowledge and observational data makes them indispensable in fields ranging from healthcare to machine learning. However, their computational complexity and sensitivity to priors require careful consideration during implementation.
# 5. Agile Software development

# To be made into notes

## 5.1 Professionel Software Engineering 
There are still many reports of software projects going wrong and of “software
failures.” Software engineering is criticized as inadequate for modern software
development. However, in my opinion, many of these so-called software failures
are a consequence of two factors:

1. Increasing system complexity As new software engineering techniques help us
	to build larger, more complex systems, the demands change. Systems have to be
	built and delivered more quickly; larger, even more complex systems are
	required; and systems have to have new capabilities that were previously
	thought to be impossible. New software engineering techniques have to be
	developed to meet new the challenges of delivering more complex software.
1. Failure to use software engineering methods It is fairly easy to write computer
	programs without using software engineering methods and techniques. Many
	companies have drifted into software development as their products and services
	have evolved. They do not use software engineering methods in their everyday
	work. Consequently, their software is often more expensive and less reliable
	than it should be. We need better software engineering education and training to
	address this problem.


Software engineering is intended to support professional software development
rather than individual programming. It includes techniques that support program
specification, design, and evolution, none of which are normally relevant for personal
software development.

each question and answer is a table row

Question Answer
What is software? Computer programs and associated documentation. Software
products may be developed for a particular customer or may be
developed for a general market.
What are the attributes of good
software?
Good software should deliver the required functionality and
performance to the user and should be maintainable, dependable
and usable.
What is software engineering? Software engineering is an engineering discipline that is concerned
with all aspects of software production from initial conception to
operation and maintenance.
What are the fundamental
software engineering activities?
Software specification, software development, software validation
and software evolution.
What is the difference between
software engineering and
computer science?
Computer science focuses on theory and fundamentals; software
engineering is concerned with the practicalities of developing and
delivering useful software.
What is the difference between
software engineering and system
engineering?
System engineering is concerned with all aspects of computerbased
systems development including hardware, software and
process engineering. Software engineering is part of this more
general process.
What are the key challenges
facing software engineering?
Coping with increasing diversity, demands for reduced delivery
times and developing trustworthy software.
What are the costs of software
engineering?
Roughly 60% of software costs are development costs, 40% are
testing costs. For custom software, evolution costs often exceed
development costs.
What are the best software
engineering techniques and
methods?
While all software projects have to be professionally managed and
developed, different techniques are appropriate for different types
of system. For example, games should always be developed using
a series of prototypes whereas safety critical control systems
require a complete and analyzable specification to be developed.
There are no methods and techniques that are good for everything.
What differences has the Internet
made to software engineering?
Not only has the Internet led to the development of massive, highly
distributed, service-based systems, it has also supported the
creation of an “app” industry for mobile devices which has
changed the economics of software.


Software engineers are concerned with developing software products, that is,
software that can be sold to a customer. There are two kinds of software product:

1. Generic products These are stand-alone systems that are produced by a
development organization and sold on the open market to any customer who is
able to buy them. Examples of this type of product include apps for mobile
devices, software for PCs such as databases, word processors, drawing packages,
and project management tools. This kind of software also includes “vertical”

The critical distinction between these types of software is that, in generic products,
the organization that develops the software controls the software specification.
This means that if they run into development problems, they can rethink what is to
be developed. For custom products, the specification is developed and controlled by
the organization that is buying the software. The software developers must work to
that specification.

### 5.1.1 Software Engineering 

Software engineering is an engineering discipline that is concerned with all aspects
of software production from the early stages of system specification through to
maintaining the system after it has gone into use. In this definition, there are two
key phrases:
1. Engineering discipline Engineers make things work. They apply theories, methods,
and tools where these are appropriate. However, they use them selectively
and always try to discover solutions to problems even when there are no applicable
theories and methods. Engineers also recognize that they must work
within organizational and financial constraints, and they must look for solutions
within these constraints.
2. All aspects of software production Software engineering is not just concerned
with the technical processes of software development. It also includes activities
such as software project management and the development of tools, methods,
and theories to support software development.


Table 
Product characteristic Description
Acceptability Software must be acceptable to the type of users for which it is
designed. This means that it must be understandable, usable, and
compatible with other systems that they use.
Dependability and security Software dependability includes a range of characteristics including
reliability, security, and safety. Dependable software should not
cause physical or economic damage in the event of system failure.
Software has to be secure so that malicious users cannot access or
damage the system.
Efficiency Software should not make wasteful use of system resources such
as memory and processor cycles. Efficiency therefore includes
responsiveness, processing time, resource utilization, etc.
Maintainability Software should be written in such a way that it can evolve to
meet the changing needs of customers. This is a critical attribute
because software change is an inevitable requirement of a
changing business environment.


important so highlight it or something

Software engineering is important for two reasons:
1. More and more, individuals and society rely on advanced software systems. We need
to be able to produce reliable and trustworthy systems economically and quickly.
2. It is usually cheaper, in the long run, to use software engineering methods and
techniques for professional software systems rather than just write programs as

important so highlight it or something

Four fundamental activities are common to all
software processes.
1. Software specification, where customers and engineers define the software that
is to be produced and the constraints on its operation.
2. Software development, where the software is designed and programmed.
3. Software validation, where the software is checked to ensure that it is what the
customer requires.
4. Software evolution, where the software is modified to reflect changing customer
and market requirements.

there are four related issues that affect many different types of software:

1. Heterogeneity Increasingly, systems are required to operate as distributed systems
across networks that include different types of computer and mobile
devices. As well as running on general-purpose computers, software may also
have to execute on mobile phones and tablets. You often have to integrate new
software with older legacy systems written in different programming languages.
The challenge here is to develop techniques for building dependable software
that is flexible enough to cope with this heterogeneity.
2. Business and social change Businesses and society are changing incredibly
quickly as emerging economies develop and new technologies become available.
They need to be able to change their existing software and to rapidly
develop new software. Many traditional software engineering techniques are
time consuming, and delivery of new systems often takes longer than planned.
They need to evolve so that the time required for software to deliver value to its
customers is reduced.
3. Security and trust As software is intertwined with all aspects of our lives, it is
essential that we can trust that software. This is especially true for remote software
systems accessed through a web page or web service interface. We have to
make sure that malicious users cannot successfully attack our software and that
information security is maintained.
4. Scale Software has to be developed across a very wide range of scales, from
very small embedded systems in portable or wearable devices through to
Internet-scale, cloud-based systems that serve a global community.

### 5.1.2 Software Engineering Diversity

There are many different types of application, including:

Important highlight or something or make them into subheaders

1. Stand-alone applications These are application systems that run on a personal
computer or apps that run on a mobile device. They include all necessary functionality
and may not need to be connected to a network. Examples of such
applications are office applications on a PC, CAD programs, photo manipulation
software, travel apps, productivity apps, and so on.
2. Interactive transaction-based applications These are applications that execute
on a remote computer and that are accessed by users from their own computers,
phones, or tablets. Obviously, these include web applications such as e-commerce
applications where you interact with a remote system to buy goods and services.
This class of application also includes business systems, where a business
provides access to its systems through a web browser or special-purpose client
program and cloud-based services, such as mail and photo sharing. Interactive
applications often incorporate a large data store that is accessed and updated in
each transaction.
3. Embedded control systems These are software control systems that control and
manage hardware devices. Numerically, there are probably more embedded systems
than any other type of system. Examples of embedded systems include the
software in a mobile (cell) phone, software that controls antilock braking in a
car, and software in a microwave oven to control the cooking process.
4. Batch processing systems These are business systems that are designed to process
data in large batches. They process large numbers of individual inputs to
create corresponding outputs. Examples of batch systems are periodic billing
systems, such as phone billing systems, and salary payment systems.
5. Entertainment systems These are systems for personal use that are intended to
entertain the user. Most of these systems are games of one kind or another,
which may run on special-purpose console hardware. The quality of the user
interaction offered is the most important distinguishing characteristic of entertainment
systems.
6. Systems for modeling and simulation These are systems that are developed by
scientists and engineers to model physical processes or situations, which include
many separate, interacting objects. These are often computationally intensive
and require high-performance parallel systems for execution.
7. Data collection and analysis systems Data collection systems are systems that
collect data from their environment and send that data to other systems for processing.
The software may have to interact with sensors and often is installed in
a hostile environment such as inside an engine or in a remote location. “Big
data” analysis may involve cloud-based systems carrying out statistical analysis
and looking for relationships in the collected data.
8. Systems of systems These are systems, used in enterprises and other large organizations,
that are composed of a number of other software systems. Some of
these may be generic software products, such as an ERP system. Other systems
in the assembly may be specially written for that environment.

Important highlight or something or make them into subheaders

Nevertheless, there are software engineering fundamentals that apply to all types
of software systems:
1. They should be developed using a managed and understood development process.
The organization developing the software should plan the development
process and have clear ideas of what will be produced and when it will be completed.
Of course, the specific process that you should use depends on the type
of software that you are developing.
2. Dependability and performance are important for all types of system. Software
should behave as expected, without failures, and should be available for use
when it is required. It should be safe in its operation and, as far as possible,
should be secure against external attack. The system should perform efficiently
and should not waste resources.
3. Understanding and managing the software specification and requirements (what
the software should do) are important. You have to know what different customers
and users of the system expect from it, and you have to manage their expectations
so that a useful system can be delivered within budget and to schedule.
4. You should make effective use of existing resources. This means that, where
appropriate, you should reuse software that has already been developed rather
than write new software

### 5.1.3 Software Engineering Ethics

1. Confidentiality You should normally respect the confidentiality of your employers
or clients regardless of whether or not a formal confidentiality agreement
has been signed.
2. Competence You should not misrepresent your level of competence. You should
not knowingly accept work that is outside your competence.
3. Intellectual property rights You should be aware of local laws governing the
use of intellectual property such as patents and copyright. You should be careful
to ensure that the intellectual property of employers and clients is protected.
4. Computer misuse You should not use your technical skills to misuse other people’s
computers. Computer misuse ranges from relatively trivial (game playing
on an employer’s machine) to extremely serious (dissemination of viruses or
other malware).

## 5.2 Software Processes 
when describing processes, it is also important to describe who is
involved, what is produced, and conditions that influence the sequence of activities:
1. Products or deliverables are the outcomes of a process activity. For example, the
outcome of the activity of architectural design may be a model of the software
architecture.
2. Roles reflect the responsibilities of the people involved in the process. Examples
of roles are project manager, configuration manager, and programmer.
3. Pre- and postconditions are conditions that must hold before and after a process
activity has been enacted or a product produced. For example, before architectural
design begins, a precondition may be that the consumer has approved all
requirements; after this activity is finished, a postcondition might be that the
UML models describing the architecture have been reviewed.

### 5.2.1 Software Process Model

Important highlight or something


You can think of them as process frameworks that may be extended and adapted to create
more specific software engineering processes.
The general process models that I cover here are:
1. The waterfall model This takes the fundamental process activities of specification,
development, validation, and evolution and represents them as separate
process phases such as requirements specification, software design, implementation,
and testing.
2. Incremental development This approach interleaves the activities of specification,
development, and validation. The system is developed as a series of versions
(increments), with each version adding functionality to the previous version.
3. Integration and configuration This approach relies on the availability of reusable
components or systems. The system development process focuses on
configuring these components for use in a new setting and integrating them
into a system.

#### 5.2.1.1 The Waterfall Method

![[Pasted image 20240904223553.png]]

The first published model of the software development process was derived from
engineering process models used in large military systems engineering (Royce
1970). It presents the software development process as a number of stages, as shown
in Figure 2.1. Because of the cascade from one phase to another, this model is known
as the waterfall model or software life cycle. The waterfall model is an example of a
plan-driven process. In principle at least, you plan and schedule all of the process
activities before starting software development.
The stages of the waterfall model directly reflect the fundamental software development
activities:

1. Requirements analysis and definition The system’s services, constraints, and
goals are established by consultation with system users. They are then defined
in detail and serve as a system specification.
2. System and software design The systems design process allocates the requirements
to either hardware or software systems. It establishes an overall system
architecture. Software design involves identifying and describing the fundamental
software system abstractions and their relationships.
3. Implementation and unit testing During this stage, the software design is realized
as a set of programs or program units. Unit testing involves verifying that
each unit meets its specification.
4. Integration and system testing The individual program units or programs are
integrated and tested as a complete system to ensure that the software
requirements have been met. After testing, the software system is delivered
to the customer.
5. Operation and maintenance Normally, this is the longest life-cycle phase. The
system is installed and put into practical use. Maintenance involves correcting
errors that were not discovered in earlier stages of the life cycle, improving the
implementation of system units, and enhancing the system’s services as new
requirements are discovered.

The need for early commitment and system rework when changes are
made means that the waterfall model is only appropriate for some types of system:
1. Embedded systems where the software has to interface with hardware systems.
Because of the inflexibility of hardware, it is not usually possible to delay decisions
on the software’s functionality until it is being implemented.
2. Critical systems where there is a need for extensive safety and security analysis
of the software specification and design. In these systems, the specification and
design documents must be complete so that this analysis is possible. Safety related
problems in the specification and design are usually very expensive to
correct at the implementation stage.
3. Large software systems that are part of broader engineering systems developed
by several partner companies. The hardware in the systems may be developed
using a similar model, and companies find it easier to use a common model for
hardware and software. Furthermore, where several companies are involved,
complete specifications may be needed to allow for the independent development
of different subsystems.
The waterfall model is not the right process model in situations where informal
team communication is possible and software requirements change quickly. Iterative
development and agile methods are better for these systems.

#### 5.2.1.2 The Incremental Development
Incremental development is based on the idea of developing an initial implementation,
getting feedback from users and others, and evolving the software through
several versions until the required system has been developed (Figure 2.2).
Specification, development, and validation activities are interleaved rather than
separate,
with rapid feedback across activities.

Important 
Incremental software development, which is a fundamental part of agile
development methods, is better than a waterfall approach for systems whose
requirements are likely to change during the development process. This is the
case for most business systems and software products. Incremental development
reflects the way that we solve problems. We rarely work out a complete problem
solution in advance but move toward a solution in a series of steps, backtracking
when we realize that we have made a mistake. By developing the
software incrementally, it is cheaper and easier to make changes in the software
as it is being developed.
Each increment or version of the system incorporates some of the functionality
that is needed by the customer. Generally, the early increments of the system
include the most important or most urgently required functionality. This means
that the customer or user can evaluate the system at a relatively early stage in
the development to see if it delivers what is required. If not, then only the current
increment has to be changed and, possibly, new functionality defined for
later increments.
Incremental development has three major advantages over the waterfall model:

1. The cost of implementing requirements changes is reduced. The amount of
analysis and documentation that has to be redone is significantly less than is
required with the waterfall model.
2. It is easier to get customer feedback on the development work that has been
done. Customers can comment on demonstrations of the software and see how
much has been implemented. Customers find it difficult to judge progress from
software design documents.
3. Early delivery and deployment of useful software to the customer is possible,
even if all of the functionality has not been included. Customers are able to use
and gain value from the software earlier than is possible with a waterfall process.
From a management perspective, the incremental approach has two problems:
1. The process is not visible. Managers need regular deliverables to measure progress.
If systems are developed quickly, it is not cost effective to produce documents
that reflect every version of the system.
2. System structure tends to degrade as new increments are added. Regular change
leads to messy code as new functionality is added in whatever way is possible.
It becomes increasingly difficult and costly to add new features to a system. To
reduce structural degradation and general code messiness, agile methods suggest
that you should regularly refactor (improve and restructure) the software.

The problems of incremental development become particularly acute for large,
complex, long-lifetime systems, where different teams develop different parts of the
system. Large systems need a stable framework or architecture, and the responsibilities
of the different teams working on parts of the system need to be clearly
defined with respect to that architecture. This has to be planned in advance rather
than developed incrementally.

#### 5.2.1.2 Integration And Configuration
![[Pasted image 20240904235145.png]]

Three types of software components are frequently reused:
1. Stand-alone application systems that are configured for use in a particular environment.
These systems are general-purpose systems that have many features,
but they have to be adapted for use in a specific application.
2. Collections of objects that are developed as a component or as a package to be
integrated with a component framework such as the Java Spring framework
(Wheeler and White 2013).
3. Web services that are developed according to service standards and that are
available for remote invocation over the Internet

based on
integration and configuration. The stages in this process are:
1. Requirements specification The initial requirements for the system are proposed.
These do not have to be elaborated in detail but should include brief
descriptions of essential requirements and desirable system features.
2. Software discovery and evaluation Given an outline of the software requirements,
a search is made for components and systems that provide the functionality
required. Candidate components and systems are evaluated to see if
they meet the essential requirements and if they are generally suitable for
use in the system.
3. Requirements refinement During this stage, the requirements are refined using
information about the reusable components and applications that have been
discovered. The requirements are modified to reflect the available components,
and the system specification is re-defined. Where modifications are
impossible, the component analysis activity may be reentered to search for
alternative solutions.
4. Application system configuration If an off-the-shelf application system that
meets the requirements is available, it may then be configured for use to create
the new system.
5. Component adaptation and integration If there is no off-the-shelf system, individual
reusable components may be modified and new components developed.
These are then integrated to create the system.

### 5.2.2 Process Activities

The four basic process activities of specification, development, validation, and
evolution are organized differently in different development processes. In the waterfall
model, they are organized in sequence, whereas in incremental development
they are interleaved. How these activities are carried out depends on the type of
software being developed, the experience and competence of the developers, and the
type of organization developing the software.

#### 5.2.2.1 Software Specifications
![[Pasted image 20240905021311.png]]

There are three main activities in the requirements engineering process:
1. Requirements elicitation and analysis This is the process of deriving the system
requirements through observation of existing systems, discussions with potential
users and procurers, task analysis, and so on. This may involve the development
of one or more system models and prototypes. These help you understand
the system to be specified.
2. Requirements specification Requirements specification is the activity of translating
the information gathered during requirements analysis into a document
that defines a set of requirements. Two types of requirements may be included
in this document. User requirements are abstract statements of the system
requirements for the customer and end-user of the system; system requirements
are a more detailed description of the functionality to be provided.
3. Requirements validation This activity checks the requirements for realism,
consistency, and completeness. During this process, errors in the requirements
document are inevitably discovered. It must then be modified to correct
these problems.


#### 5.2.2.2 Software Design And Implementation
![[Pasted image 20240905022444.png]]

Figure 2.5
shows four activities that may be part of the design process for information systems:
1. Architectural design, where you identify the overall structure of the system, the
principal components (sometimes called subsystems or modules), their relationships,
and how they are distributed.
2. Database design, where you design the system data structures and how these are
to be represented in a database. Again, the work here depends on whether an
existing database is to be reused or a new database is to be created.
3. Interface design, where you define the interfaces between system components.
This interface specification must be unambiguous. With a precise interface, a
component may be used by other components without them having to know
how it is implemented. Once interface specifications are agreed, the components
can be separately designed and developed.
4. Component selection and design, where you search for reusable components
and, if no suitable components are available, design new software components.
The design at this stage may be a simple component description with the implementation
details left to the programmer. Alternatively, it may be a list of
changes to be made to a reusable component or a detailed design model
expressed in the UML. The design model may then be used to automatically
generate an implementation.













