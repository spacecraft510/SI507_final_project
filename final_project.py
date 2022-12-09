import requests
import os
import json
import time
import ast
import tkinter 
from tkinter import ttk
#################################################################
class WLStats:
    def __init__(self,win=0, lose=0):
        self.win=win
        self.lose=lose
        self.total = win+lose
        self.winrate = round(win/(win+lose),5) if ((win+lose)!=0) else 0.0

    def incr_win(self, amount=1):
        self.win+=amount
        self.total+=amount
        self.winrate = round(self.win / self.total,5) if ((self.total)!=0) else 0.0

    def incr_lose(self, amount=1):
        self.lose+=amount
        self.total+=amount
        self.winrate = round(self.win / self.total,5) if ((self.total)!=0) else 0.0
        
    def getWinRate(self):
        return self.winrate

class Hero:
    def __init__(self,name="", id=0):
        self.name = name
        self.id = id
        self.wl_list = {}
        read_file = open("hero_name.json", "r")
        Lines = read_file.readlines()
        for line in Lines:
            res = line.strip().replace('"', '').replace(',','').split(": ")
            if self.id != int(res[0]):
                self.wl_list[int(res[0])]=WLStats()
        read_file.close()
        self.edge_list = []
        self.edge_rate = []

    def findLowestWinRate(self):
        filter_wllist = {k:self.wl_list[k] for k in self.wl_list if self.wl_list[k].total >= 10}
        list = {k: v.getWinRate() for k, v in sorted(filter_wllist.items(), key=lambda item: item[1].getWinRate())}
        # print(str(list.items()))
        return [(k, v) for k, v in list.items()][:5]

    def incr_win(self, id=0, amount=1):
        self.wl_list[id].incr_win(amount)

    def incr_lose(self, id=0, amount=1):
        self.wl_list[id].incr_lose(amount)
    
    def edgeUpdate(self):
        newEdges = self.findLowestWinRate()
        self.edge_list = list(x[0] for x in newEdges)
        self.edge_rate = list(x[1] for x in newEdges)


    def getEdge(self):
        return self.edge_list,self.edge_rate

    def print(self):
        print("id: "+str(self.id))
        print("name: "+self.name)
        for x in self.wl_list:
            print("hero_id: "+str(x)+" games_played: "+str(self.wl_list[x].total) +" wins: "+str(self.wl_list[x].win))
        print(self.edge_list)
        print(self.edge_rate)
#################################################################
gui = tkinter.Tk()
gui.title('Dota2 BanPick Helper')
gui.geometry("760x540")
text = tkinter.Text(gui, width=60, height=30)
text.grid(row = 0, column = 0, columnspan  = 60, rowspan =30)

def main():

    Hero_list = {}
    name_list = {}
    read_file = open("hero_name.json", "r")
    Lines = read_file.readlines()
    for line in Lines:
        res = line.strip().replace('"', '').replace(',','').split(": ")
        name = res[1]
        id = int(res[0])
        Hero_list[id]=Hero(name,id)
        name_list[name]=id
        print(str(id)+"  "+name)
    read_file.close()
    id_list = {y: x for x, y in name_list.items()}

    def insert_hello():
        text.insert("end", "Hello!")
    
####################################################################################

    n = tkinter.StringVar()
    edgelist = [tkinter.StringVar() for x in range(5)]
    ratelist = [tkinter.StringVar() for x in range(5)]
    option = ttk.Combobox(gui, width = 27, textvariable = n)
    option['values'] = list(name_list.keys())
    option.grid(row=0,column=60,sticky="w")
    def callback(event):
        if not option.get() == "":
            res_name = option.get()
            hero = Hero_list[name_list[res_name]]
            edge ,rate = hero.getEdge()
            for idx,x in enumerate(edge):
                edgelist[idx].set(id_list[edge[idx]])
                ratelist[idx].set(rate[idx])
            # print(edge)
            # for x in edgelist:
            #     print(x.get())
    
    def setVar(toHero):
        n.set(toHero)
        hero = Hero_list[name_list[toHero]]
        edge ,rate = hero.getEdge()
        for idx,x in enumerate(edge):
            edgelist[idx].set(id_list[edge[idx]])
            ratelist[idx].set(rate[idx])
        print(edge)
        for x in edgelist:
            print(x.get())
