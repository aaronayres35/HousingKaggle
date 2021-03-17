# --------------------------------------------------------------------------------------------------------------------

# get seed info (i.e seed.subseed, where seed is seed in quadrant and sub-seed is rank among teams w/ same seed)
def get_seed_info(i):
    mapping = {
        1: '1.1', 2: '1.2', 3: '1.3', 4: '1.4', 5: '2.1', 6: '2.2', 7: '2.3', 8: '2.4',
        9: '3.1', 10: '3.2', 11: '3.3', 12: '3.4', 13: '4.1', 14: '4.2', 15: '4.3', 16: '4.4',
        17: '5.1', 18: '5.2', 19: '5.3', 20: '5.4', 21: '6.1', 22: '6.2', 23: '6.3', 24: '6.4',
        25: '7.1', 26: '7.2', 27: '7.3', 28: '7.4', 29: '8.1', 30: '8.2', 31: '8.3', 32: '8.4',
        33: '9.1', 34: '9.2', 35: '9.3', 36: '9.4', 37: '10.1', 38: '10.2', 39: '10.3', 40: '10.4',
        41: '11.1', 42: '11.2', 43: '11.3', 44: '11.4', 45: '11.5', 46: '11.6', 47: '12.1', 48: '12.2', 49: '12.3', 50: '12.4',
        51: '13.1', 52: '13.2', 53: '13.3', 54: '13.4', 55: '14.1', 56: '14.2', 57: '14.3', 58: '14.4',
        59: '15.1', 60: '15.2', 61: '15.3', 62: '15.4', 63: '16.1', 64: '16.2', 65: '16.3', 66: '16.4', 67: '16.5', 68: '16.6'
    }
    return mapping[i]

# --------------------------------------------------------------------------------------------------------------------

# chalk "model" (winning team is highest seed)
def chalk_submission():
    FILE    = "submissions/chalk.txt"
    N_TEAMS = 68

    # clear
    open(FILE,"w").close()
    # open
    f = open(FILE,"w")

    for i in range(1, N_TEAMS+1):
        t1 = get_seed_info(i)
        for j in range(i+1, N_TEAMS+1):
            if i != j:
                t2 = get_seed_info(j)
                f.write(f"2021_{t1}_{t2}, 10\n")
    f.close()
    return FILE

# chalk "model" (winning team is highest seed)
def upset_submission():
    FILE    = "submissions/upset.txt"
    N_TEAMS = 68

    # clear
    open(FILE,"w").close()
    # open
    f = open(FILE,"w")

    for i in range(1, N_TEAMS+1):
        t1 = get_seed_info(i)
        for j in range(i+1, N_TEAMS+1):
            if i != j:
                t2 = get_seed_info(j)
                f.write(f"2021_{t1}_{t2}, -10\n")
    f.close()
    return FILE
    
# --------------------------------------------------------------------------------------------------------------------
