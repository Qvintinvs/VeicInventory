from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models import vehicle
from services import namelist_creator
from views import index_view


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Singleton(SQLAlchemy, model_class=vehicle.Base)

    main_page = providers.Singleton(
        index_view.IndexView,
        namelist_creator=namelist_creator.NamelistContentCreator("emission_vehicles"),
    )
