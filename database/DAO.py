from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_nodes(n_canzoni):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select a.* , count(t.TrackId) n_canzoni
        from album a , track t 
        where a.AlbumId = t.AlbumId 
        group by a.AlbumId 
        having n_canzoni > %s"""
        cursor.execute(query, (n_canzoni,))
        result = []
        for row in cursor:
            result.append(Album(**row))
        cursor.close()
        cnx.close()
        return result
