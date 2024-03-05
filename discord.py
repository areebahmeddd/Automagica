import discord
import requests

BOT_TOKEN = " "

bot = discord.Client()

@bot.event
async def on_ready():
    print(f'\n[{bot.user.name}] status: Online (ID: {bot.user.id})\n')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("-github"):
        command_parts = message.content.split()

        if len(command_parts) != 2:
            syntax_error = discord.Embed(
                title = "❌ Invalid Command Format",
                color = discord.Color.yellow()
            )

            await message.channel.send(embed = syntax_error)
        else:
            github_username = command_parts[1]
            github_data = await fetch_github_profile(github_username)

            if github_data:
                user_profile = discord.Embed(
                    title = f'👤 {github_data["name"]} https://github.com/{github_username}',
                    description = f'📈 {github_data["followers"]} followers -- 📊 {github_data["following"]} following',
                    color = discord.Color.green()
                )

                for index, (repo_title, repo_description) in enumerate(github_data["repositories_info"], start = 1):
                    user_profile.add_field(name = f'📦 {index}. {repo_title}', value = repo_description, inline = False)

                user_profile.set_thumbnail(url = github_data["avatar_url"])

                await message.channel.send(embed = user_profile)
            else:
                profile_unavailable = discord.Embed(
                    title = f'🔎 GitHub profile "{github_username}" not found',
                    color = discord.Color.red()
                )

                await message.channel.send(embed = profile_unavailable)

async def fetch_github_profile(username):
    user_response = requests.get(f'https://api.github.com/users/{username}')
    repository_response = requests.get(f'https://api.github.com/users/{username}/repos')

    if user_response.status_code == 200 and repository_response.status_code == 200:
        user_data = user_response.json()
        repository_data = repository_response.json()

        repositories_info = [
            (repo.get("name", 0), repo.get("description", 0))
            for repo in repository_data[:5]
        ]

        return {
            "name": user_data.get("name", 0),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
            "avatar_url": user_data.get("avatar_url", 0),
            "repositories_info": repositories_info
        }
    else:
        return None

bot.run(BOT_TOKEN)