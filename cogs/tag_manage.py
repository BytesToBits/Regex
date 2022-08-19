import asyncio
from datetime import datetime
import disnake
from disnake.ext import commands
from core.autocomplete import autocomplete_tag

from core.db.Tags import Tag, TagDB

class TagManage(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.slash_command(
        name="tags-manage",
        dm_permission=False
    )
    async def tag_manage(self, _): return

    @tag_manage.sub_command(
        name="create",
        description="Create a new tag",
        options=[
            disnake.Option(
                name="name",
                description="Name of the tag",
                required=True,
                max_value=40
            )
        ]
    )
    async def tag_create(self, inter:disnake.CommandInteraction, name:str):
        db = TagDB()
        doc = db.get(inter.guild_id)

        if not inter.author.guild_permissions.manage_guild:
            if not doc: return await inter.send("You do not have permission to create tags!", ephemeral=True)

            if doc["create"] and not inter.author.get_role(int(doc["create"])): return await inter.send("You do not have permission to create tags!", ephemeral=True)

        TAG = next((i for i in doc["tags"] if i["name"] == name), None)

        if TAG: return await inter.send("This tag already exists!", ephemeral=True)

        await inter.response.send_modal(
            title="Create Tag",
            custom_id="create_tag_modal",
            components=[
                disnake.ui.TextInput(
                    label="Tag Content",
                    custom_id="content",
                    style=disnake.TextInputStyle.multi_line,
                    required=True,
                    max_length=2000
                )
            ]
        )
        
        try:
            modal_inter: disnake.ModalInteraction = await inter.bot.wait_for(
                'modal_submit',
                check=lambda mod: mod.custom_id == "create_tag_modal" and mod.author.id == inter.author.id,
                timeout=300
            )
        except asyncio.TimeoutError:
            return

        tag = Tag(name, modal_inter.text_values.get("content"), [], datetime.utcnow(), inter.author.id)

        await modal_inter.response.defer(with_message=True)

        db.add(inter.guild_id, tag)

        return await modal_inter.edit_original_message("Tag created!")

    @tag_manage.sub_command(
        name="delete",
        description="Delete a tag",
        options=[
            disnake.Option(
                name="name",
                description="Name of the tag",
                required=True,
                autocomplete=True
            )
        ]
    )
    async def tag_delete(self, inter:disnake.CommandInteraction, name:str):
        db = TagDB()
        doc = db.get(inter.guild_id)

        TAG = next((i for i in doc["tags"] if i["name"] == name), None)

        if not TAG: return await inter.send("This tag does not exist!")

        if not inter.author.guild_permissions.manage_guild and not str(inter.author.id) == TAG["author"]:
            if doc["delete"] and not inter.author.get_role(int(doc["delete"])): return await inter.send("You do not have permission to delete tags!", ephemeral=True)

        db.delete(inter.guild_id, name)

        return await inter.send("Tag deleted!", ephemeral=True)
    
    @tag_delete.autocomplete("name")
    async def name_autocomp(name:str,inter:disnake.ApplicationCommandInteraction,val:str):
        return autocomplete_tag(inter,val)

    @tag_manage.sub_command(
        name="edit",
        description="Edit a tag",
        options=[
            disnake.Option(
                name="name",
                description="Name of the tag",
                required=True,
                autocomplete=True
            )
        ]
    )
    async def tag_edit(self, inter:disnake.CommandInteraction, name:str):
        db = TagDB()
        doc = db.get(inter.guild_id)

        if not doc: return await inter.send("This server does not have any tags!", ephemeral=True)

        TAG = next((i for i in doc["tags"] if i["name"] == name), None)

        if not TAG: return await inter.send("This tag does not exist!")

        if not inter.author.guild_permissions.manage_guild and not str(inter.author.id) == TAG["author"]:
            if doc["edit"] and not inter.author.get_role(int(doc["delete"])): return await inter.send("You do not have permission to edit tags!", ephemeral=True)

        await inter.response.send_modal(
            title="Edit Tag",
            custom_id="edit_tag_modal",
            components=[
                disnake.ui.TextInput(
                    label="Tag Content",
                    custom_id="content",
                    style=disnake.TextInputStyle.multi_line,
                    required=True,
                    max_length=2000
                )
            ]
        )
        
        try:
            modal_inter: disnake.ModalInteraction = await inter.bot.wait_for(
                'modal_submit',
                check=lambda mod: mod.custom_id == "edit_tag_modal" and mod.author.id == inter.author.id,
                timeout=300
            )
        except asyncio.TimeoutError:
            return

        tag = Tag(name, modal_inter.text_values.get("content"), [], datetime.utcnow(), inter.author.id)

        await modal_inter.response.defer(with_message=True)

        db.edit(inter.guild_id, tag)

        return await modal_inter.edit_original_message("Tag edited!")
    
    @tag_edit.autocomplete("name")
    async def name_autocomp(name:str,inter:disnake.ApplicationCommandInteraction,val:str):
        return autocomplete_tag(inter,val)

def setup(bot):
    bot.add_cog(TagManage(bot))