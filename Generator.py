from config import configs
import os
import shutil
# import sys
import random
import json
import math

# Todo : Re generate the scenario in case liveness is not guaranteed 
class TestGenerator():


    # read the config and load all the values
    def setup(self, config, config_id):
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
        self.test_type = str(config['test_type'])
        self.exclusion_dict = config['exclusion_list']
        
        # Things to Remove
        self.nclients = int(config['nclients'])
        self.nclientops = int(config['nclientops'])
        self.sleeptime = int(config['sleeptime'])
        self.clienttimeout = int(config['clienttimeout'])
        self.delta = int(config['delta'])
        self.window_size = int(config['window_size'])
        self.exclude_size = int(config['exclude_size'])
        # Things to Remove

        self.config_id = config_id
        self.main()


    def main(self):
        leader_limit = int(math.ceil(self.limit_step_2/self.limit_step_1))
        self.partition_list = self.partitionGenerator(self.nodes, self.partition_size, self.limit_step_1)
        self.leader_list = self.get_leader(self.all_leaders, self.nodes, self.node_to_twin_dict, leader_limit)
        self.generate_test_cases(self.config_id, self.partition_list, self.leader_list, self.limit_step_3, self.nbr_of_rounds, self.test_type)


            
    def generate_nodes(self, n):
        nodes_list = [chr(i) for i in range(ord('A'),ord('A')+n)]
        return nodes_list
    

    # l : boolean flag ( True : all nodes can be leader, False : Only Faulty Nodes can be leader )
    # nodes : list of nodes excluding the twins
    # node_to_twin_dict : Mapping from node to twin ( if it exists )
    def get_leader( self, l, nodes, node_to_twin_dict, leader_limit):
        list_of_leader = []
        if l == True:
            for node in nodes[0:self.nvalidators]:
                if node in node_to_twin_dict:
                    list_of_leader.append([node, node_to_twin_dict[node]])
                else:
                    list_of_leader.append([node])
        else:
            for node in node_to_twin_dict:
                list_of_leader.append([node, node_to_twin_dict[node]]) # Only nodes with twin will be made as leaders
        return list_of_leader[0:leader_limit]

    
    # partition_list : list of all the partitions possible
    # leader_list : list of leaders possible
    # nbr_of_rounds : Number of rounds for each test case
    # test_type : indicates deterministic or randon 
    def generate_test_cases(self, config_id, partition_list, leader_list, nbr_of_scenario, nbr_of_rounds, test_type):
        partition_index = 0
        leader_index = -1
        os.mkdir('scenario/'+ str(config_id) + '/')
        for scenario_nbr in range(1, nbr_of_scenario+1):
            test_dict = {}
            test_dict['round_partitions'] = {}
            for round in range(nbr_of_rounds):
                round_dict = {}
                if test_type == 'DETERMINISTIC':
                    if leader_index == len(leader_list) - 1:  # go to next partition if all possible leader-partition pair is created for current partition
                        partition_index = partition_index + 1
                    leader_index = ( leader_index + 1 ) % len(leader_list)
                else :
                    leader_index = random.randint(0, len(leader_list)-1)
                    partition_index = random.randint(0, len(partition_list)-1)
                leader = leader_list[leader_index] 
                partition = partition_list[partition_index]
                round_dict['Leader'] = leader
                round_dict['Partition'] = partition
                test_dict['round_partitions'][round] = round_dict
                test_dict['exclusion_flag'] = 0
            live = self.check_liveness(test_dict)
            # print("Liveness - config_id : ", config_id, " Scenario id : ", scenario_nbr, " Live : ", live)
            self.generate_intra_partition_exclude_list()
            self.add_generic_details_to_scenario(test_dict)
            file_path = os.getcwd()
            with open(file_path + '/scenario/'+ str(config_id) + '/'+ str(scenario_nbr) + '.json', 'a+') as scene_file:
                json.dump(test_dict, scene_file, indent=4)



    # To partition input of (x, y) where x is the number of input elements and y is the number of partitions, we can do that in two steps: 
    # Scenario 1: Partition the input (x-1, y-1) and add xth element to another partition
    # Scenario 2: Partition the input (x-1, y) and add xth element to one of the y partitions. So, this can be done y times
    def partitionGenerator(self, inputList, numberOfPartitions, limit_1):
        result = []
        if len(inputList) < numberOfPartitions or  numberOfPartitions < 1 :
            return result
        if numberOfPartitions == 1:
            partition = []
            partition.append(inputList[:])
            result.append(partition)
            return result
        sets = []
        sets.append(inputList[len(inputList)-1])
        #Partition the input to size (x-1, y-1)
        secondPartition = self.partitionGenerator(inputList[0:len(inputList)-1], numberOfPartitions-1, limit_1)
        for i in range(len(secondPartition)):
            tempList = secondPartition[i]
            l = tempList[:]
            l.append(sets)
            result.append(l)
        # Partition the elements to size (x-1, y) by calling the function recursively   
        firstPartition = self.partitionGenerator(inputList[0:len(inputList)-1], numberOfPartitions, limit_1)
        for i in range(len(firstPartition)):
            for j in range(len(firstPartition[i])):
                l = []
                for lst in firstPartition[i]:
                    l.append(lst[:])
                l[j].append(inputList[len(inputList)-1])
                result.append(l) 
        return result[:limit_1]    
    

    # Exclusion list will be read from the Config file
    # Append to Exclusion list to Block all the messages node and its twin
    def generate_intra_partition_exclude_list(self):
        for i in range(self.nbr_of_rounds):
            if str(i) not in self.exclusion_dict:
                self.exclusion_dict[str(i)] = {}
            
            for node, twin in self.node_to_twin_dict.items():
                if node not in self.exclusion_dict[str(i)]:
                    self.exclusion_dict[str(i)][node] = {}
                if twin not in self.exclusion_dict[str(i)]:
                    self.exclusion_dict[str(i)][twin] = {}
                if  twin not in self.exclusion_dict[str(i)][node]:
                    self.exclusion_dict[str(i)][node][twin] = {}
                if node not in self.exclusion_dict[str(i)][twin]:
                    self.exclusion_dict[str(i)][twin][node] = {}
                
                self.exclusion_dict[str(i)][node][twin]["messageType"] = "*"
                self.exclusion_dict[str(i)][twin][node]["messageType"] = "*"
                

    def add_generic_details_to_scenario(self, scenario_dict):
        scenario_dict['nvalidators'] = self.nvalidators
        scenario_dict['ntwins'] = self.nfaulty
        scenario_dict['exclusion'] = self.exclusion_dict
        scenario_dict['twin_mapping'] = self.node_to_twin_dict

        scenario_dict['nfaulty'] = self.nfaulty
        scenario_dict['nclients'] = self.nclients
        scenario_dict['nclientops'] = self.nclientops
        scenario_dict['sleeptime'] = self.sleeptime
        scenario_dict['clienttimeout'] = self.clienttimeout
        scenario_dict['delta'] = self.delta
        scenario_dict['window_size'] = self.window_size
        scenario_dict['exclude_size'] = self.exclude_size


    def check_liveness(self, scenario_dict):
        idx = -10
        partition = scenario_dict['round_partitions']
        for round in sorted(partition):
            found = False
            for lst in partition[round]['Partition']:
                if len(lst) >= (2 * self.nfaulty + 1):
                    found = True
            if found == False:
                idx = -10
            else:
                if idx == -10:
                    idx = int(round)
                else:
                    if int(round) - idx + 1 == 3: #  2*f+1 partition size can be reached in 3 consecutive rounds
                        return True

        return False

