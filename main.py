import colorama
import sys
from colorama import Back, Style
from time import time


def valid(grid,curNode,nextX,nextY):
    return (nextX>=0 and nextX<grid.height) and (nextY>=0 and nextY<grid.width) and (not grid.matrix[nextX][nextY] in curNode.predecessor) and (grid.matrix[nextX][nextY].render!=1)

def visit(node1,node2,queue):
    node2.predecessor=node1.predecessor.copy()
    node2.predecessor.append(node1)
    queue.append(node2)

def getCost(Node):
    return Node.value+Node.manhattandist

class Grid:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.matrix=[]
        for i in range(height):
            self.matrix.append([None]*width)
    def print(self,startNode,goalNode):
        for i in range(self.height):
            for j in range(self.width):
                if(self.matrix[i][j].isSameWith(startNode)):
                    print(Back.RED+'  '+Style.RESET_ALL,end='')
                elif(self.matrix[i][j].isSameWith(goalNode)):
                    print(Back.GREEN+'  '+Style.RESET_ALL,end='')
                elif(self.matrix[i][j].render==0):
                    print(Back.WHITE+'  '+Style.RESET_ALL,end='')
                elif(self.matrix[i][j].render==1):
                    print(Back.BLUE+'  '+Style.RESET_ALL,end='')
                elif(self.matrix[i][j].render==2):
                    print(Back.YELLOW+'  '+Style.RESET_ALL,end='')
            print()
    def generateManDist(self,goalNode):
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j].manhattandist=abs(i-goalNode.x)+abs(j-goalNode.y)
    def highLightPath(self,goalNode):
        goalNode.render=2
        for i in range(len(goalNode.predecessor)):
            goalNode.predecessor[i].render=2
    def reset(self):
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j].visited=False
                if(self.matrix[i][j].render==2):
                    self.matrix[i][j].render=0

class Node:
    def __init__(self,x,y,render):
        self.x=x
        self.y=y
        self.render=render
        self.value=0
        self.manhattandist=0
        self.predecessor=[]
        self.visited=False
    def isSameWith(self,otherNode):
        return self.x==otherNode.x and self.y==otherNode.y
    def setVisited(self,bool):
        self.visited=bool
    # def print(self):
    #     print("     x="+str(self.x)+',y='+str(self.y))

class PrioQueue:
    def __init__(self):
        self.queue=[]
    def append(self,element):
        self.queue.append(element)
    def pop(self):
        min=0
        for i in range(1,len(self.queue)):
            if(self.queue[i].value+self.queue[i].manhattandist<self.queue[min].value+self.queue[min].manhattandist):
                min=i
        return self.queue.pop(min)
    # def removeUnwanted(self,curGoalNode):
    #     deleteIndex=[]
    #     for i in range(len(self.queue)-1,-1,-1):
    #         if(self.queue[i].value+self.queue[i].manhattandist>=curGoalNode.value+curGoalNode.manhattandist):
    #             deleteIndex.append(i)
    #     for i in deleteIndex:
    #         del self.queue[i]

def bfs(grid,startx,starty,endx,endy):
    queue=[]
    queue.append(grid.matrix[startx][starty])
    found=False
    count=0
    while(len(queue)>0 and not found):
        count+=1
        curNode=queue.pop(0)
        # print("curnode, x="+str(curNode.x)+', y='+str(curNode.y)+', render='+str(curNode.render))
        # for i in range(len(curNode.predecessor)):
        #     curNode.predecessor[i].print()
        if(curNode.isSameWith(grid.matrix[endx][endy])):
            grid.highLightPath(curNode)
            found=True
        else:
            if(valid(grid,curNode,curNode.x-1,curNode.y) and  not grid.matrix[curNode.x-1][curNode.y].visited):
                visit(curNode,grid.matrix[curNode.x-1][curNode.y],queue)
                grid.matrix[curNode.x-1][curNode.y].setVisited(True)
            if(valid(grid,curNode,curNode.x,curNode.y-1) and not grid.matrix[curNode.x][curNode.y-1].visited):
                visit(curNode,grid.matrix[curNode.x][curNode.y-1],queue)
                grid.matrix[curNode.x][curNode.y-1].setVisited(True)
            if(valid(grid,curNode,curNode.x+1,curNode.y) and not grid.matrix[curNode.x+1][curNode.y].visited):
                visit(curNode,grid.matrix[curNode.x+1][curNode.y],queue)
                grid.matrix[curNode.x+1][curNode.y].setVisited(True)
            if(valid(grid,curNode,curNode.x,curNode.y+1) and not grid.matrix[curNode.x][curNode.y+1].visited):    
                visit(curNode,grid.matrix[curNode.x][curNode.y+1],queue)
                grid.matrix[curNode.x][curNode.y+1].setVisited(True)
    return [count,found]

