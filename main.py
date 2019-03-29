import colorama
import sys
from colorama import Back, Style
from time import time

def valid(grid,curNode,nextX,nextY): #mengecek apakah koordinat dapat dikunjungi
    return (nextX>=0 and nextX<grid.height) and (nextY>=0 and nextY<grid.width) and (not grid.matrix[nextX][nextY] in curNode.predecessor) and (grid.matrix[nextX][nextY].render!=1)

def visit(node1,node2,queue): #mengcopy path sementara dari node1 ke node2
    node2.predecessor=node1.predecessor.copy()
    node2.predecessor.append(node1)
    queue.append(node2)

class Grid: #representasi maze
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.matrix=[]
        for i in range(height):
            self.matrix.append([None]*width)
    def print(self): #cetak ke layar dengan warna
        for i in range(self.height):
            for j in range(self.width):
                if(self.matrix[i][j].render==0):
                    print(Back.WHITE+'  '+Style.RESET_ALL,end='')
                elif(self.matrix[i][j].render==1):
                    print(Back.BLUE+'  '+Style.RESET_ALL,end='')
                elif(self.matrix[i][j].render==2):
                    print(Back.YELLOW+'  '+Style.RESET_ALL,end='')
                elif(self.matrix[i][j].render==3):
                    print(Back.RED+'  '+Style.RESET_ALL,end='')
                elif(self.matrix[i][j].render==4):
                    print(Back.GREEN+'  '+Style.RESET_ALL,end='')
            print()
    def generateManDist(self,goalNode): #menghitung manhattandistance tiap node
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j].manhattandist=abs(i-goalNode.x)+abs(j-goalNode.y)
    def highLightPath(self,goalNode): #memberikan warna tertentu ke node
        goalNode.render=4
        for i in range(len(goalNode.predecessor)):
            goalNode.predecessor[i].render=2
        goalNode.predecessor[0].render=3
    def reset(self): #membuang semua warna hasil highLightPath pada node
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j].visited=False
                if(self.matrix[i][j].render in [2,3,4]):
                    self.matrix[i][j].render=0

class Node: #representasi node
    def __init__(self,x,y,render):
        self.x=x
        self.y=y
        self.render=render
        self.value=0
        self.manhattandist=0
        self.predecessor=[]
        self.visited=False
    def isSameWith(self,otherNode): #operator=
        return self.x==otherNode.x and self.y==otherNode.y
    def setVisited(self,bool):
        self.visited=bool
    def getCost(self): #menghitung f(n)+g(n)
        return self.value+self.manhattandist

class PrioQueue: #representasi priority queue
    def __init__(self):
        self.queue=[]
    def append(self,element): #meletakkan element berdasarkan prioritas
        if(len(self.queue)==0):
            self.queue.append(element)
        else:
            idx=0
            found=False
            while(idx<len(self.queue) and not found):
                if(self.queue[idx].getCost()>=element.getCost()):
                    found=True
                else:
                    idx+=1
            if(found):
                self.queue.insert(idx,element)
            else:
                self.queue.append(element)
    def pop(self): #mengambil sekaligus membuang elemen
        return self.queue.pop(0)
    def removeUnwanted(self,curGoalNode): #membuang elemen2 dengan prioritas lebih rendah dari curGoalNode
        deleteIndex=[]
        for i in range(len(self.queue)-1,-1,-1):
            if(self.queue[i].getCost()>=curGoalNode.getCost()):
                deleteIndex.append(i)
        for i in deleteIndex:
            del self.queue[i]

def bfs(grid,startx,starty,endx,endy): #algoritma BFS, menggunakan queue biasa
    queue=[]
    queue.append(grid.matrix[startx][starty])
    found=False
    count=0
    while(len(queue)>0 and not found): #kunjungi hingga ditemukan jalan
        count+=1
        curNode=queue.pop(0)
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

def astar(grid,startx,starty,endx,endy): #algoritma a*, kunjungi hingga tidak ada node hidup tersisa
    grid.generateManDist(grid.matrix[endx][endy])
    prioQueue=PrioQueue()
    prioQueue.append(grid.matrix[startx][starty])
    found=False
    count=0
    while(len(prioQueue.queue)>0 and not found):
        count+=1
        curNode=prioQueue.pop()
        if(curNode.isSameWith(grid.matrix[endx][endy])):
            curGoalNode=curNode
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
        if(found):
            prioQueue.removeUnwanted(curGoalNode)
    if(found):
        grid.highLightPath(curGoalNode)
    return [count,found]

if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print('Usage: python main.py <inputmaze>')
    else:
        tempRow=[]
        try:
            with open('inputMaze/'+sys.argv[1],'r') as f:
                for line in f:
                    tempRow.append(line.strip())
        except:
            print('File',sys.argv[1],'not found')
            sys.exit(0)
        grid=Grid(len(tempRow[0]),len(tempRow))
        for i in range(grid.height):
            for j in range(grid.width):
                grid.matrix[i][j]=Node(i,j,int(tempRow[i][j]))
        colorama.init()
        print('Maze Input')
        grid.print()
        startx=int(input('Input row coordinate of start: '))
        starty=int(input('Input column coordinate of start: '))
        endx=int(input('Input row coordinate of goal: '))
        endy=int(input('Input column coordinate of goal: '))
        print('\nShortest Path using BFS Algorithm')
        start=time()
        result=bfs(grid,startx,starty,endx,endy)
        end=time()
        if(result[1]):
            grid.print()
            print('Total Iteration:',result[0])
        else:
            print('No path found')
        print('Time execution using BFS:',end-start,'s')
        grid.reset()
        print('\nShortest Path using A* Algorithm')
        start=time()
        result=astar(grid,startx,starty,endx,endy)
        end=time()
        if(result[1]):
            grid.print()
            print('Total Iteration:',result[0])
        else:
            print('No path found')
        print('Time execution using A*:',end-start,'s')
        
    