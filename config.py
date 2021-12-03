configs = [
    {
        'nvalidators': 4,
        'all_leaders' : True,
        'nfaulty': 1,
        'limit_step_1' : 15,
        'limit_step_2' : 60,
        'limit_step_3' : 5,
        'partition_size' : 2,
        'nbr_of_rounds' : 10,
        'test_type' : 'DETERMINISTIC',
        'nclients': 5,
        'nclientops': 5,
        'sleeptime': 1,
        'clienttimeout': 10,
        'delta': 0.5,
        'window_size': 5,
        'exclude_size': 1,
        'quorum_size_bug': 0,
        'conflicting_votes_bug': 0,
        'exclusion_flag': 0,
        'exclusion_list': {
            "4": {
                "C" : {
                    "D" : {
                        "messageType" : "Proposal"
                    }
                },
                "B" : {
                    "E" : {
                        "messageType" : "*"
                    }
                }
            },
            "5" : {
                "B" : {
                    "A" : {
                        "messageType" : "Proposal"
                    }
                },
                "B" : {
                    "E" : {
                        "messageType" : "Vote"
                    }
                }
            }
        } 
    }
]