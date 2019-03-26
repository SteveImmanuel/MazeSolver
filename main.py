def valid(x,y,maxX,maxY):
    return (x>=0 and x<maxX) and (y>=0 and y<maxY)

def visit(node1,node2,queue):
    if((node2.render!=1) and (not node2 in node1.predecessor) and (not node2 in queue)):
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
    
def bfs(grid,startx,starty,endx,endy):
    queue=[]
    queue.append(grid.matrix[startx][starty])
    found=False
    pathExist=True

    while(not found and pathExist):
        print("current queue=")
        for i in range(len(queue)):
            queue[i].print()
        if(len(queue)==0):
            pathExist=False
        else:
            curNode=queue.pop(0)
            print("curnode, x="+str(curNode.x)+', y='+str(curNode.y)+', render='+str(curNode.render))
            if(curNode.isSameWith(grid.matrix[endx][endy])):
                curNode.highLight()
                found=True
            else:
                if(valid(curNode.x-1,curNode.y,grid.height,grid.width)):
                    visit(curNode,grid.matrix[curNode.x-1][curNode.y],queue)
                if(valid(curNode.x,curNode.y-1,grid.height,grid.width)):
                    visit(curNode,grid.matrix[curNode.x][curNode.y-1],queue)
                if(valid(curNode.x+1,curNode.y,grid.height,grid.width)):
                    visit(curNode,grid.matrix[curNode.x+1][curNode.y],queue)
                if(valid(curNode.x,curNode.y+1,grid.height,grid.width)):    
                    visit(curNode,grid.matrix[curNode.x][curNode.y+1],queue)
    return pathExist


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
        print(" curnode, x="+str(curNode.x)+', y='+str(curNode.y)+', render='+str(curNode.render))
        if(curNode.isSameWith(grid.matrix[endx][endy])):
            curNode.render=2
            found=True
        else:
            if(valid(curNode.x-1,curNode.y,grid.height,grid.width)):
                grid.matrix[curNode.x-1][curNode.y].value=curNode.value+1
                prioQueue.add(grid.matrix[curNode.x-1][curNode.y])
            if((grid.matrix[curNode.x][curNode.y-1].render!=1) and (not grid.matrix[curNode.x][curNode.y-1] in curNode.predecessor) and (valid(curNode.x,curNode.y-1,grid.height,grid.width))):
                # print("masuk 2")
                grid.matrix[curNode.x][curNode.y-1].predecessor=grid.matrix[curNode.x][curNode.y-1].predecessor+curNode.predecessor
                grid.matrix[curNode.x][curNode.y-1].predecessor.append(curNode)
                grid.matrix[curNode.x][curNode.y-1].value=curNode.value+1
                prioQueue.add(grid.matrix[curNode.x][curNode.y-1])
            if((grid.matrix[curNode.x][curNode.y+1].render!=1) and (not grid.matrix[curNode.x][curNode.y+1] in curNode.predecessor) and (valid(curNode.x,curNode.y+1,grid.height,grid.width))):
                # print("masuk 3")
                grid.matrix[curNode.x][curNode.y+1].predecessor=grid.matrix[curNode.x][curNode.y+1].predecessor + curNode.predecessor
                grid.matrix[curNode.x][curNode.y+1].predecessor.append(curNode)
                grid.matrix[curNode.x][curNode.y+1].value=curNode.value+1
                prioQueue.add(grid.matrix[curNode.x][curNode.y+1])
            if((grid.matrix[curNode.x+1][curNode.y].render!=1) and (not grid.matrix[curNode.x+1][curNode.y] in curNode.predecessor) and (valid(curNode.x+1,curNode.y,grid.height,grid.width))):
                # print("masuk 4")
                grid.matrix[curNode.x+1][curNode.y].predecessor=grid.matrix[curNode.x+1][curNode.y].predecessor+curNode.predecessor
                grid.matrix[curNode.x+1][curNode.y].predecessor.append(curNode)
                grid.matrix[curNode.x+1][curNode.y].value=curNode.value+1
                prioQueue.add(grid.matrix[curNode.x+1][curNode.y])


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
    print("selesai")

    grid.print()
    
    
    