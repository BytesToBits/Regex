from disnake.ext import commands
import disnake

from core.db.Tags import TagDB

class SearchModal(disnake.ui.Modal):
    def __init__(self, tags):
        self.tags = tags

        components = [
            disnake.ui.TextInput(
                label="Tag Name",
                placeholder="Epic",
                style=disnake.TextInputStyle.short,
                max_length=40,
                custom_id="tag_name",
                required=True
            )
        ]

        super().__init__(title="Search Tag", custom_id="search_tag", components=components)

    async def callback(self, inter:disnake.ModalInteraction):
        TAG: dict = next((i for i in self.tags if i["name"] == inter.text_values.get("tag_name")), None)

        if not TAG:
            return await inter.send("This tag does not exist!", ephemeral=True)
        
        return await inter.send(embed=disnake.Embed(
            title=f"Tag Info: {TAG['name']}",
            color=disnake.Color.orange(),
            description=TAG['content']
        ), ephemeral=True)
    
    async def on_error(self, _, inter: disnake.ModalInteraction):
        return await inter.send("Oops, something went wrong!", ephemeral=True)

class TagView(disnake.ui.View):
    def __init__(self, tags, embed: disnake.Embed, author:int, all_tags):
        super().__init__(timeout=300)
        
        self.all_tags = all_tags
        self.tags = tags
        self.embed = embed
        self.page = 0
        self.author = author
    
    @disnake.ui.button(emoji="⬅️")
    async def move_back(self, _, inter:disnake.MessageInteraction):
        if not inter.author.id == self.author: return await inter.send("You cannot use this button.", ephemeral=True)

        self.page -= 1

        self.embed.description = '\n'.join(list(map(lambda k:f'`{k["name"]}`', self.tags[self.page%len(self.tags)])))
        self.embed.set_footer(text=f"Page {self.page%len(self.tags)+1}/{len(self.tags)}")

        return await inter.response.edit_message(embed=self.embed, view=self)

    @disnake.ui.button(emoji="🔍")
    async def search(self, _, inter:disnake.MessageInteraction):
        if not inter.author.id == self.author: return await inter.send("You cannot use this button.", ephemeral=True)

        return await inter.response.send_modal(SearchModal(self.all_tags))

    @disnake.ui.button(emoji="➡️")
    async def move_front(self, _, inter:disnake.MessageInteraction):
        if not inter.author.id == self.author: return await inter.send("You cannot use this button.", ephemeral=True)

        self.page += 1

        self.embed.description = '\n'.join(list(map(lambda k:f'`{k["name"]}`', self.tags[self.page%len(self.tags)])))
        self.embed.set_footer(text=f"Page {self.page%len(self.tags)+1}/{len(self.tags)}")

        return await inter.response.edit_message(embed=self.embed, view=self)

class Tags(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.TAGS_PER_PAGE = 15

    @commands.slash_command(
        name="tags",
        dm_permission=False,
        description="View tag list"
    )
    async def tags(self, inter:disnake.CommandInteraction):
        db = TagDB()
        doc = db.get(inter.guild_id)

        if not doc: return await inter.send("This server does not have any tags!", ephemeral=True)
        if doc["use"] and not inter.author.get_role(int(doc["use"])): return await inter.send("You do not have permission to view tags!", ephemeral=True)

        tags = [doc["tags"][x:x+self.TAGS_PER_PAGE] for x in range(0, len(doc["tags"]), self.TAGS_PER_PAGE)]

        embed= disnake.Embed(
                    color=disnake.Color.blurple(),
                    description='\n'.join(list(map(lambda k:f'`{k["name"]}`', tags[0])))
                )
        embed.set_footer(text=f"Page 1/{len(tags)}")

        view = TagView(tags, embed, inter.author.id, doc["tags"])

        return await inter.send(
            embed=embed,
            view=view
        )
    
    @commands.slash_command(
        name="tag",
        dm_permission=False,
        description="Send a tag to the server",
        options=[
            disnake.Option(
                name="tag_name",
                type=disnake.OptionType.string,
                required=True,
                description="Name of the tag to send"
            )
        ]
    )
    async def tag(self, inter:disnake.CommandInteraction, tag_name:str):
        db = TagDB()
        doc = db.get(inter.guild_id)

        if not doc: return await inter.send("This server does not have any tags!", ephemeral=True)
        if doc["use"] and not inter.author.get_role(int(doc["use"])): return await inter.send("You do not have permission to use tags!", ephemeral=True)

        TAG = next((i for i in doc["tags"] if i["name"] == tag_name), None)

        if not TAG: return await inter.send("This tag does not exist!", ephemeral=True)

        return await inter.send(
            content=TAG["content"],
            allowed_mentions=disnake.AllowedMentions.none
        )

def setup(bot):
    bot.add_cog(Tags(bot))