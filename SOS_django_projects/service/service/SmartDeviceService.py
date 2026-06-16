from service.models import SmartDevice
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.core.paginator import Paginator


class SmartDeviceService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("device_id", None)
        if DataValidator.isNotNull(value):
            query = query.filter(device_id__istartswith=value.strip())

        value = params.get("device_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(device_name__istartswith=value.strip())

        value = params.get("room", None)
        if DataValidator.isNotNull(value):
            query = query.filter(room__istartswith=value.strip())

        value = params.get("status", None)
        if DataValidator.isNotNull(value):
            query = query.filter(status__istartswith=value.strip())

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return SmartDevice