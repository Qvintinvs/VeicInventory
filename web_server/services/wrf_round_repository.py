from flask_sqlalchemy import SQLAlchemy
from models.wrf_round import WRFRound
from models.wrf_round_status import WRFRoundStatus
from services.wrf_round_processor import WRFRoundProcessor
from sqlalchemy import asc


class WRFRoundRepository:
    """Will deal with the database rounds"""

    def __init__(self, sql_db: SQLAlchemy, wrf_round_processor: WRFRoundProcessor):
        self.__db = sql_db
        self.__processor = wrf_round_processor

    def save_emission_round(self, new_round: WRFRound):
        self.__db.session.add(new_round)

        self.__db.session.commit()

    def enqueue_pending_round(self):
        oldest_pending_round = (
            self.__db.session.query(WRFRound)
            .filter(WRFRound.status == WRFRoundStatus.PENDING)
            .order_by(asc(WRFRound.timestamp))
            .first()
        )

        if not oldest_pending_round:
            return

        self.__processor.enqueue_round(oldest_pending_round)

        oldest_pending_round.status = WRFRoundStatus.RUNNING

        self.__db.session.commit()

    def get_wrf_round_by_id(self, round_id: int):
        return self.__db.session.get(WRFRound, round_id)
