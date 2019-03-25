def valid(x,y,maxX,maxY):
    return (x>=0 and x<maxX) and (y>=0 and y<maxY)

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

class Node:
    def __init__(self,x,y,render):
        self.x=x
        self.y=y
        self.render=render
        self.value=0
        self.predecessor=[]
    def isSameWith(self,otherNode):
        return self.x==otherNode.x and self.y==otherNode.y
    def highLight(self):
        for i in range(len(self.predecessor)):
            self.predecessor[i].render=2
    def print(self):
        print("     x="+str(self.x)+',y='+str(self.y))

class PrioQueue:
    def __init__(self):
        self.queue=[]
    
    def add(self,element):
        self.queue.append(element)

    def pop(self):
        min=0
        for i in range(len(self.queue)):
            if(self.queue[i].value<self.queue[min].value):
                min=i
        return self.queue.pop(min)
    
def bfs(grid,startx,starty,endx,endy):
    prioQueue=PrioQueue()
    prioQueue.add(grid.matrix[startx][starty])
    found=False
    noPath=False
    while(not found and not noPath):
        if(len(prioQueue.queue)==0):
            noPath=True
        else:
            curNode=prioQueue.pop()
            # print("curnode, x="+str(curNode.x)+', y='+str(curNode.y)+', render='+str(curNode.render))
            if(curNode.isSameWith(grid.matrix[endx][endy])):
                curNode.render=2
                found=True
            else:
                
                try:
                    if((grid.matrix[curNode.x-1][curNode.y].render!=1) and (not grid.matrix[curNode.x-1][curNode.y] in curNode.predecessor) and (valid(curNode.x-1,curNode.y,grid.height,grid.width))):
                        # print("masuk 1")
                        grid.matrix[curNode.x-1][curNode.y].predecessor=grid.matrix[curNode.x-1][curNode.y].predecessor+curNode.predecessor
                        grid.matrix[curNode.x-1][curNode.y].predecessor.append(curNode)
                        prioQueue.add(grid.matrix[curNode.x-1][curNode.y])
                except:
                    continue
                try:
                    if((grid.matrix[curNode.x][curNode.y-1].render!=1) and (not grid.matrix[curNode.x][curNode.y-1] in curNode.predecessor) and (valid(curNode.x,curNode.y-1,grid.height,grid.width))):
                        # print("masuk 2")
                        grid.matrix[curNode.x][curNode.y-1].predecessor=grid.matrix[curNode.x][curNode.y-1].predecessor+curNode.predecessor
                        grid.matrix[curNode.x][curNode.y-1].predecessor.append(curNode)
                        prioQueue.add(grid.matrix[curNode.x][curNode.y-1])
                except:
                    continue
                try:
                    if((grid.matrix[curNode.x][curNode.y+1].render!=1) and (not grid.matrix[curNode.x][curNode.y+1] in curNode.predecessor) and (valid(curNode.x,curNode.y+1,grid.height,grid.width))):
                        # print("masuk 3")
                        grid.matrix[curNode.x][curNode.y+1].predecessor=grid.matrix[curNode.x][curNode.y+1].predecessor + curNode.predecessor
                        grid.matrix[curNode.x][curNode.y+1].predecessor.append(curNode)
                        prioQueue.add(grid.matrix[curNode.x][curNode.y+1])
                except:
                    continue
                try:
                    if((grid.matrix[curNode.x+1][curNode.y].render!=1) and (not grid.matrix[curNode.x+1][curNode.y] in curNode.predecessor) and (valid(curNode.x+1,curNode.y,grid.height,grid.width))):
                        # print("masuk 4")
                        grid.matrix[curNode.x+1][curNode.y].predecessor=grid.matrix[curNode.x+1][curNode.y].predecessor+curNode.predecessor
                        grid.matrix[curNode.x+1][curNode.y].predecessor.append(curNode)
                        prioQueue.add(grid.matrix[curNode.x+1][curNode.y])
                except:
                    continue


if __name__ == "__main__":
    width=int(input())
    height=int(input())
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
    # for i in range(len(grid.matrix[endx][endy].predecessor)):
    #     grid.matrix[endx][endy].predecessor[i].print()
    grid.matrix[endx][endy].highLight()

    grid.print()
    
    
    