from service.models import WasteCollection
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.core.paginator import Paginator


class WasteCollectionService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("collection_id", None)
        if DataValidator.isNotNull(value):
            query = query.filter(collection_id__istartswith=value.strip())

        value = params.get("vehicle_id", None)
        if DataValidator.isNotNull(value):
            query = query.filter(vehicle_id__istartswith=value.strip())

        value = params.get("driver_id", None)
        if DataValidator.isNotNull(value):
            query = query.filter(driver_id__istartswith=value.strip())

        value = params.get("route", None)
        if DataValidator.isNotNull(value):
            query = query.filter(route__istartswith=value.strip())

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return WasteCollection