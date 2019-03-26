def valid(grid,curNode,nextX,nextY):
    return (nextX>=0 and nextX<grid.height) and (nextY>=0 and nextY<grid.width) and (not grid.matrix[nextX][nextY] in curNode.predecessor) and (grid.matrix[nextX][nextY]!=1)

def visit(node1,node2,queue):
    node2.predecessor+=node1.predecessor
    node2.predecessor.append(node1)
    queue.append(node2)

class Grid:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.matrix=[]
        for i in range(height):
            self.matrix.append([None]*width)
    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.matrix[i][j].render,end='')
            print()
    def generateManDist(self,goalNode):
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j].manhattandist=abs(i-goalNode.x)+abs(j-goalNode.y)

class Node:
    def __init__(self,x,y,render):
        self.x=x
        self.y=y
        self.render=render
        self.value=0
        self.manhattandist=0
        self.predecessor=[]
    def isSameWith(self,otherNode):
        return self.x==otherNode.x and self.y==otherNode.y
    def highLight(self):
        self.render=2
        for i in range(len(self.predecessor)):
            self.predecessor[i].render=2
    # def print(self):
    #     print("     x="+str(self.x)+',y='+str(self.y))
    # def manhattandist(self,otherNode):
    #     return abs(self.x-otherNode.x)+abs(self.y-otherNode.y)

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
    def removeUnwanted(self,curGoalNode):
        deleteIndex=[]
        for i in range(len(self.queue)-1,-1,-1):
            if(self.queue[i].value+self.queue[i].manhattandist>=curGoalNode.value+curGoalNode.manhattandist):
                deleteIndex.append(i)
        for i in deleteIndex:
            del self.queue[i]

def bfs(grid,startx,starty,endx,endy):
    queue=[]
    queue.append(grid.matrix[startx][starty])
    found=False
    while(len(queue)>0 and not found):
        curNode=queue.pop(0)
        # print("curnode, x="+str(curNode.x)+', y='+str(curNode.y)+', render='+str(curNode.render))
        if(curNode.isSameWith(grid.matrix[endx][endy])):
            curNode.highLight()
            found=True
        else:
            if(valid(grid,curNode,curNode.x-1,curNode.y) and not grid.matrix[curNode.x-1][curNode.y] in queue):
                visit(curNode,grid.matrix[curNode.x-1][curNode.y],queue)
            if(valid(grid,curNode,curNode.x,curNode.y-1) and not grid.matrix[curNode.x][curNode.y-1] in queue):
                visit(curNode,grid.matrix[curNode.x][curNode.y-1],queue)
            if(valid(grid,curNode,curNode.x+1,curNode.y) and not grid.matrix[curNode.x+1][curNode.y] in queue):
                visit(curNode,grid.matrix[curNode.x+1][curNode.y],queue)
            if(valid(grid,curNode,curNode.x,curNode.y+1) and not grid.matrix[curNode.x][curNode.y+1] in queue):    
                visit(curNode,grid.matrix[curNode.x][curNode.y+1],queue)


def astar(grid,startx,starty,endx,endy):
    grid.generateManDist(grid.matrix[endx][endy])
    prioQueue=PrioQueue()
    prioQueue.append(grid.matrix[startx][starty])
    found=False
    while(len(prioQueue)>0):
        # print("current prioqueue=")
        # for i in range(len(prioQueue.queue)):
        #     prioQueue.queue[i].print()
        curNode=prioQueue.pop()
        # print(" curnode, x="+str(curNode.x)+', y='+str(curNode.y)+', render='+str(curNode.render))
        if(curNode.isSameWith(grid.matrix[endx][endy])):
            curGoalNode=curNode
            found=True
        else:
            if(valid(grid,curNode,curNode.x-1,curNode.y) and not grid.matrix[curNode.x-1][curNode.y] in prioQueue.queue):
                grid.matrix[curNode.x-1][curNode.y].value=curNode.value+1
                visit(curNode,grid.matrix[curNode.x-1][curNode.y],prioQueue)
            if(valid(grid,curNode,curNode.x,curNode.y-1) and not grid.matrix[curNode.x][curNode.y-1] in prioQueue.queue):
                grid.matrix[curNode.x][curNode.y-1].value=curNode.value+1
                visit(curNode,grid.matrix[curNode.x][curNode.y-1],prioQueue)
            if(valid(grid,curNode,curNode.x+1,curNode.y) and not grid.matrix[curNode.x+1][curNode.y] in prioQueue.queue):
                grid.matrix[curNode.x+1][curNode.y].value=curNode.value+1
                visit(curNode,grid.matrix[curNode.x+1][curNode.y],prioQueue)
            if(valid(grid,curNode,curNode.x,curNode.y+1) and not grid.matrix[curNode.x][curNode.y+1] in prioQueue.queue):    
                grid.matrix[curNode.x][curNode.y+1].value=curNode.value+1
                visit(curNode,grid.matrix[curNode.x][curNode.y+1],prioQueue)
        if (found):
            prioQueue.removeUnwanted(curGoalNode)
    if (found):
        curGoalNode.highLight()


if __name__ == "__main__":
    height=int(input())
    width=int(input())
    grid=Grid(width,height)
    for i in range(height):
        temp=input()
        for j in range(width):
            grid.matrix[i][j]=Node(i,j,int(temp[j]))
    startx=int(input())
    starty=int(input())
    endx=int(input())
    endy=int(input())
    bfs(grid,startx,starty,endx,endy)
    # print("selesai")
    grid.print()
    
    
    