if __name__ == '__main__':
    
    path = os.getcwd()

    if os.path.exists(path + '/scenario/') and os.path.isdir(path + '/scenario/'):
        shutil.rmtree(path + '/scenario/')

    os.mkdir('scenario/')

    tg = TestGenerator()
    for i,config in enumerate(configs, start = 1):
        tg.setup(config, i)

    # # -------------------------------- Test get_leader ----------------------------------------
    # l = True
    # nodes = ['A', 'B', 'C', 'D', 'E']
    # node_to_twin_dict = {}
    # node_to_twin_dict['A'] = 'E'
    # leader_limit = 4
    # # myList = TestGenerator.get_leader(l, nodes, node_to_twin_dict, leader_limit)
    # # print(myList)

    # l = False
    # nodes = ['A', 'B', 'C', 'D', 'E', 'F']
    # node_to_twin_dict = {}
    # node_to_twin_dict['A'] = 'E'
    # node_to_twin_dict['B'] = 'F'
    # leader_limit = 4
    # # myList = TestGenerator.get_leader(l, nodes, node_to_twin_dict, leader_limit)
    # # print(myList)
    # # -----------------------------------------------------------------------------------------

    # # print(TestGenerator.generate_nodes(5))
    

    # # -----------------------------------------------------------------------------------------
    # # Test PartitionGenerator
    # # inputList = []
    # # for i in range(1,5):
    # #     inputList.append(i)
    # # numberOfPartitions = 2
    # # partitionList = TestGenerator.partitionGenerator(inputList, numberOfPartitions)
    # # print("Generated Partitions ", partitionList)
    # # print(partitionList)
    # # if (len(partitionList) != 7):
    # #     print("Partition generation Missing")