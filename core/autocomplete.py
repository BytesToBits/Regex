import disnake
from core.db.Tags import TagDB

def autocomplete_tag(inter:disnake.ApplicationCommandInteraction, val:str):
        ret = []
        
        db = TagDB()
        doc = db.get(inter.guild_id)
        
        if doc and "tags" in doc:
            val = val.lower()
            for i in doc["tags"]:
                if val in i["name"].lower(): ret.append(i["name"])

        return ret
