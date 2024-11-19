import csv

# Load rankings directly into a list of lists
with open('rankings.csv', 'r') as file:
    rankings_list = [line.strip().split(',') for line in file.readlines()]
    rankings_list = [[row[0], float(row[1])] for row in rankings_list]  # Convert scores to float

# Load bracket data directly into a list of lists
with open('bracket.txt', 'r') as file:
    bracket = {}
    index = 0
    for line in file:
        # Remove any surrounding whitespace or newlines
        line = line.strip()
        if line:  # Check if the line is not empty
            bracket[line] = index
            index += 1


prize_moneys = [3,
6.5,
10,
20,
30,
60,
120,
]

prize_quantities = [
    64,
    32,
    16,
    8,
    4,
    2,
    1
]

class GreedyTable:

    def __init__(self, prize_quantities):

        self.greedy_table = []
        self.total = prize_quantities[0]

        for num in prize_quantities:
            self.greedy_table.append([False for _ in range(num)])

        
    def mark_taken(self, player, round):

        placement = bracket[player]

        for i in range(round+1):

            section = int(placement // (self.total / len(self.greedy_table[i])))

            self.greedy_table[i][section] = True


    def is_taken_path(self, player, round):

        placement = bracket[player]

        for i in range(round+1):

            section = int(placement // (self.total / len(self.greedy_table[i])))

            if self.greedy_table[i][section]:
                return True

        return False
    
    def is_taken(self, player, round):

        placement = bracket[player]

        section = int(placement // (self.total / len(self.greedy_table[round])))

        return self.greedy_table[round][section]



## Iterate through players in descending order
## Force player to lose at the earliest point possible
def get_min(rankings_index, round):

    

    players_above = 0
    gt = GreedyTable(prize_quantities)

    target_prize_money = rankings_list[rankings_index][1]
    target_player = rankings_list[rankings_index][0]

    if target_player in bracket:
        target_prize_money += prize_moneys[round]
        ##gt.mark_taken(target_player, round)

    for i in range(len(rankings_list)):

        player, prize_money = rankings_list[i]

        if i == rankings_index:
            continue

        if prize_money > target_prize_money:
            players_above += 1
            continue

        if prize_money + prize_moneys[-1] < target_prize_money:
            break

        if take_max(player, prize_money, target_prize_money, gt):
            players_above += 1
        


    return players_above + 1



## Iterate through players in descending order
## Apply the least amount of prize money it would take to surpass player
## Mark that path taken in greedy table
def get_max(rankings_index, round):

    players_above = 0
    gt = GreedyTable(prize_quantities)

    target_prize_money = rankings_list[rankings_index][1]
    target_player = rankings_list[rankings_index][0]
    
    if target_player in bracket:
        target_prize_money += prize_moneys[round]
        gt.mark_taken(target_player, round)

    for i in range(len(rankings_list)):

        player, prize_money = rankings_list[i]

        if i == rankings_index:
            continue

        if prize_money > target_prize_money:
            players_above += 1
            continue

        if prize_money + prize_moneys[-1] < target_prize_money:
            break

        if take_min(player, prize_money, target_prize_money, gt):
            players_above += 1

    return players_above + 1


def take_min(player, prize_money, target, gt):

    if player not in bracket:
        return prize_money > target

    for i in range(len(prize_moneys)):

        tournament_prize = prize_moneys[i]

        if tournament_prize + prize_money < target:
            continue

        if not gt.is_taken_path(player, i):
            gt.mark_taken(player, i)
            return True
        
    return False
        

def take_max(player, prize_money, target, gt):

    ## goal is to get min possible prize money

    if player not in bracket:
        return prize_money > target
    
    if prize_money + prize_moneys[0] > target:
        return True
    
    for i in range(1, len(prize_moneys)):

        tournament_prize = prize_moneys[i-1]

        if not gt.is_taken(player, i):          
            if tournament_prize + prize_money < target:
                gt.mark_taken(player, i)
                return False
            else:
                gt.mark_taken(player, len(prize_moneys)-1)
                return True
    
    gt.mark_taken(player, len(prize_moneys)-1)
    return True
    
res = []

for i in range(len(rankings_list)):

    target_player = rankings_list[i][0]

    row = [target_player]

    for j in range(len(prize_moneys)):

        if target_player not in bracket and j > 0:
            break

        
        minv = get_min(i, j)
        maxv = get_max(i, j)

        if minv == maxv:
            string = f"{minv}"
        else:
            string = f"{minv}-{maxv}"

        if minv > maxv:
            print(target_player, j, minv, maxv)

        row.append(string)

    res.append(row)

# Writing to the CSV file
with open('outcomes.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write multiple rows
    writer.writerows(res)