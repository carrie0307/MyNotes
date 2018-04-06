# -*- coding: utf-8 -*-
"""
    python实现图与dfs,bfs
    From: https://www.cnblogs.com/yupeng/p/3414736.html

    学习的点：
        1. 图的存储形式
        2. dfs,bfs思想与实现
"""

class Graph(object):

    def __init__(self,*args,**kwargs):
        self.node_neighbors = {} # 此处图的存储形式是:{a:a1,ba,a3,b:a1,b2,...}表示点a的邻接点有a1,ba,a3,点b的邻接点有a1,b2,...;self.node_neighbors.keys()就是所有的点
        self.visited = {}

    def add_nodes(self,nodelist):

        for node in nodelist:
            self.add_node(node)

    def add_node(self,node):
        if not node in self.nodes():
            self.node_neighbors[node] = []

    def add_edge(self,edge):
        # 给点u,v之间添加边的本质就是，再node_neighbors[u]中添加上v,再noer_neighbors[v]中添加上u
        u,v = edge
        if(v not in self.node_neighbors[u]) and ( u not in self.node_neighbors[v]):
            self.node_neighbors[u].append(v)

            if(u!=v):
                self.node_neighbors[v].append(u)

    def nodes(self):
        # 获取所有的节点，根据初始化中图的定义方式，返回self.node_neighbors.keys()即可
        return self.node_neighbors.keys()

    def depth_first_search(self,root=None):
        order = []
        def dfs(node):
            self.visited[node] = True
            order.append(node)
            for n in self.node_neighbors[node]:
                if not n in self.visited:
                    dfs(n)

        if root:
            dfs(root)

        for node in self.nodes():
            if not node in self.visited:
                dfs(node)

        print order
        return order

    def breadth_first_search(self,root=None):
        queue = [] # 将访问queue中每个节点的子节点
        order = []
        def bfs():
            while len(queue)> 0:
                # 得到当前要访问的点node
                node  = queue.pop(0)

                self.visited[node] = True
                for n in self.node_neighbors[node]:
                    # n是node的子节点
                    if (not n in self.visited) and (not n in queue):
                        # 将n(即当前node的子节点添加到待遍历队列queue中)
                        queue.append(n)
                        # order记录了访问的顺序
                        order.append(n)


        if root:
            queue.append(root)
            order.append(root)
            bfs()

        # 防止root为空或有孤立点的情况(如果是二叉树，则可以忽略这种情况) / 或直接遍历所有的点
        for node in self.nodes():
            if not node in self.visited:
                queue.append(node)
                order.append(node)
                bfs()
        return order

    def breadth_first_search_2(self,root=None):
        '''
        另一种bfs的方法
        '''
        queue = [] # queue中的结点是将要被遍历子结点的结点
        order = []

        for node in self.nodes():
            # 直接先遍列所有的结点
            if node not in self.visited:
                queue.append(node) # 该结点入队列
                order.append(node) # 访问该结点
                self.visited[node] = True

            while len(queue) > 0:
                cur_node = queue.pop(0)

                for sub_node in self.node_neighbors[cur_node]:
                    if sub_node not in self.visited and sub_node not in queue:
                        self.visited[sub_node] = True
                        order.append(sub_node)
                        queue.append(sub_node)

        return order




if __name__ == '__main__':
    g = Graph()
g.add_nodes([i+1 for i in range(8)])
g.add_edge((1, 2))
g.add_edge((1, 3))
g.add_edge((2, 4))
g.add_edge((2, 5))
g.add_edge((4, 8))
g.add_edge((5, 8))
g.add_edge((3, 6))
g.add_edge((3, 7))
g.add_edge((6, 7))
print "nodes:", g.nodes()

# order = g.breadth_first_search(1)
# print 'bfs1:', order
order = g.breadth_first_search_2(1)
print 'bf2:', order
# order = g.depth_first_search(1)
