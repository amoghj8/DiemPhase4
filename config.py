configs = [
    {
        'nvalidators': 4,
        'all_leaders' : False,
        'nfaulty': 1,
        'limit_step_1' : 15,
        'limit_step_2' : 60,
        'limit_step_3' : 5,
        'partition_size' : 2,
        'nbr_of_rounds' : 10,
        'test_type' : 'RANDOM',
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
                    "B" : {
                        "messageType" : "proposal_message"
                    }
                },
                "B" : {
                    "C" : {
                        "messageType" : "*"
                    }
                }
            },
            "2": {
                "C" : {
                    "D" : {
                        "messageType" : "proposal_message"
                    }
                },
                "B" : {
                    "E" : {
                        "messageType" : "*"
                    }
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
        'limit_step_3' : 5,
        'partition_size' : 2,
        'nbr_of_rounds' : 10,
        'test_type' : 'RANDOM',
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
                    "B" : {
                        "messageType" : "proposal_message"
                    }
                },
                "B" : {
                    "C" : {
                        "messageType" : "*"
                    }
                }
            },
            "2": {
                "C" : {
                    "D" : {
                        "messageType" : "proposal_message"
                    }
                },
                "B" : {
                    "E" : {
                        "messageType" : "*"
                    }
                }
            }
        }
    }
]