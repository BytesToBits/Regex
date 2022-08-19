import disnake
from core.db.Tags import TagDB

def autocomplete_tag(inter:disnake.ApplicationCommandInteraction, val:str):      
        db = TagDB()
        doc = db.get(inter.guild_id)
        
        if doc:
            return list(filter(lambda tag: val.lower() in tag["name"].lower(), doc["tags"]))
        
        return []