####################################################################################
            
    option.bind("<<ComboboxSelected>>", callback)
    option.current()
    # button1 = tkinter.Button(gui, text='load from OpenDotaAPI', width=20, command=insert_hello)
    scrollbar = tkinter.Scrollbar(gui)
    scrollbar.grid(row = 0, column = 30, rowspan =60,sticky = "nsw")
    scrollbar.config( command = text.yview )
    text.config(yscrollcommand=scrollbar.set)
    button1 = tkinter.Button(gui, text='update OpenDotaAPI', width=20, command=lambda: updateMatchups(Hero_list))
    button1.grid(row = 60, column = 0, sticky = "W", pady = 2)
    button2 = tkinter.Button(gui, text='load from OpenDotaAPI', width=20, command=lambda: loadMatchups(Hero_list,"get_matchups.json"))
    button2.grid(row = 60, column = 1, sticky = "W", pady = 2)
    button3 = tkinter.Button(gui, text='load from file ', width=20, command=lambda: loadMatchups(Hero_list))
    button3.grid(row = 60, column = 2, sticky = "W", pady = 2)
    button4 = tkinter.Button(gui, text='getMatchesOpenDota', width=20, command=lambda: getMatchesOpenDota(Hero_list))
    button4.grid(row = 70, column = 0, sticky = "W", pady = 2)
    button5 = tkinter.Button(gui, text='getMatchesSteam', width=20, command=lambda: getRecentMatchesSteam(Hero_list))
    button5.grid(row = 70, column = 1, sticky = "W", pady = 2)
    button6 = tkinter.Button(gui, text='getLargeMatchesSteam', width=20, command=lambda: getLargeMatchesSteam(Hero_list, int(round(scale.get()))))
    button6.grid(row = 70, column = 2, sticky = "W", pady = 2)

    button7 = tkinter.Button(gui, text='save to file', width=20, command=lambda: saveMatchups(Hero_list))
    button7.grid(row = 80, column = 0, sticky = "W", pady = 2)
    buttonend = tkinter.Button(gui, text='STOP', width=20, command=gui.destroy)
    buttonend.grid(row = 80, column = 1, sticky = "W", pady = 2)
    scale = tkinter.Scale(gui, from_=100, to=10000, orient="horizontal")
    scale.grid(row = 80, column = 2, sticky = "nW", padx=25)


    buttonedge1 = tkinter.Button(gui, textvariable=edgelist[0], width=15, command=lambda:setVar(edgelist[0].get()))
    buttonedge1.grid(row = 10, column = 60, sticky = "nW", pady = 2)
    buttonedge2 = tkinter.Button(gui, textvariable=edgelist[1], width=15, command=lambda:setVar(edgelist[1].get()))
    buttonedge2.grid(row = 11, column = 60, sticky = "nW", pady = 2)
    buttonedge3 = tkinter.Button(gui, textvariable=edgelist[2], width=15, command=lambda:setVar(edgelist[2].get()))
    buttonedge3.grid(row = 13, column = 60, sticky = "nW", pady = 2)
    buttonedge4 = tkinter.Button(gui, textvariable=edgelist[3], width=15, command=lambda:setVar(edgelist[3].get()))
    buttonedge4.grid(row = 14, column = 60, sticky = "nW", pady = 2)
    buttonedge5 = tkinter.Button(gui, textvariable=edgelist[4], width=15, command=lambda:setVar(edgelist[4].get()))
    buttonedge5.grid(row = 15, column = 60, sticky = "nW", pady = 2)

    buttonrate1 = tkinter.Button(gui, textvariable=ratelist[0], width=10)
    buttonrate1.grid(row = 10, column = 60, sticky = "n",padx = 120, pady = 2)
    buttonrate2 = tkinter.Button(gui, textvariable=ratelist[1], width=10)
    buttonrate2.grid(row = 11, column = 60, sticky = "n",padx = 120, pady = 2)
    buttonrate3 = tkinter.Button(gui, textvariable=ratelist[2], width=10)
    buttonrate3.grid(row = 13, column = 60, sticky = "n",padx = 120, pady = 2)
    buttonrate4 = tkinter.Button(gui, textvariable=ratelist[3], width=10)
    buttonrate4.grid(row = 14, column = 60, sticky = "n",padx = 120, pady = 2)
    buttonrate5 = tkinter.Button(gui, textvariable=ratelist[4], width=10)
    buttonrate5.grid(row = 15, column = 60, sticky = "n",padx = 120, pady = 2)
    gui.mainloop()


#################################################################################
def getLargeMatchesSteam(Hero_list, limit=100):

    response = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?key=CFCC44456136B4AE0AAF4E97E89CB551&skill=3&min_players=10") #&matches_requested=500
    response_status_code = response.status_code
    base = response.json()["result"]["matches"][0]["match_seq_num"]
    # get 1000 matches
    success = 0
    match_seq_num = base
    # print(limit)
    text.insert("end",  "fetching "+str(limit)+" matches data...(This will take a while)\n")
    gui.update()
    test = []
    while True:
        gui.update()
        if(success>limit):
            break
        text.insert("end",  "progress: "+str(round((success/limit)*100))+"%...\n")
        gui.update()
        response = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v1/?key=CFCC44456136B4AE0AAF4E97E89CB551&start_at_match_seq_num="+str(match_seq_num)) 
        response_status_code = response.status_code
        print(response_status_code)
        for i in range(20):
            gui.update()
            time.sleep(0.5)
        matches = response.json()["result"]["matches"]
        # print("new Cycle----@"+str(match_seq_num))
        for match in matches:
            sub_match_id = match["match_id"]
            lobby_type = match["lobby_type"]
            radiant_win = match["radiant_win"]
            game_mode =match["game_mode"]
            # text.insert("end",  "processing match: "+str(sub_match_id)+"\n")
            if match["match_seq_num"] in test:
                raise ValueError('A very specific bad thing happened.')
            test.append(match["match_seq_num"])
            gui.update()
            if (lobby_type==7) and (game_mode==3 or game_mode==22):
                radiant_team, dire_team = [], []
                for player in match["players"]:
                    if player["team_number"] == 0:
                        radiant_team.append(player["hero_id"])
                    else:
                        dire_team.append(player["hero_id"])
                for r in radiant_team:
                    for d in dire_team:
                        if radiant_win:
                            Hero_list[r].incr_win(d)
                            Hero_list[d].incr_lose(r)
                        else:
                            Hero_list[r].incr_lose(d)
                            Hero_list[d].incr_win(r)   
                success+=1

        match_seq_num -= 200 

    for id in Hero_list:
        Hero_list[id].edgeUpdate()
    text.insert("end",  "Steam large matches data loaded\n")


