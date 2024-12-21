from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy
from models import vasques_vehicle_model, vehicles_database
from services import namelist_creator
from views import index_view


class InventoryAppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.Singleton(SQLAlchemy, model_class=vasques_vehicle_model.Base)

    vehicular_inventory = providers.Singleton(
        vehicles_database.VehiclesDatabase, db=database
    )

    main_page = providers.Singleton(
        index_view.IndexView,
        vehicular_inventory=vehicular_inventory,
        namelist_creator=namelist_creator.NamelistContentCreator("emission_vehicles"),
    )
