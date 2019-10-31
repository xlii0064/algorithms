class Vertex:
    def __init__(self,u):
        """
        Functionality of the function is to make instance of vertex
        Time complexity:O(1)
        Space complexity:O(1)
        Error handle:None
        Precondition:u must be a number
        :param u: the index number of the vertex to be made
        """
        self.u=u
        self.adj=[]
        self.hasCamera=False
        self.hasService=False
    def addEdge(self,edge):
        """
        Functionality of the function is to add an edge into this vertex's list
        Time complexity:O(1)
        Space complexity:O(1)
        Error handle:None
        Precondition: a vertex instance has been made
        :param edge: the edge to be inserted in the list
        :return: None
        """
        self.adj.append(edge)

    def __str__(self):
        """
        Functionality of the function is to generate all the information in this vertex to a string
        Time complexity:O(len(adj))
        Space complexity:O(1)
        Error handle:None
        Precondition:a vertex instance has been made
        :return: a string that contains all the edges and attributes in this vertex
        """
        string=str(self.u)+"->"+str(self.hasCamera)+"->"
        if len(self.adj)==0:
            return string+"[]"
        for i in range (len(self.adj)-1):
            string+=str(self.adj[i])+","
        string+=str(self.adj[len(self.adj)-1])
        return string
class Edge:
    def __init__(self,u,v,w):
        """
        Functionality of the function is to create an instance of the class Edge
        Time complexity:O(1)
        Space complexity:O(1)
        Error handle:None
        Precondition:u,v,w must be numbers
        :param u: the vertex index which is the starting point
        :param v: the end vertex
        :param w: the weight of this edge
        """
        self.u=u
        self.v = v
        self.w=w
        self.hasToll=False
    def __str__(self):
        """
        Functionality of the function is to generate all the information in this edge to a string
        Time complexity:O(1)
        Space complexity:O(1)
        Error handle:None
        Precondition:an edge instance has been made
        :return: the string that contains all the attributes in this edge
        """
        return "("+str(self.v)+","+str(self.w)+","+str(self.hasToll)+")"
