import os
import pygsheets
import pandas as pd

THIS_PATH  = os.path.dirname(__file__)
MTEAM_PATH = os.path.join(THIS_PATH, '../data/MTeams.csv')

# --------------------------------------------------------------------------------------------------------------------

def right_cell(cell):
    col, row = cell[:1], cell[1:]
    return f"{chr(ord(col)+1)}{row}"

def left_cell(cell):
    col, row = cell[:1], cell[1:]
    return f"{chr(ord(col)-1)}{row}"

# --------------------------------------------------------------------------------------------------------------------
def get_id_from_name(name):
    df = pd.read_csv(MTEAM_PATH)
    name = name.strip()
    return int(df.loc[df['TeamName']==name, 'TeamID'].values[0])
    
def get_name_from_id(id):
    df = pd.read_csv(MTEAM_PATH)
    id = int(id)
    return df.loc[df['TeamID']==id, 'TeamName'].values[0]

def get_predictions(submission):
    submission = os.path.join(THIS_PATH, '..', submission)
    df = pd.read_csv(submission)
    # key: "{team1_id}_{team2_id}", val: id of winning team
    predictions = {}
    for _, row in df.iterrows():
        id_  = row['ID']
        pred = row['Pred']
        year, t1, t2 = list(map(int, id_.split('_')))
        
        predictions[f"{t1}_{t2}"] = t1 if (float(pred) > 0.50) else t2
    return predictions
    
# --------------------------------------------------------------------------------------------------------------------

def bracket_from_submission(submission, gsheet_key, season):
    gc = pygsheets.authorize() # This may create a link to authorize

    N_ROUNDS    = 6
    _, FILENAME = submission.split('/')
    NAME, _     = FILENAME.split('.')
    
    template = gc.open_by_key(gsheet_key).worksheet_by_title('Template')
    sheet = gc.open_by_key(gsheet_key)
    # create new worksheet for bracket and unhide
    wk_sheet = sheet.add_worksheet(NAME, src_tuple=(sheet.id, template.id), src_worksheet=template)
    wk_sheet.hidden = False
    
    # map between tournament game number and cell of teams playing in it
    # key: "ROUND.GAME_NUM", val: (team_1 cell, team_2 cell)
    gsheet_cell_map = {
        "0.1": ('G69', 'G70'), "0.2": ('K69', 'K70'), "0.3": ('O69', 'O70'), "0.4": ('S69', 'S70'),
        "1.1": ('A5', 'A7'), "1.2": ('A9', 'A11'), "1.3": ('A13', 'A15'), "1.4": ('A17', 'A19'), "1.5": ('A21', 'A23'), "1.6": ('A25', 'A27'), "1.7": ('A29', 'A31'), "1.8": ('A33', 'A35'), "1.9": ('A37', 'A39'), "1.10": ('A41', 'A43'), "1.11": ('A45', 'A47'), "1.12": ('A49', 'A51'), "1.13": ('A53', 'A55'), "1.14": ('A57', 'A59'), "1.15": ('A61', 'A63'), "1.16": ('A65', 'A67'), "1.17": ('Y5', 'Y7'), "1.18": ('Y9', 'Y11'), "1.19": ('Y13', 'Y15'), "1.20": ('Y17', 'Y19'), "1.21": ('Y21', 'Y23'), "1.22": ('Y25', 'Y27'), "1.23": ('Y29', 'Y31'), "1.24": ('Y33', 'Y35'), "1.25": ('Y37', 'Y39'), "1.26": ('Y41', 'Y43'), "1.27": ('Y45', 'Y47'), "1.28": ('Y49', 'Y51'), "1.29": ('Y53', 'Y55'), "1.30": ('Y57', 'Y59'), "1.31": ('Y61', 'Y63'), "1.32": ('Y65', 'Y67'),
        "2.1": ('C6', 'C10'), "2.2": ('C14', 'C18'), "2.3": ('C22', 'C26'), "2.4": ('C30', 'C34'), "2.5": ('C38', 'C42'), "2.6": ('C46', 'C50'), "2.7": ('C54', 'C58'), "2.8": ('C62', 'C66'), "2.9": ('W6', 'W10'), "2.10": ('W14', 'W18'), "2.11": ('W22', 'W26'), "2.12": ('W30', 'W34'), "2.13": ('W38', 'W42'), "2.14": ('W46', 'W50'), "2.15": ('W54', 'W58'), "2.16": ('W62', 'W66'),
        "3.1": ('E8', 'E16'), "3.2": ('E24', 'E32'), "3.3": ('E40', 'E48'), "3.4": ('E56', 'E64'), "3.5": ('U8', 'U16'), "3.6": ('U24', 'U32'), "3.7": ('U40', 'U48'), "3.8": ('U56', 'U64'),
        "4.1": ('G12', 'G28'), "4.2": ('G44', 'G60'), "4.3": ('S12', 'S28'), "4.4": ('S44', 'S60'),
        "5.1": ('I20', 'I52'), "5.2": ('Q20', 'Q52'),
        "6.1": ('K35', 'O35')
    }
    
    predictions = get_predictions(submission)
    
    for ROUND in range(N_ROUNDS+1):
        N_GAMES = (2 ** (N_ROUNDS-ROUND)) if ROUND != 0 else 4 # first four

        for GAME in range(1, N_GAMES+1):
            # get teams
            (team_a_cell, team_b_cell) = gsheet_cell_map[f"{ROUND}.{GAME}"]
            team_a_info = wk_sheet.get_value(team_a_cell).strip()
            team_b_info = wk_sheet.get_value(team_b_cell).strip()
            
            team_a_seed, team_a = team_a_info.split('.')
            team_b_seed, team_b = team_b_info.split('.')
            
            team_a_id = get_id_from_name(team_a.strip())
            team_b_id = get_id_from_name(team_b.strip())

            matchup = f"{team_a_id}_{team_b_id}" if int(team_a_id) < int(team_b_id) else f"{team_b_id}_{team_a_id}"
            winner  = predictions[matchup]
            
            # write '.' to cell next to winner
            winner_cell, loser_cell = (team_a_cell, team_b_cell) if (winner == team_a_id) else (team_b_cell, team_a_cell)
            cell_to_mark = right_cell(winner_cell) if (GAME <= (N_GAMES/2)) else left_cell(winner_cell)
            wk_sheet.update_value(cell_to_mark, '.')
    
    wk_sheet.create_protected_range('A5', 'Y70')
    return wk_sheet.url