def astar(grid,startx,starty,endx,endy):
    grid.generateManDist(grid.matrix[endx][endy])
    prioQueue=PrioQueue()
    prioQueue.append(grid.matrix[startx][starty])
    found=False
    count=0
    while(len(prioQueue.queue)>0 and not found):
        count+=1
        # print("current prioqueue=")
        # for i in range(len(prioQueue.queue)):
        #     prioQueue.queue[i].print()
        curNode=prioQueue.pop()
        # print('len pred=',len(curNode.predecessor))
        # print(" curnode, x="+str(curNode.x)+', y='+str(curNode.y))
        if(curNode.isSameWith(grid.matrix[endx][endy])):
            # curGoalNode=curNode
            grid.highLightPath(curNode)
            found=True
        else:
            if(valid(grid,curNode,curNode.x-1,curNode.y) and not grid.matrix[curNode.x-1][curNode.y].visited):
                grid.matrix[curNode.x-1][curNode.y].value=curNode.value+1
                visit(curNode,grid.matrix[curNode.x-1][curNode.y],prioQueue)
                grid.matrix[curNode.x-1][curNode.y].setVisited(True)
            if(valid(grid,curNode,curNode.x,curNode.y-1) and not grid.matrix[curNode.x][curNode.y-1].visited):
                grid.matrix[curNode.x][curNode.y-1].value=curNode.value+1
                visit(curNode,grid.matrix[curNode.x][curNode.y-1],prioQueue)
                grid.matrix[curNode.x][curNode.y-1].setVisited(True)
            if(valid(grid,curNode,curNode.x+1,curNode.y) and not grid.matrix[curNode.x+1][curNode.y].visited):
                grid.matrix[curNode.x+1][curNode.y].value=curNode.value+1
                visit(curNode,grid.matrix[curNode.x+1][curNode.y],prioQueue)
                grid.matrix[curNode.x+1][curNode.y].setVisited(True)
            if(valid(grid,curNode,curNode.x,curNode.y+1) and not grid.matrix[curNode.x][curNode.y+1].visited):    
                grid.matrix[curNode.x][curNode.y+1].value=curNode.value+1
                visit(curNode,grid.matrix[curNode.x][curNode.y+1],prioQueue)
                grid.matrix[curNode.x][curNode.y+1].setVisited(True)
    return [count,found]


if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print('Usage: python main.py <inputmaze>')
    else:
        try:
            with open('inputMaze/'+sys.argv[1],'r') as f:
                tempRow=[]
                for line in f:
                    tempRow.append(line.strip())
            grid=Grid(len(tempRow[0]),len(tempRow))
            for i in range(grid.height):
                for j in range(grid.width):
                    grid.matrix[i][j]=Node(i,j,int(tempRow[i][j]))
            colorama.init()
            startx=int(input('Input row coordinate of start: '))
            starty=int(input('Input column coordinate of start: '))
            endx=int(input('Input row coordinate of goal: '))
            endy=int(input('Input column coordinate of goal: '))
            print('Maze Input')
            grid.print(grid.matrix[startx][starty],grid.matrix[endx][endy])
            print('\nShortest Path using BFS Algorithm')
            start=time()
            result=bfs(grid,startx,starty,endx,endy)
            end=time()
            if(result[1]):
                grid.print(grid.matrix[startx][starty],grid.matrix[endx][endy])
            else:
                print('No path found')
            print('Total Iteration:',result[0])
            print('Time execution using BFS:',end-start,'s')
            grid.reset()
            print('\nShortest Path using A* Algorithm')
            start=time()
            result=astar(grid,startx,starty,endx,endy)
            end=time()
            if(result[1]):
                grid.print(grid.matrix[startx][starty],grid.matrix[endx][endy])
            else:
                print('No path found')
            print('Total Iteration:',result[0])
            print('Time execution using A*:',end-start,'s')
        except:
            print('File',sys.argv[1],'not found')
        
    