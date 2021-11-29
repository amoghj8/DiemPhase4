configs = [
    {
        'nvalidators': 4,
        'all_leaders' : False,
        'nfaulty': 1,
        'limit_step_1' : 5,
        'limit_step_2' : 5,
        'limit_step_3' : 2,
        'partition_size' : 2,
        'nbr_of_rounds' : 10,
        'nclients': 5,
        'nclientops': 5,
        'sleeptime': 1,
        'clienttimeout': 10,
        'delta': 5,
        'window_size': 5,
        'exclude_size': 1,
        'exclusion_list': {
            "1": {
                "C" : {
                    "destination" : ["D"],
                    "messageType" : ""
                },
                "D" : {
                    "destination" : ["A"],
                    "messageType": "proposal_message"
                }
            },
            "2": {
                "A" : {
                    "destination" : ["C"],
                    "messageType" : ""
                },
                "B" : {
                    "destination" : ["D"],
                    "messageType": "vote_message"
                }
            }
        } 
    },
    {
        'nvalidators': 4,
        'all_leaders' : False,
        'nfaulty': 1,
        'limit_step_1' : 5,
        'limit_step_2' : 5,
        'limit_step_3' : 2,
        'partition_size' : 2,
        'nbr_of_rounds' : 10,
        'nclients': 5,
        'nclientops': 5,
        'sleeptime': 1,
        'clienttimeout': 10,
        'delta': 5,
        'window_size': 5,
        'exclude_size': 1,
        'exclusion_list': {
            "1": {
                "A" : {
                    "destination" : ["B", "C"],
                    "messageType" : ""
                },
                "B" : {
                    "destination" : ["D"],
                    "messageType": "vote_message"
                }
            },
            "2": {
                "C" : {
                    "destination" : ["A"],
                    "messageType" : ""
                },
                "B" : {
                    "destination" : ["D"],
                    "messageType": "proposal_message"
                }
            }
        }
    }
]