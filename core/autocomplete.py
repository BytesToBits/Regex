import disnake
from core.db.Tags import TagDB

def autocomplete_tag(inter:disnake.ApplicationCommandInteraction, val:str):      
        db = TagDB()
        doc = db.get(inter.guild_id)
        
        if doc:
            return list(map(lambda k: k["name"], filter(lambda tag: val.lower() in tag["name"].lower(), doc["tags"])))[:25]
        
        return []
