import discord
import os
from dotenv import load_dotenv

#load token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

guesses = int(os.getenv("GUESSES"))
leaderboard = int(os.getenv("LEADERBOARD"))
answer_id = int(os.getenv("ANSWER_ID"))
leaderboard_med = int(os.getenv("LEADERBOARD_MED"))

song = "TECHNIUM"
main_artist = "Fit For A King"
main_artist2 = "The Plot In You"
artist = "Fit For A King, The Plot In You"
link = "https://open.spotify.com/track/5Pk2Fy0i0BuzfGaCFpB9DB?si=c66d4beb18ec4583"
answer = (f"[{song} by {artist}]({link})")

class MyClient(discord.Client):
    def __init__ (self, *, intents):
        super().__init__(intents = intents)
        self.winner_declared = False
        self.artist_winner = False
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self,message):
        #Prevent bot from replying to itself
        if message.author == self.user:
            return

        #react if song is correct
        if message.channel.id == guesses:
            guess_parts = message.content.lower().split(" by ")
            if len(guess_parts) == 2:
                guessed_song = guess_parts[0].strip()
                guessed_artist = guess_parts[1].strip()
                if guessed_song == song.lower() and guessed_artist == artist.lower():
                    await message.add_reaction("✅")
                    if not self.winner_declared:
                        self.winner_declared = True

                        #update leaderboard
                        leader_channel = self.get_channel(leaderboard)
                        leader_message = await leader_channel.fetch_message(leaderboard_med)

                        user_tag = message.author.mention
                        lines = leader_message.content.splitlines()
                        new_lines = []
                        updated = False

                        for line in lines:
                            if line.startswith(user_tag):
                                try:
                                    count = float(line.split(":")[1].strip())
                                except ValueError:
                                    count = 0.0

                                new_lines.append(f"{user_tag}: {count + 1}")
                                updated = True
                            else:
                                new_lines.append(line)
                        if not updated:
                            new_lines.append(f"{user_tag}: 1")

                        new_content = "\n".join(new_lines)
                        await leader_message.edit(content=new_content)

                        #put answer into answer channel
                        answer_channel = self.get_channel(answer_id)
                        await answer_channel.send(f"Answer:\n {answer}")
                        await answer_channel.send(f"Congratulations:\n {user_tag} 🎉")

                        with open("songs.txt", "a") as file:
                            file.write(f"\n{song.lower()} {artist.lower()}")
                            file.close()

                #elif guessed_song.lower() == song and main_artist.lower() in guessed_artist:
                    #await message.add_reaction("🟦")
                    #await message.add_reaction("🟪")

                if main_artist.lower() in guessed_artist or main_artist2.lower() in guessed_artist and not self.artist_winner:
                    self.artist_winner = True
                    if not self.winner_declared:
                        await message.add_reaction("🟦")
                    #update leaderboard
                    leader_channel = self.get_channel(leaderboard)
                    leader_message = await leader_channel.fetch_message(leaderboard_med)

                    user_tag = message.author.mention
                    lines = leader_message.content.splitlines()
                    new_lines = []
                    updated = False

                    for line in lines:
                        if line.startswith(user_tag):
                            try:
                                count = float(line.split(":")[1].strip())
                            except ValueError:
                                count = 0.0
                            new_lines.append(f"{user_tag}: {count + 0.5}")
                            updated = True
                        else:
                            new_lines.append(line)
                    if not updated:
                        new_lines.append(f"{user_tag}: 1")

                    new_content = "\n".join(new_lines)
                    await leader_message.edit(content=new_content)

                    #put answer into answer channel
                    answer_channel = self.get_channel(answer_id)
                    await answer_channel.send(f"The Artist is:\n {main_artist}")
                    await answer_channel.send(f"Congratulations:\n {user_tag} 🎉")

                elif main_artist.lower() in guessed_artist or main_artist2 in guessed_artist:
                    await message.add_reaction("🟦")

                #elif guessed_song != song.lower() and guessed_artist != artist.lower():
                    #await message.add_reaction("🟥")



intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)