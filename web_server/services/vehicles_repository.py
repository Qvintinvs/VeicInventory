from flask_sqlalchemy import SQLAlchemy
from models.vasques_emission_model import VasquesEmissionModel


class VehiclesRepository:
    def __init__(self, sql_db: SQLAlchemy):
        self.__db = sql_db

    def insert_a(self, new_vehicle: VasquesEmissionModel):
        self.__db.session.add(new_vehicle)

        self.__db.session.commit()

    def read_vehicles_data(self):
        vehicles_read = self.__db.session.query(VasquesEmissionModel).limit(5).all()

        return tuple(vehicle.to_dict() for vehicle in vehicles_read)

    def delete_vehicle_by(self, its_id: int):
        self.__db.session.query(VasquesEmissionModel).filter_by(id=its_id).delete()

        self.__db.session.commit()

    def edit(self, edited_items: dict, its_id: int):
        test = self.__db.session.query(VasquesEmissionModel).filter_by(id=its_id).first()
        edited_items["id"] = its_id
        print(f"edited_items: {edited_items}")
        
        for key, value in edited_items.items():
            print(f"Key: {key}, Value: {value}, Expected Type: {type(getattr(test, key, None))}")
            print(f"test: {test}")
            print(f"key: {key}")
            print(f"value: {value}")
            
            if key == "subcategory":
                subcategory_obj = test.subcategory
                if subcategory_obj:
                    setattr(test, key, subcategory_obj)
                else:
                    print(f"Warning: No subcategory found with name {value}")
            else:
                setattr(test, key, value)

            print("attr has been assigned")
            print("\n")

        print(test.to_dict())
        # print(test.fuel)

        self.__db.session.commit()

        test1 = self.__db.session.query(VasquesEmissionModel).filter_by(id=its_id).first()
        print(test1.to_dict())