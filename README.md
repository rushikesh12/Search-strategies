# Search-strategies
Implmented Informed and Uniformed Search Strategies in Python 3.

Search-strategies play an important part in Artificial Intelligence, when Agents have to provide a solution to problems. There can be numerous solutions of a single problem, thus to implement the most effective (user defined mostly cost based) we use different search strategies to solve the problem.

In this implementation, I have implemented an Uninformed and an Informed Solution.

*Both the implementation are Graph-based i.e nodes are not repeatedly expanded*

Reference Graph-Representaion:
![Graph-Representation](https://github.com/rushikesh12/Search-strategies/blob/master/graph_representation.png)

## Uniformed Approach
In this approach the agent is only provided with the list of nodes and must find the effective path to goal form the source location. In this implementation, the input1.txt provideds the distance between two nodes as represented by the graph above. I have chosen to implement Uniform Cost Search (UCS) as this approach guarantees to find the solution with the least cost.

## Informed(Heuristic) Approach
In this approach the agent along with the list of nodes, it is provided with [heuristic](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html). This method will use the input1.txt as well the h_kassel.txt(heuristic) for find th effective path to goal from source location. I have chosen to implement A* (A-star) algorithm as this approach guarantees(depending on the heuristic) to find the solution with the least cost.

### To run the program
**Uninformed Approach**
```bash
python find_route.py input1.txt origin_city destination_city
```
For example: python find_route.py input1.txt Bremen Kassel

**Informed(Heuristic) Approach**
```bash
python find_route.py input1.txt origin_city destination_city h_kassel.txt 
```
For example: python find_route.py input1.txt Bremen Kassel h_kassel.txt