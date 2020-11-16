import discord
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import requests
import numpy as np
from io import BytesIO
from PIL import Image
from tqdm import tqdm
import random

GUILD = '723985175481942137'
TOKEN = 'Nzc3NDM1MDQ3MDAyNzY3Mzcy.X7DYzw.fXAIxA86JGf7SzT2tIFtd_NW6VU'

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        for guild in client.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        global channel_id
        channel_id = client.get_channel(777785991519535114)
        await channel_id.send("```Welcome to Oliver's Network Generator Discord Bot 3000!\n \nFor more information type: \n\t$commands for a list of commands \n\t$guide for a step by step how to guide```")


    async def on_message(self, message):
        if message.author == self.user:
            return

        if (message.channel.id == channel_id.id):
            if message.content.startswith('$commands'):
                await message.channel.send(
'''```
Commands:

$startnetwork
    Starts/restarts the network generator, make sure
    to wait until it says its ready before trying
    any new commands. The main thing that it's doing
    is downloading profile pics, which takes a few seconds.

$addconnection
    Add a singular connection in the format:
        name,name,relationship
    name = discord username
    relationship = Friend, Family or SO

$addconnections
    Add multiple connections at once in the format:
        name,name,relationship;name,name,relationship

    Same as before but put a semicolon between
    connections

$generaterandom type #
    Generates # random connections for testing
    purposes

    Type is either edges or connections. edges will
    plug the connections straight into the network,
    while connections will give you the text that you
    can enter yourself.

$print
    Generates the network visualization and sends it
    in the chat
$commands
    Sends you a list of commands

$guide
    Sends you a step by step how to guide

$goodbye
    The bot will shutdown```''')

            if message.content.startswith('$guide'):
                await message.channel.send(
'''```
User Guide:

1. Start by entering $startnetwork and wait until you
    get the OK to continue.

2. Start adding connections, either one at a time
    using $addconnection or all at once using
    $addconnections

    Side Note: I reccommend keeping a relationship
    record in the form of a .txt file or just a note
    in your phone for easy copying and pasteing.

3. Generate the network graph using $print

4. Say $goodbye```''')

            if message.content.startswith('$hello'):
                await message.channel.send('Hello World!')

            if message.content.startswith('$testimage'):
                await message.channel.send(file=discord.File('default_avatar.jpg'))

            if message.content.startswith('$goodbye'):
                gb_user = message.author

                if gb_user.nick != None:
                    gb_name = message.author.nick
                else:
                    gb_name = message.author.name

                await message.channel.send(f'Goodbye {gb_name}!')
                await client.close()

            if message.content.startswith('$startnetwork'):

                await message.channel.send('Starting Network Generator')

                for guild in client.guilds:
                    if guild.name == GUILD:
                        break

                global name_ind
                name_ind = {}
                global member_count
                member_count = 0
                global bots
                bots = []
                global relationshipColorDict
                relationshipColorDict = {'Family':'blue', 'SO':'pink', 'Friend':'green'}
                global G
                G = nx.Graph()

                #generate nodes and get profile pictures
                imageBaseURL = 'https://cdn.discordapp.com/'
                for ind, member in tqdm(enumerate(guild.members)):
                    if member.avatar != None:
                        url = f'{imageBaseURL}avatars/{member.id}/{member.avatar}.png?size=1024'
                        r = requests.get(url, stream=True)
                        PFPimg = mpimg.imread(BytesIO(r.content))

                    else:
                        PFPimg = mpimg.imread('default_avatar.jpg')

                    G.add_node(ind, image=PFPimg, name=member.name, disc=member.discriminator)
                    name_ind[member.name] = ind
                    name_ind[ind] = member.name
                    member_count += 1

                    if member.bot:
                        bots.append(ind)

                await message.channel.send('Network Generator Ready')


            if message.content.startswith('$addconnection'):
                command = message.content.lstrip('$addconnection')

                #name,name,relationship;name,name,relationship
                if command.startswith('s'):
                    edge_input = command.lstrip('s').strip().split(';')
                    edge_input = [x.split(',') for x in edge_input]

                    for x in edge_input:
                        G.add_edge(name_ind[x[0]], name_ind[x[1]], relationship=relationshipColorDict[x[2]])

                    await message.channel.send(f'Connections made: {G.edges()}')

                else:
                    #name,name,relationship
                    edge_input = command.strip().split(',')
                    G.add_edge(name_ind[edge_input[0]], name_ind[edge_input[1]], relationship=relationshipColorDict[edge_input[2]])
                    await message.channel.send(f'Connection made: {name_ind[edge_input[0]]}, {name_ind[edge_input[1]]}, {relationshipColorDict[edge_input[2]]}')

            if message.content.startswith('$generaterandom'):
                randCommand = message.content.lstrip('$generaterandom').strip().split()
                randNum = int(randCommand[1])
                await message.channel.send(f'Generating {randNum} random {randCommand[0]}')

                if randCommand[0] == 'edges':
                    for i in range(randNum):
                        name1 = random.randint(0,member_count-1)
                        name2 = random.randint(0,member_count-1)
                        relationship = random.choice(list(relationshipColorDict.keys()))

                        if name1 not in bots and name2 not in bots:
                            G.add_edge(name1,name2, relationship=relationshipColorDict[relationship])

                if randCommand[0] == 'connections':
                    randConnectionsList = []
                    for i in range(randNum):
                        name1 = name_ind[random.randint(0,member_count)]
                        name2 = name_ind[random.randint(0,member_count)]
                        relationship = random.choice(list(relationshipColorDict.keys()))

                        if i == 0:
                            randConnectionsList.append(f'{name1},{name2},{relationship}')
                        else:
                            randConnectionsList.append(f';{name1},{name2},{relationship}')

                    randConnectionsString = ''.join(randConnectionsList)
                    await message.channel.send(randConnectionsString)

            if message.content.startswith('$print'):
                await message.channel.send('Printing Network')
                # generate graph
                pos=nx.kamada_kawai_layout(G)

                #matplotlib figure
                fig=plt.figure(figsize=(5,5), frameon=False)
                ax=plt.subplot(111)
                ax.set_aspect('equal')


                #Bot Corner
                H = G.subgraph(bots)

                center = (-0.75,0.75)
                side_length = 0.3

                bots_pos = nx.circular_layout(H, center = np.array(center), scale=0.1)

                for n in G.nodes():
                    if n in bots:
                        pos[n] = bots_pos[n]

                ax.add_patch(matplotlib.patches.Rectangle((center[0]-(side_length/2),center[1]-(side_length/2)),
                                                            side_length, side_length, color='grey', alpha=0.5))

                ax.text(center[0],center[1]+(side_length/2),
                        'Bot Corner!', horizontalalignment='center',
                        verticalalignment='bottom',
                        fontfamily='Lucida Console')

                #no go zones
                for n in G.nodes():
                    if n not in bots:
                        bot_zone = (-0.55,0.55)
                        legend_zone = (0.41,0.58)
                        border_buffer = 0.95
                        x,y = pos[n]

                        #border patrol
                        if x > border_buffer:
                            x_dist = abs(x-border_buffer)
                            x = x - x_dist

                        if x < -border_buffer:
                            x_dist = abs(x-border_buffer)
                            x = x + x_dist

                        if y > border_buffer:
                            y_dist = abs(y-border_buffer)
                            y = y - y_dist

                        if y < -border_buffer:
                            y_dist = abs(y-border_buffer)
                            y = y + y_dist

                        #bot zone
                        if x < bot_zone[0] and y > bot_zone[1]:
                            print('Bot Zone: ',n, name_ind[n], pos[n])
                            x_dist = abs(x-bot_zone[0])
                            y_dist = abs(y-bot_zone[1])

                            if x_dist < y_dist:
                                x = x + x_dist
                            else:
                                y = y - y_dist

                        #legend zone
                        if x > legend_zone[0] and y > legend_zone[1]:
                            print('Legend Zone: ',n, name_ind[n], pos[n])
                            x_dist = abs(x-legend_zone[0])
                            y_dist = abs(y-legend_zone[1])

                            if x_dist < y_dist:
                                x = x - x_dist
                            else:
                                y = y - y_dist

                        pos[n] = np.array((x,y))

                #plot netowrk edges
                edges = G.edges()
                colors = [G[u][v]['relationship'] for u,v in edges]
                nx.draw_networkx_edges(G,pos,ax=ax, edge_color=colors)

                #Legend
                markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in relationshipColorDict.values()]
                plt.legend(markers, relationshipColorDict.keys(), numpoints=1)

                #fuckery to put images on nodes
                figlim = 1
                plt.xlim(-figlim,figlim)
                plt.ylim(-figlim,figlim)

                trans = ax.transData.transform
                trans2 = fig.transFigure.inverted().transform
                imsize = 0.03 # this is the image size

                for n in tqdm(G.nodes()):
                    (x,y) = pos[n]
                    xx,yy = trans((x,y)) # figure coordinates
                    xa,ya = trans2((xx,yy)) # axes coordinates
                    a = plt.axes([xa-imsize/2.0,ya-imsize/2.0, imsize, imsize])
                    a.imshow(G.nodes()[n]['image'])
                    a.set_aspect('equal')
                    a.axis('off')

                ax.axes.xaxis.set_visible(False)
                ax.axes.yaxis.set_visible(False)

                plt.savefig("network.png", dpi=400)

                await message.channel.send(file=discord.File('network.png'))



intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = MyClient(intents = intents)
client.run(TOKEN)
