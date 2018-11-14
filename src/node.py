#encode:utf-8
'''
node
'''

Inf = float('Inf')

class Node(object):
    _nid = 0
    def __init__(self, pos):
        Node._nid += 1
        self.nid = Node._nid
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
        pass
    def __str__(self):
        return '{{nid: {}, pos: ({}, {})}}'.format(self.nid, self.x, self.y)
    pass # end Node

class Connection(object):
    def __init__(self, a: Node, b: Node, d: float):
        self.a = a# one
        self.b = b# the other
        self.d = d# distance
        pass
    def __str__(self):
        return '{{a: {}, b: {}, d: {}}}'.format(self.a, self.b, self.d)
    pass # end Connection

class Dijkstra(object):
    def __init__(self):
        self.grid: [Connection] = []
        ''' self.grid
        # see: tmp/20180110150356774.gif
        [
            {a:1,b:2,d:7},
                {a:1,b:3,d:9},
                {a:2,b:3,d:10},
                {a:2,b:4,d:15},
                {a:3,b:4,d:11},
                {a:4,b:5,d:6},
                {a:1,b:6,d:14},
                {a:3,b:6,d:2},
                {a:5,b:6,d:9},
        ]
        '''
        pass

    def add(self, connection: Connection):
        self.grid.append(connection)
        pass

    def remove(self, node: Node):
        remove = []
        for g in self.grid:
            if g.a.nid == node.nid or g.b.nid == node.nid:
                remove.append(g)
        for r in remove:
            self.grid.remove(r)
        pass

    def get_connection(self, a: Node, b: Node):
        r = list(filter(lambda c: c.a.nid == a.nid and c.b.nid == b.nid, self.grid))
        if r:
            return r[0]
        r = list(filter(lambda c: c.a.nid == b.nid and c.b.nid == a.nid, self.grid))
        if r:
            return r[0]
        return None

    def run(self, node1, node2):
        path = []
        vmap = {}
        left = [node1]
        nodes = list(set([c.a for c in self.grid]).union(set([c.b for c in self.grid])))
        for node in nodes:
            if node.nid not in vmap:
                if node.nid == node1.nid:
                    vmap[node.nid] = {'d': 0, 'from': None}
                else:
                    vmap[node.nid] = {'d': Inf, 'from': None}
                    left.append(node)
        while left:
            cur = min(left, key=lambda v: vmap[v.nid]['d'])
            if cur == node2:
                path = [cur]
                break
            left.remove(cur)
            for l in left:
                c = self.get_connection(cur, l)
                if not c:
                    continue
                d = vmap[cur.nid]['d'] + c.d
                if d < vmap[l.nid]['d']:
                    vmap[l.nid] = {'d': d, 'from': cur}
        while True:
            pre = vmap[path[-1].nid]['from']
            if pre:
                path.append(pre)
            else:
                break
        path.reverse()
        return path

    pass # end Dijkstra

def distance(a: Node, b: Node):
    dx = a.x - b.x
    dy = a.y - b.y
    return pow(dx * dx + dy * dy, 0.5)

def test():
    nodes = []
    for i in range(3):
        for j in range(3):
            n = Node((i+1, j+1))
            nodes.append(n)

    dij = Dijkstra()

    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            a = nodes[i]
            b = nodes[j]
            d = distance(a, b)
            if d <= 1.1:#1.414
                c = Connection(a, b, d)
                dij.add(c)

    path = dij.run(nodes[0], nodes[7])

    print('path = ', [n.nid for n in path])
    pass

if __name__ == '__main__':
    test()
    pass
