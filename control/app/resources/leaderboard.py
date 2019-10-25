import falcon

from app.resources import BaseResource
from app.leaderboard_status import LeaderboardStatus


class LeaderboardResource(BaseResource):
    leaderboard_control = None
    conn = None

    def __init__(self, leaderboard_control, conn):
        super(LeaderboardResource, self).__init__()
        self.leaderboard_control = leaderboard_control
        self.conn = conn

    def on_post(self, req, resp):
        result = self.conn.execute(self.leaderboard_control.insert().values(status=LeaderboardStatus.NOT_STARTED.value))
        inserted_leaderboard_id = result.inserted_primary_key[0]
        resp.status=falcon.HTTP_200
        resp.media={
            "leaderboard_id": inserted_leaderboard_id,
        }
        print(resp)

    def on_post_start(self, req, resp, leaderboard_id):
        query=self.leaderboard_control.update().values(
            status=LeaderboardStatus.STARTED.value)
        query=query.where(
            self.leaderboard_control.columns.leaderboard_id == leaderboard_id)
        result=self.conn.execute(query)

        query2 = self.leaderboard_control.select()
        result=self.conn.execute(query2)
        for updated in result:
            print(updated)
            resp.status=falcon.HTTP_200
            resp.media={
                "leaderboard_id": updated["leaderboard_id"],
                "status": updated["status"]
            }
            print(resp)
