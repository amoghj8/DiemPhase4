from config import configs

class TestGenerator:
    
    # l : boolean flag ( True : all nodes can be leader, False : Only Faulty Nodes can be leader )
    # nodes : list of nodes excluding the twins
    # node_to_twin_dict : Mapping from node to twin ( if it exists )
    def get_leader( l, nodes, node_to_twin_dict, leader_limit):
        list_of_leader = []
        if l == True:
            for node in nodes:
                if node in node_to_twin_dict:
                    list_of_leader.append([node, node_to_twin_dict[node]])
                else:
                    list_of_leader.append([node])
        else:
            for node in node_to_twin_dict:
                list_of_leader.append([node, node_to_twin_dict[node]]) # Only nodes with twin will be made as leaders
        return list_of_leader[0:leader_limit]

    
    # read the cofig and load all the values
    def setup(self, config):
        self.nvalidators = int(config['nvalidators'])
        self.nfaulty = int(config['nfaulty'])
        self.nodes = self.generate_nodes(self.nvalidators + self.nfaulty)
        self.node_to_twin_dict = {}
        for i in range(0, self.nfaulty):
            self.node_to_twin_dict[self.nodes[i]] = self.nodes[i+self.nvalidators]
        self.all_leaders = bool(config['all_leaders'])
        self.partition_size = int(config['partition_size'])
        self.nbr_of_rounds = int(config['nbr_of_rounds'])
        self.limit_step_1 = int(config['limit_step_1'])
        self.limit_step_2 = int(config['limit_step_2'])
        self.limit_step_3 = int(config['limit_step_3'])

        print('List of Nodes : ', self.nodes)
        print('Node to Twin Mapping : ', self.node_to_twin_dict)
        print('All Nodes Can be leader : ', self.all_leaders)
        print('Partition Size   : ', self.partition_size)
        print('Number of rounds : ', self.nbr_of_rounds)
        print('Limit for Step 1 : ', self.limit_step_1)
        print('Limit for step 2 : ', self.limit_step_2)
        print('Limit for step 3 : ', self.limit_step_3)
        
        
    def generate_nodes(self, n):
        nodes_list = [chr(i) for i in range(ord('A'),ord('A')+n)]
        return nodes_list

    

if __name__ == '__main__':
    
    # -------------------------------- Test get_leader ----------------------------------------
    l = True
    nodes = ['A', 'B', 'C', 'D', 'E']
    node_to_twin_dict = {}
    node_to_twin_dict['A'] = 'E'
    leader_limit = 4
    myList = TestGenerator.get_leader(l, nodes, node_to_twin_dict, leader_limit)
    print(myList)

    l = False
    nodes = ['A', 'B', 'C', 'D', 'E', 'F']
    node_to_twin_dict = {}
    node_to_twin_dict['A'] = 'E'
    node_to_twin_dict['B'] = 'F'
    leader_limit = 4
    myList = TestGenerator.get_leader(l, nodes, node_to_twin_dict, leader_limit)
    print(myList)
    # -----------------------------------------------------------------------------------------

    # print(TestGenerator.generate_nodes(5))
    tg = TestGenerator()
    
    for config in configs:
        tg.setup(config)