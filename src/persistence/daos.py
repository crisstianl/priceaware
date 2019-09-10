import logging
from .models import Store, Item

"""
Store database operations
"""
LOGGER = logging.getLogger('django.db.backends')    
LOGGER.setLevel(logging.DEBUG)                      
LOGGER.addHandler(logging.StreamHandler())

def drop_db():
    from os import remove
    remove("db.sqlite3")

class StoreDAO(object):
    
    def __init__(self):
        super().__init__()

    def query_by_id(self, id):
        """
        query by id
        """
        return Store.objects.get(pk=id)

    def query_by_name(self, name):
        """
        query by name
        """
        return Store.objects.filter(title__icontains = str(name))       

    def query_all(self, offset=0, limit=100):
        """
        query all from offset until limit and order by title asc
        """
        return Store.objects.all().order_by('-rating', 'title')[offset:limit]

    def insert(self, instance):
        """
        insert a new record, id must be null
        """
        if instance.id:
            raise ValueError("store id must be null")

        instance.save()
        return True

    def update(self, instance):
        if not instance.id:
            raise ValueError("store id must be valid")
            
        instance.save()
        return True

    def delete_by_id(self, id):
        if not id:
            raise ValueError("store id must be valid")

        instance = Store.objects.get(pk=id)
        if instance:
            instance.delete()
            return True
        return False 

    def delete_all(self):
        Store.objects.all().delete()


"""
Item database operations
"""
class ItemDAO(object):
    def __init__(self):
        super().__init__()

    def query_by_id(self, id):
        """
        query by id
        """
        return Item.objects.get(pk=id)      

    def query_all(self, offset=0, limit=100):
        """
        query all from offset until limit and order by title asc
        """
        return Item.objects.all().order_by('-updated', 'name')[offset:limit]

    def delete_by_id(self, id):
        if not id:
            raise ValueError("item id must be valid")

        instance = Item.objects.get(pk=id)
        if instance:
            instance.delete()
            return True
        return False 

    def delete_all(self):
        Item.objects.all().delete()