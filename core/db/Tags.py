from datetime import datetime
from typing import List, Union
from .Core import BaseDB

class Tag:
    def __init__(self, name:str, content: str, attachments: List[str], created_at: datetime, author: Union[str, int]):
        self.name = name
        self.content = content
        self.attachments = attachments
        self.created_at = created_at
        self.author = str(author)

        self.data = {
            "name": self.name,
            "content": self.content,
            "attachments": self.attachments,
            "created_at": self.created_at,
            "author": self.author
        }

class TagDB(BaseDB):
    def __init__(self):
        super().__init__(col="tags")
        self.DEFAULT = {
            "create": None,
            "delete": None,
            "use": None,
            "edit": None,
            "tags": []
        }
    
    def get(self, guild_id):
        guild_id = str(guild_id)

        return self.col.find_one({ "guild": guild_id })
    
    def add(self, guild_id, tag: Tag):
        guild_id = str(guild_id)

        if not self.get(guild_id):
            self.col.insert_one({ "guild": guild_id, **self.DEFAULT })

        self.col.update_one({
            "guild": guild_id
        }, {
            "$push": {
                "tags": tag.data
            }
        })

    def delete(self, guild_id, tag_name: str):
        guild_id = str(guild_id)

        if not self.get(guild_id):
            self.col.insert_one({ "guild": guild_id, **self.DEFAULT })

        self.col.update_one({
            "guild": guild_id
        }, {
            "$pull": {
                "tags": {
                    "name": tag_name
                }
            }
        })
    
    def edit(self, guild_id, tag: Tag):
        guild_id = str(guild_id)

        if not self.get(guild_id):
            self.col.insert_one({ "guild": guild_id, **self.DEFAULT })

        self.delete(guild_id, tag.name)

        self.add(guild_id, tag)