from import_export import resources
from .models import Medication
import sys


def get_db_fk_field_names(db):
    your_fields = db._meta.local_fields
    # db_field_names = [f.name + '_id' if f.related_model is not None else f.name for f in your_fields]
    fk_field_names = [{"name": f.name, "model": f.related_model} for f in your_fields if f.related_model is not None]
    model_field_names = [f.name for f in your_fields]
    return fk_field_names  # , model_field_names


class MedicationResource(resources.ModelResource):
    class Meta:
        model = Medication
        import_id_fields = ['pharma_code']

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):  # https://github.com/django-import-export/django-import-export/issues/299
        id_index = dataset.headers.index('id')
        field_indexes = []
        for fk in get_db_fk_field_names(Medication):
            field_indexes.append({"index": dataset.headers.index(fk["name"]), "model": fk["model"]})
        print(field_indexes)
        # try:
        for row_number in range(len(dataset.dict)):
            row = list(dataset.lpop())
            print(row)
            # try:
            print("row: ", row_number)
            for index in field_indexes:
                print('\t'+str(index["index"]))
                obj, created = index["model"].objects.get_or_create(name=row[index["index"]])
                row[index["index"]] = index["model"].objects.filter(name=row[index["index"]])[0].pk
            print(row)
            # except IndexError:
            #     pass

            dataset.append(tuple(row))
        # except Exception as e:
        #     info = sys.exc_info()
        #     ex_type, ex, tb = info
        #     # traceback.print_tb(tb)
        #     print(type(ex_type), e)