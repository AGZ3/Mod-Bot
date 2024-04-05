# main.py

# Imports
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from link_manager import load_pending_links, save_pending_links, remove_pending_link, get_toggle_state, set_toggle_state, links
from badwords_manager import load_badwords, save_badwords, normalize_message


load_dotenv()
# Retrieve bot token from .env and assign it to TOKEN
TOKEN = os.getenv('DISCORD_KEY')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
# On ready event: print success message when bot connects
async def on_ready():
    print(f"{bot.user} has connected to Discord!")



#### ON MESSAGE, CHECK FOR LINKS OR BLACKLISTED WORDS ####
    
@bot.event
async def on_message(message):
    badwords = load_badwords()   
    pending_links = load_pending_links()

    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
        return  # Ensure no further processing if it's a valid command     

    # split contents of message sent by user for easy link detection
    no_space = ''.join(message.content.split()).lower()

    # Only responds if the message comes from a Discord user
    if message.author == bot.user:
        return

    # Detect Links and delete followed by a warning message
    
    pending_links_toggle = get_toggle_state()

    try:
        if pending_links_toggle == 1:
            for link in links:
                if link in no_space:
                    # Delete the original message
                    await message.delete()

                    await message.channel.send(f'Hey {message.author.name}, the link you sent is pending review. Please wait for a mod to review your message.')
                    
                    print("Link detected. Trying to DM moderators.")
                    
                    # Load the current pending links from the file
                    pending_links = load_pending_links()
                    
                    # Update pending_links with the new detected link
                    pending_links[str(message.author.id)] = {
                        "link": message.content,
                        "channel": message.channel.id,
                        "user": message.author.id,
                        "username": message.author.name
                    }
                    
                    # Save the updated pending links back to the file
                    save_pending_links(pending_links)

                    # Notify moderators
                    moderators = [member for member in message.guild.members if any(role.name == 'Moderator' for role in member.roles)]
                    print(f"Found {len(moderators)} moderators.")

                    for moderator in moderators:
                        print(f"Attempting to DM {moderator}.")
                        try:
                            dm_channel = await moderator.create_dm()
                            pending_links[message.author.id] = {"link": message.content, "channel": message.channel.id,
                                                                "user": message.author.id}
                            await dm_channel.send(
                                f"Hey {moderator}! It looks like your approval is needed for this message: \n{message.content}. "
                                f"\nType '!approve {message.author.id}' to approve.")
                            print(f"DM sent to {moderator}.")
                            print(f'moderator loop: {str(pending_links)}')
                            return
                        except Exception as e:
                            print(f"Could not DM {moderator} due to {e}")
        elif pending_links_toggle == 0:
            for link in links:
                if link in no_space:
                    # Delete the original message
                    await message.channel.send(f"Hey {message.author.name}, links aren't allowed in this server. Please abide by the admin's rules!")
                    return
    except Exception as e:
        print(f"An error occured in on_message: {e}")

    # Detect bad words from badwords list and remove them from the channel
    normalized_message = normalize_message(no_space)
    for i in badwords:
        if i in normalized_message:
            await message.delete()
            await message.channel.send("You can't use those words in this channel!")
            return

    await bot.process_commands(message)  # Allow bot to process commands after message has been received

#### HELLO COMMAND ####
@bot.command()
async def hello(ctx):
    await ctx.send('Hello, I am Mobi the Mod Bot!')
    return

#### APPROVE PENDING LINKS ####
@bot.command()
async def approve(ctx, user_id: int):
    pending_links = load_pending_links()
    user_id_str = str(user_id)  # Converting user_id to string to maintain consistency
    
    # Debugging: Print the keys present in pending_links
    print(f"Keys in pending_links: {list(pending_links.keys())}")

    if user_id_str in pending_links:
        try:
            channel_id = pending_links[user_id_str].get('channel', None)  # Using .get() method to avoid KeyError

            if channel_id is not None:  # Check if channel_id exists
                channel = bot.get_channel(channel_id)

                if channel:
                    await channel.send(f"{pending_links[user_id_str]['username']}: \n{pending_links[user_id_str]['link']} (Approved by {ctx.author.name})")
                    print (f"Link Approved by: {ctx.author.name}, {ctx.author.id}")
                    remove_pending_link(user_id_str)
                    await ctx.send("Link approved and posted.")
                else:
                    await ctx.send("Could not find the channel to post the approved link.")
            else:
                await ctx.send("Channel information not found.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    else:
        await ctx.send("No link found for approval.")

@bot.command()
async def link_approval(ctx, word=None):
    if word is None:
        await ctx.send('Missing arguments. Use !toggle_link_approval [on/off]')
        return
    if ctx.message.author.guild_permissions.administrator:
        if word.lower() == "on":
            set_toggle_state(1)  # Turn on link approval
            await ctx.send('Link Approval has been turned ON!')
            print("Link Approval has been turned ON")
        elif word.lower() == "off":
            set_toggle_state(0)  # Turn off link approval
            await ctx.send('Link Approval has been turned OFF!')
            print("Link Approval has been turned OFF")
        else:
            await ctx.send('Invalid argument. Use !toggle_link_approval [on/off]')
    else:
        await ctx.send('You do not have the permission to use this command.')

#### ADMIN ADD/REMOVE WORDS FROM BADWORDS LIST ####
@bot.command()
async def words(ctx, action=None, *, word=None):
    
    badwords = load_badwords()   

    if action is None or word is None:
        await ctx.send('Missing arguments. Use !words [add/remove] [word]')
        return
        
    if ctx.message.author.guild_permissions.administrator:
        if action.lower() == "add":
            if word not in badwords:
                badwords.append(word)
                save_badwords(badwords)
                await ctx.send(f'Added "{word}" to the list of bad words.')
            else:
                await ctx.send(f'Word "{word}" is already in the list.')
        elif action.lower() == "remove":
            if word in badwords:
                badwords.remove(word)
                save_badwords(badwords)
                await ctx.send(f'Removed "{word}" from the list of bad words.')
            else:
                await ctx.send(f'Word "{word}" is not in the list.')
        else:
            await ctx.send('Invalid action. Use "add" to add a word or "remove" to remove a word.')
    else:
        await ctx.send('You do not have the permission to use this command.')


# Start bot
bot.run(TOKEN)