class Graph:
    def __init__(self):
        self.graph=[]
        self.largest=0
        self.serviceList=[]
        self.reverseGraph=[]
        self.reverseGraphLargest=0
    def buildGraph(self,filename_roads):
        """
        Functionality of the function is to generate the graph using the information from the file
        Time complexity:O(E) since all the edges in the file should be inserted in this graph
        Space complexity:O(E) since all the edges in the file should be inserted in this graph
        Error handle: If the file is invalid, print the error message and return
        Precondition:a graph instance has been created
        :param filename_roads: the file that contains all the possible roads
        :return:None
        """
        try:
            open(filename_roads, "r")
        except:
            print("Invalid file")
            return
        file = open(filename_roads, "r")
        lines = file.read().split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].split(" ")
            lines[i][0] = int(lines[i][0])
            lines[i][1] = int(lines[i][1])
            lines[i][2] = float(lines[i][2])
            u=Vertex(lines[i][0])
            edge=Edge(lines[i][0],lines[i][1],lines[i][2])
            self.largest=self.insert(u, edge,self.largest,self.graph)


    def insert(self,vertex,edge,largest,graph):
        """
        Functionality of the function is to insert the new edge into this graph
        Time complexity:O(1) in best case where the vertex to be inserted in already existed.O(v) in the worst case where
        the edge contains the largest vertex in the file and there's nothing in the graph yet
        Space complexity:O(1) in best case where the vertex to be inserted in already existed.O(v) in the worst case where
        the edge contains the largest vertex in the file and there's nothing in the graph yet
        Error handle: None
        Precondition: an instance of the graph has already been created
        :param vertex: where the edge should be inserted in
        :param edge: the edge to be inserted
        :param largest: the largest index of the vertex in the graph
        :param graph: the graph to be inserted in
        :return: the new index of the largest vertex
        """
        if edge.v>=largest:
            for i in range (largest,edge.v+1,1):
                graph.append(Vertex(i))
            largest=edge.v+1
        if vertex.u>=largest:
            for i in range (largest,vertex.u+1,1):
                graph.append(Vertex(i))
            largest=vertex.u+1
        graph[vertex.u].addEdge(edge)
        return largest
    def dijkstra(self,source,target,graph,largest,whole):
        """
        Functionality of the function is to find the shortest path to some the target using dijkstra algorithm
        Time complexity:O(ElogV) since inserting takes O(logV) and for E edges the algorithm would loop through E times
        Space complexity:O(E+V) since the input graph would be O(E+V)
        Error handle:print error message and return if the target and source are not int
        Precondition:the graph instance has been created
        :param source: the start node of the path
        :param target: the end node of the path
        :param graph: the graph to be explored
        :param largest: the largest vertex in the graph
        :param whole: whether the function needs to return a whole finalized list or it can stop as soon as it has finalized
        the target
        :return: a list contains the finalized list, the list contains the index of the vertices in the heap and if it is possible
        to reach the target from source or not
        """
        try:
            source = int(source)
            target = int(target)
        except:
            print("source and target must be numbers")
            return
        possible = False
        discovered = [[source, 0]]
        finalized = []
        vertices = [-2 for _ in range(largest + 1)]
        vertices[source] = 0
        while len(discovered) > 0:
            if vertices[target] == -1:
                possible = True
                if not whole:
                    break
            u = discovered[0][0]
            for edgeIndex in range(len(graph[u].adj)):
                edge = graph[u].adj[edgeIndex]
                vPos = vertices[edge.v]
                uPos = vertices[edge.u]
                if vPos == -2:
                    item = [edge.v, discovered[uPos][1] + edge.w, edge.u]
                    discovered = self.heapInsert(discovered, item, vertices)
                else:
                    if discovered[vPos][1] > discovered[uPos][1] + edge.w:
                        if vPos != -1:
                            discovered[vPos][1] = discovered[uPos][1] + edge.w
                            discovered[vPos][2] = edge.u
            finalized.append(discovered[0])
            self.heapRemoveSmallest(discovered, vertices)
        return [finalized,vertices,possible]
    def quickestPath(self,source,target):
        """
        Functionality of the function is to find the shortest path from the source to the target
        Time complexity:O(ElogV) since inserting takes O(logV) and for E edges the algorithm would loop through E times
        Space complexity:O(E+V) since the input graph would be O(E+V)
        Error handle:print error message and return if the target and source are not int
        Precondition:the graph instance has been created
        :param source:the start node of the path
        :param target: the end node of the path
        :return: return [[],-1] if it is impossible to reach target from source. Else return (path,time)
        """
        try:
            source = int(source)
            target = int(target)
        except:
            print("source and target must be numbers")
        result=self.dijkstra(source,target,self.graph,self.largest,False)
        finalized=result[0]
        vertices=result[1]
        possible=result[2]
        if vertices[target] == -1:
            possible = True
        if possible:
            quickest=self.findPath(finalized,source)
        else:
            return [[],-1]
        time=finalized[len(finalized)-1][1]
        return (quickest,time)
    def heapInsert(self,heap,item,vertices):
        """
        Functionality of the function is to insert the item into the heap
        Time complexity:O(logv) for worst case and O(1) for best case where the item is the largest one in the heap
        Space complexity:O(v) for the list vertices
        Error handle:None
        Precondition:the heap must be a valid min heap
        :param heap: where the item should be inserted in
        :param item: the item to insert
        :param vertices: the vertices' list that contains all indexes of the vertices in the heap
        :return: return a heap that contains the newly added item
        """
        heap.append(item)
        if (len(heap))==1:
            vertices[item[0]]=0
            return heap
        vertices[item[0]]=len(heap)-1
        index=len(heap)-1
        parent=(index-1)//2
        while parent>=0:
            if heap[index][1]<heap[parent][1]:
                heap[index],heap[parent]=heap[parent],heap[index]
                vertices[heap[index][0]],vertices[heap[parent][0]]=vertices[heap[parent][0]],vertices[heap[index][0]]
                index=parent
                parent=(index-1)//2
            else:
                break
        vertices[item[0]]=index
        return heap

    def heapRemoveSmallest(self,heap,vertices):
        """
        Functionality of the function is to remove the smallest one in the heap
        Time complexity:O(logv) for worst case and O(1) for best case where the all the values in the heap are all the same
        Space complexity:O(v) for the list vertices
        Error handle: None
        Precondition: the heap is a min heap
        :param heap: the heap to be removed the smallest
        :param vertices: the vertices' list that contains all indexes of the vertices in the heap
        :return: None
        """
        vertices[heap[0][0]]=-1
        if len(heap)==1:
            heap.pop()
            return
        vertices[heap[len(heap)-1][0]] =0
        heap[0]=heap[len(heap)-1]
        heap.pop()
        if len(heap)>0:
            self.down(heap,0,vertices)
    def down(self, heap, index, vertices):
        """
        Functionality of the function is to move down the node until it is a valid heap
        Time complexity:O(logv) for worst case and O(1) for best case where the all the values in the heap are all the same
        Space complexity:O(v) for the list vertices
        Error handle: None
        Precondition: the list vertices contains all the correct indexes of the vertices in the heap
        :param heap: the heap to be modified
        :param index: the index of the node to be adjusted
        :param vertices:the vertices' list that contains all indexes of the vertices in the heap
        :return: None
        """
        left=index*2+1
        right=index*2+2
        if right>=len(heap):
            if left>=len(heap):
                return heap
            else:
                minIdex=left
        else:
            if heap[left][1]<=heap[right][1]:
                minIdex=left
            else:
                minIdex=right
        if heap[index][1]>heap[minIdex][1]:
            heap[index],heap[minIdex]=heap[minIdex],heap[index]
            vertices[heap[index][0]], vertices[heap[minIdex][0]]= vertices[heap[minIdex][0]], vertices[heap[index][0]]
            self.down(heap, minIdex, vertices)

    def findPath(self,final,source):
        """
        Functionality of the function is to find all the vertices that made the shortest path
        Time complexity:O(V) in the worst case and O(1) in the best case where the target directly connects with the source node
        Space complexity:O(V) same as the input final list
        Error handle:None
        Precondition: the source node is in the final list
        :param final: the list that contains all the possible nodes in the shortest path
        :param source: the source node that starts the path
        :return: a list that contains all the nodes of the shortest path
        """
        index=len(final)-1
        result = [final[index][0]]
        if index==0:
            return result
        prev=final[index][2]
        while final[index][0]!=source:
            #O(V)
            if final[index][0]==prev:
                result.append(prev)
                prev=final[index][2]
            index-=1
        result.append(source)
        result.reverse()
        return result

    def augmentGraph(self,filename_camera,filename_toll):
        """
        Functionality of the function is to generate the graph so it can indicate if a vertex has cameras or an edge has tolls
        Time complexity: O(E) since it needs to go through every edge to generate the graph
        Space complexity: O(E+V) same as the input graph
        Error handle:print error message and return if the file is invalid
        Precondition: a graph that contains all the nodes in the file has been created
        :param filename_camera: the file that contains all the nodes that has cameras
        :param filename_toll: the file that contains all the edges that has tolls
        :return: None
        """
        try:
            open(filename_toll, "r")
            open(filename_camera,"r")
        except:
            print("Invalid file")
            return
        camera_file = open(filename_camera, "r")
        cameras = camera_file.read().split("\n")
        toll_file = open(filename_toll, "r")
        tolls = toll_file.read().split("\n")
        for index in range(len(cameras)):
            cameras[index]=int(cameras[index])
            vertexIndex=cameras[index]
            self.graph[vertexIndex].hasCamera=True
        for index in range (len(tolls)):
            tolls[index]=tolls[index].split(" ")
            tolls[index][0]=int(tolls[index][0])
            tolls[index][1] = int(tolls[index][1])
            uIndex=tolls[index][0]
            vIndex=tolls[index][1]
            for edge in range (len(self.graph[uIndex].adj)):
                if self.graph[uIndex].adj[edge].v ==vIndex:
                    self.graph[uIndex].adj[edge].hasToll=True
    def quickestSafePath(self,source,target):
        """
        Functionality of the function is to find the shortest from the source to the target that doesn't contain any cameras
        or tolls
        Time complexity:O(ElogV) since dijkstra using min heap will use O(ElogV) time
        Space complexity: O(E+V) same as the input graph
        print error message and return if the target and source are not int
        Precondition:the graph instance has been created
        :param source:the start node of the path
        :param target: the end node of the path
        :return: return [[],-1] if it is impossible to reach target from source. Else return (path,time)
        """
        try:
            source = int(source)
            target = int(target)
        except:
            print("source and target must be numbers")
        possible=False
        discovered=[[source,0]]
        finalized=[]
        vertices=[-2 for i in range (self.largest+1)]
        vertices[source]=0
        while len(discovered)>0:
            if vertices[target]==-1:
                possible=True
                break
            u=discovered[0][0]
            for edgeIndex in range (len(self.graph[u].adj)):
                edge=self.graph[u].adj[edgeIndex]
                vPos = vertices[edge.v]
                uPos = vertices[edge.u]
                #if u and v don't have cameras and this edge doesn't have a toll
                valid=self.graph[u].hasCamera==False and edge.hasToll==False and self.graph[edge.v].hasCamera==False

                if vPos==-2 and valid:
                    item=[edge.v,discovered[uPos][1]+edge.w,edge.u]
                    discovered=self.heapInsert(discovered,item,vertices)
                else:
                    if valid:
                        if discovered[vPos][1]>discovered[uPos][1]+edge.w:
                            if vPos!=-1:
                                discovered[vPos][1]=discovered[uPos][1]+edge.w
                                discovered[vPos][2]=edge.u
            finalized.append(discovered[0])
            self.heapRemoveSmallest(discovered,vertices)
        if vertices[target] == -1:
            possible = True
        if possible:
            quickest=self.findPath(finalized,source)
        else:
            return [[],-1]
        time=finalized[len(finalized)-1][1]
        return (quickest,time)
    def  addService(self, filename_service):
        """
        Functionality of the function is to add the service to the graph according to the file and generate a reverse graph
        Time complexity:O(E) for generating a reverse graph
        Space complexity:O(V+E) same as the input graph
        Error handle: print error message and return if the file is invalid
        Precondition: a graph that contains all the nodes in the file has been created
        :param filename_service: the file that contains all the service points
        :return: None
        """
        try:
            open(filename_service, "r")
        except:
            print("Invalid file")
            return
        service_file = open(filename_service, "r")
        services = service_file.read().split("\n")
        self.serviceList=services
        for index in range (len(services)):
            services[index]=int(services[index])
            servicePos=services[index]
            self.graph[servicePos].hasService=True
        for vertexIndex in range(len(self.graph)):
            for edge in self.graph[vertexIndex].adj:
                u = Vertex(edge.v)
                e=Edge(edge.v,edge.u,edge.w)
                self.reverseGraphLargest= self.insert(u,e,self.reverseGraphLargest,self.reverseGraph)


    def quickestDetourPath(self, source, target):
        """
        Functionality of the function is to find the shortest path that contains at least one node that has services
        Time complexity:O(Elogv) since the dijkstra would take ElogV time and other loops take V time which is less than ElogV
        Space complexity:O(E+V) since the input graph would be O(E+V)
        Error handle: print error message and return if one of the source and target is not a number
        Precondition: a graph that contains source and target has been made
        :param source: the source node to start the path
        :param target: the end node of the path
        :return: return [[],-1] if it is impossible to reach target from source. Else return (path,time)
        """
        try:
            source = int(source)
            target = int(target)
        except:
            print("source and target must be numbers")
        #O(ElogV)
        result=self.dijkstra(source,target,self.graph,self.largest,True)
        finalized=result[0]
        result2=self.dijkstra(target,source,self.reverseGraph,self.reverseGraphLargest,True)
        reverseFinalized=result2[0]
        newFinalized=[0 for _ in range(len(self.graph))]
        for index in range (len(finalized)):
            #O(V)
            vertexID=finalized[index][0]
            newFinalized[vertexID]=finalized[index]
        newReverseFinalized=[0 for _ in range(len(self.graph))]
        for index in range (len(reverseFinalized)):
            #O(V)
            vertexID=reverseFinalized[index][0]
            newReverseFinalized[vertexID]=reverseFinalized[index]
        path=[0 for _ in range (len(self.graph))]
        for item in range (len(newFinalized)):
            #O(V)
            if newFinalized[item]!=0 and newReverseFinalized[item]!=0:
                newFinalized[item][1]+=newReverseFinalized[item][1]
                path[item]=newFinalized[item]

        minTime=0
        minTimeServicePoint=0
        found=False
        for vertices in range (len(path)):
            #O(V)
            if path[vertices]==0:
                continue
            vertexId=path[vertices][0]
            if self.graph[vertexId].hasService and not found:
                minTime=path[vertices][1]
                minTimeServicePoint=vertexId
                found=True
            if self.graph[vertexId].hasService and path[vertices][1]<minTime:
                minTime=path[vertices][1]
                minTimeServicePoint=vertexId
        for num in range (len(finalized)):
            #O(V)
            if finalized[num][0]==minTimeServicePoint:
                finalized=finalized[:num+1]
                break
        for num in range (len(reverseFinalized)):
            #O(V)
            if reverseFinalized[num][0]==minTimeServicePoint:
                reverseFinalized=reverseFinalized[:num+1]
                break
        if not found:
            return [[],-1]
        else:
            #O(V)
            front=self.findPath(finalized,source)
            end=self.findPath(reverseFinalized,target)
            end.pop()
            end.reverse()
            whole=front+end
            return (whole,minTime)
    def __str__(self):
        string=""
        for i in self.graph:
            string+=str(i)+"\n"
        return string
    def printByRequirments(self,result):
        output=""
        if result==[[],-1]:
            return "No path exists\nTime: 0 minute(s)"
        path=result[0]
        time=result[1]
        for i in range (len(path)-1):
            output+=str(path[i])+"-->"
        output+=str(path[len(path)-1])+"\nTime: "+str(time)+" minute(s)"
        return output
if __name__=="__main__":
    g=Graph()
    file_road=input("Enter the file name for the graph: ")
    g.buildGraph(file_road)
    file_camera=input("Enter the file name for camera nodes:")
    file_toll=input("Enter the file name for the toll roads:")
    file_service=input("Enter the file name for the service nodes:")
    source=input("Source node:")
    target=input("Sink node:")
    quickest=g.quickestPath(source,target)
    g.augmentGraph(file_camera,file_toll)
    safest=g.quickestSafePath(source,target)
    g.addService(file_service)
    detour=g.quickestDetourPath(source,target)
    print("Quickest path:")
    print(g.printByRequirments(quickest))
    print("Safe quickest path:")
    print(g.printByRequirments(safest))
    print("Quickest detour path:")
    print(g.printByRequirments(detour))