def getRecentMatchesSteam(Hero_list):
    response = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?key=CFCC44456136B4AE0AAF4E97E89CB551&game_mode=1&skill=3&min_players=10") #&matches_requested=500
    response_status_code = response.status_code
    response_data = response.json()["result"]["matches"]
    for match in response_data:
        match_id = match["match_id"]
        # print("processing match: "+str(match_id))
        text.insert("end",  "processing match: "+str(match_id)+"\n")
        gui.update()
        match_response = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?key=CFCC44456136B4AE0AAF4E97E89CB551&match_id="+str(match_id))
        if match_response.status_code ==200:
            radiant_win = match_response.json()["result"]["radiant_win"]
            radiant_team, dire_team = [], []
            for player in match["players"]:
                if player["team_number"] == 0:
                    radiant_team.append(player["hero_id"])
                else:
                    dire_team.append(player["hero_id"])
            for r in radiant_team:
                for d in dire_team:
                    if radiant_win:
                        Hero_list[r].incr_win(d)
                        Hero_list[d].incr_lose(r)
                    else:
                        Hero_list[r].incr_lose(d)
                        Hero_list[d].incr_win(r)
    for id in Hero_list:
        Hero_list[id].edgeUpdate()
    text.insert("end",  "Steam matches data loaded\n")

def updateMatchups(Hero_list):
    if os.path.exists("get_matchups.json"):
        os.remove("get_matchups.json")
    read_file = open("get_matchups.json", "w")
    for num in Hero_list:
        text.insert("end", str("updating hero_id: "+str(num))+"\n")
        response = requests.get("https://api.opendota.com/api/heroes/"+str(num)+"/matchups")
        response_status_code = response.status_code
        # print(str(response.json()))
        text.insert("end",  "getting "+str(num)+" matchups from OpenDota\n")
        gui.update()
        read_file.write(str(num)+"%"+str(response.json())+"\n")
        time.sleep(2.4)

def saveMatchups(Hero_list):
    if os.path.exists("hero_matchups.json"):
        os.remove("hero_matchups.json")
    read_file = open("hero_matchups.json", "w")
    for num in Hero_list:
        string=str(num)+"%"
        list=[]
        for x in Hero_list[num].wl_list:
            list.append({'hero_id': x, 'games_played': Hero_list[num].wl_list[x].total, 'wins': Hero_list[num].wl_list[x].win})
        read_file.write(string+str(list)+"\n")
    read_file.close()
    text.insert("end",  "Match Data saved\n")

def loadMatchups(Hero_list, file="hero_matchups.json"):
    read_file = open(file, "r")
    Lines = read_file.readlines()
    for line in Lines:
        # print(line)
        [id,res] = line.strip().split("%")
        # res = json.loads(line.strip())
        res = ast.literal_eval(res)
        
        for dict in res:
            Hero_list[int(id)].incr_win(dict['hero_id'], dict['wins'])
            Hero_list[int(id)].incr_lose(dict['hero_id'], dict['games_played']-dict["wins"])
        # Hero_list[id].print()
    for id in Hero_list:
        Hero_list[id].edgeUpdate()
    text.insert("end", str(file)+" loaded\n")

    
def getMatchesOpenDota(Hero_list):
    response = requests.get("https://api.opendota.com/api/publicMatches/?mmr_descending=10000")
    response_status_code = response.status_code
    response_data = response.json()
    for match in response_data:
        radiant_win = match['radiant_win']
        # print(radiant_win)
        radiant_team = [int(x) for x in match['radiant_team'].split(",")]
        dire_team = [int(x) for x in match['dire_team'].split(",")] 
        for r in radiant_team:
            for d in dire_team:
                if radiant_win:
                    Hero_list[r].incr_win(d)
                    Hero_list[d].incr_lose(r)
                else:
                    Hero_list[r].incr_lose(d)
                    Hero_list[d].incr_win(r)
    for id in Hero_list:
        Hero_list[id].edgeUpdate()
    text.insert("end",  "OpenDota matches loaded\n")

if __name__ == '__main__':
    main()
