import json


class MatchWriter(object):
    def save(self, filter_ids, matches):
        raise NotImplementedError()


class PostgresMatchWriter(MatchWriter):
    def __init__(self, conn):
        self.conn = conn

    def _serialize(self, matches):
        dicts = [m.__dict__ for m in matches if m is not None]
        return json.dumps(dicts)

    def save(self, channel, filter_ids, matches):
        ms_serialized = self._serialize(matches)

        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO matches (matches)
                VALUES (%s)
            """, (ms_serialized,))

            cursor.execute("""
                SELECT id FROM matches
                WHERE matches = %s
            """, (ms_serialized,))
            match_id = cursor.fetchone()

            for f_id in filter_ids:
                cursor.execute("""
                    INSERT INTO match_filters (filter_id, match_id)
                    VALUES (%s, %s)
                """, (f_id, match_id))
        self.conn.commit()
