import discord
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import requests
import numpy as np
from io import BytesIO
from PIL import Image
from tqdm import tqdm
import random

GUILD = 'nope'
TOKEN = 'not making that mistake again'

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

        await channel_id.send('Starting Network Generator')

        for guild in client.guilds:
            if guild.name == GUILD:
                break

        global name_ind
        name_ind = {}
        global name_disc
        name_disc = {}
        global disc_image
        disc_image = {}
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

            G.add_node(int(member.discriminator), image=PFPimg, name=member.name)

            name_disc[int(member.discriminator)] = member.name
            name_disc[member.name] = int(member.discriminator)

            disc_image[int(member.discriminator)] = PFPimg

            name_ind[member.name] = ind
            name_ind[ind] = member.name
            member_count += 1

            if member.bot:
                bots.append(int(member.discriminator))

        await channel_id.send('Network Generator Ready')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if (message.channel.id == channel_id.id):
            if message.content.startswith('$commands'):
                await message.channel.send(
'''```
Commands:

$restart
    Restarts the network generator, make sure
    to wait until it says its ready before trying
    any new commands. The main thing that it's doing
    is downloading profile pics, which takes a
    few seconds.

#connection DO INPUT
    Replace DO with either:
        add
        break
    pretty self explanetory what those do

    Replace INPUT with
        name,name,relationship

        name = discord username
        relationship = Friend, Family or SO

    message plural:
        Same as before but put a semicolon between
        connections. Also don't put in any spaces
        or returns, just the text.

        name,name,relationship;name,name,relationship

$load csv
    This is the way to load the network after its
    been saved. Just make sure to attatch the .csv
    file to the command message.

$generaterandom type #
    # is the number of random connections you want to
    generate.

    Type is either:
        edges
        connections

    edges:
        will plug the connections straight into
        the network

    connections:
        will give you the text that you
        can enter yourself using:
            $load message plural

$print
    Generates the network visualization and sends it
    in the chat

$save
    Saves current connections into a .csv file. You
    can download this and then load it back into the
    bot using:
        $add connection csv

    Side Note: a .csv file isn't something I made up,
                its a very common file format and you
                can open and edit it yourself in other
                programs like excel or just by editing
                the text itself as its pretty
                straightforward if you just look
                at it.

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
1. Start adding connections, either one at a time
    using:
        $load message singular

    or multiple at once using:
        $load message multiple

3. Generate the network graph using $print

4. Save connections you've created using:
    $save

5. Restart the bot using:
    $restart

6. Try loading in your saved connections using:
    $load csv

    Make sure to attatch the .csv file in the
    message.

7. Print the graph again using $print to see
    if you did everything right```''')

            if message.content.startswith('$hello'):
                hi_user = message.author

                if hi_user.nick != None:
                    hi_name = message.author.nick
                else:
                    hi_name = message.author.name

                await message.channel.send(f'Hello {hi_name}!')

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

            if message.content.startswith('$restart'):

                await message.channel.send('Starting Network Generator')

                for guild in client.guilds:
                    if guild.name == GUILD:
                        break

                global name_ind
                name_ind = {}
                global name_disc
                name_disc = {}
                global disc_image
                disc_image = {}
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

                    G.add_node(int(member.discriminator), image=PFPimg, name=member.name)

                    name_disc[int(member.discriminator)] = member.name
                    name_disc[member.name] = int(member.discriminator)

                    disc_image[int(member.discriminator)] = PFPimg

                    name_ind[member.name] = ind
                    name_ind[ind] = member.name
                    member_count += 1

                    if member.bot:
                        bots.append(int(member.discriminator))

                await message.channel.send('Network Generator Ready')


            if message.content.startswith('$load csv'):

                await message.channel.send('Importing Edge List and Reconstructing Graph')
                await message.attachments[0].save('import.csv')

                df = pd.read_csv('import.csv')
                print(df)
                G = nx.from_pandas_edgelist(df, source='source', target='target', edge_attr='relationship')


                for guild in client.guilds:
                    if guild.name == GUILD:
                        break

                #generate nodes and get profile pictures
                imageBaseURL = 'https://cdn.discordapp.com/'
                for ind, member in tqdm(enumerate(guild.members)):
                    if int(member.discriminator) not in G.nodes():
                        G.add_node(int(member.discriminator), name=member.name)

                        if member.bot:
                            bots.append(int(member.discriminator))

                nx.set_node_attributes(G, disc_image, 'image')

                await message.channel.send('Finished!')

            if message.content.startswith('$connection'):
                command = message.content.lstrip('$connection').split()
                add_break = command[0]
                mult_sing = command[1]
                edge_input = command[2]

                if add_break == 'add':
                    if mult_sing == 'multiple':
                        #name,name,relationship;name,name,relationship
                        edge_input = edge_input.lstrip('message multiple').strip().split(';')
                        edge_input = [x.split(',') for x in edge_input]

                        add_out = []
                        for x in edge_input:
                            add_out.append((name_disc[x[0]], name_disc[x[1]]))
                            G.add_edge(name_disc[x[0]], name_disc[x[1]], relationship=x[2])

                        await message.channel.send(f'Connections made: {add_out}')

                    elif mult_sing == 'singular':
                        #name,name,relationship
                        edge_input = edge_input.lstrip('message singular').strip().split(',')
                        G.add_edge(name_disc[edge_input[0]], name_disc[edge_input[1]], relationship=edge_input[2])
                        await message.channel.send(f'Connection made: {name_disc[edge_input[0]]}, {name_disc[edge_input[1]]}, {relationshipColorDict[edge_input[2]]}')

                if add_break == 'break':
                    if mult_sing == 'multiple':
                        #name,name,relationship;name,name,relationship
                        edge_input = edge_input.lstrip('message multiple').strip().split(';')
                        edge_input = [x.split(',') for x in edge_input]

                        break_out = []
                        for x in edge_input:
                            break_out.append((name_disc[x[0]], name_disc[x[1]]))
                            G.remove_edge(name_disc[x[0]], name_disc[x[1]])

                        await message.channel.send(f'Connections broken: {break_out}')

                    elif mult_sing == 'singular':
                        #name,name,relationship
                        edge_input = edge_input.lstrip('message singular').strip().split(',')
                        G.remove_edge(name_disc[edge_input[0]], name_disc[edge_input[1]])
                        await message.channel.send(f'Connection broken: {name_disc[edge_input[0]]}, {name_disc[edge_input[1]]}, {relationshipColorDict[edge_input[2]]}')

            if message.content.startswith('$generaterandom'):
                randCommand = message.content.lstrip('$generaterandom').strip().split()
                randNum = int(randCommand[1])
                await message.channel.send(f'Generating {randNum} random {randCommand[0]}')

                if randCommand[0] == 'edges':
                    for i in range(randNum):
                        name1 = random.choice(list(G.nodes()))
                        name2 = random.choice(list(G.nodes()))
                        relationship = random.choice(list(relationshipColorDict.keys()))

                        if name1 not in bots and name2 not in bots:
                            G.add_edge(name1,name2, relationship=relationship)

                if randCommand[0] == 'connections':
                    randConnectionsList = []
                    for i in range(randNum):
                        name1 = random.choice(list(G.nodes()))
                        name2 = random.choice(list(G.nodes()))
                        relationship = random.choice(list(relationshipColorDict.keys()))

                        if i == 0:
                            randConnectionsList.append(f'{name1},{name2},{relationship}')
                        else:
                            randConnectionsList.append(f';{name1},{name2},{relationship}')

                    randConnectionsString = ''.join(randConnectionsList)
                    await message.channel.send(randConnectionsString)

            if message.content.startswith('$save'):
                #DATAFRAME
                df = nx.to_pandas_edgelist(G)
                print(df)
                df.to_csv('network.csv', index = False)
                await message.channel.send('Here is a record of all current connections:', file = discord.File('network.csv'))

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
                            x_dist = abs(x-bot_zone[0])
                            y_dist = abs(y-bot_zone[1])

                            if x_dist < y_dist:
                                x = x + x_dist
                            else:
                                y = y - y_dist

                        #legend zone
                        if x > legend_zone[0] and y > legend_zone[1]:
                            x_dist = abs(x-legend_zone[0])
                            y_dist = abs(y-legend_zone[1])

                            if x_dist < y_dist:
                                x = x - x_dist
                            else:
                                y = y - y_dist

                        pos[n] = np.array((x,y))

                #plot netowrk edges
                edges = G.edges()
                print(edges)
                colors = [relationshipColorDict[G[u][v]['relationship']] for u,v in edges]
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
