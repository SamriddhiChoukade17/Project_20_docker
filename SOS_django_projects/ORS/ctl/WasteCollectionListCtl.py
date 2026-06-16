from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.models import WasteCollection
from service.service.WasteCollectionService import WasteCollectionService


class WasteCollectionListCtl(BaseCtl):

    count = 1

    def request_to_form(self, request_form):

        self.form["collection_id"] = request_form.get("collectionId", "").strip()
        self.form["vehicle_id"] = request_form.get("vehicleId", "").strip()
        self.form["driver_id"] = request_form.get("driverId", "").strip()
        self.form["route"] = request_form.get("route", "").strip()

    def display(self, request, params={}):

        WasteCollectionListCtl.count = self.form['page_no']

        self.page_list = self.get_service().search(self.form)

        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })

        return res

    def submit(self, request, params={}):

        self.form['page_no'] = WasteCollectionListCtl.count

        if request.POST['operation'] == "Next":
            WasteCollectionListCtl.count += 1
            self.form['page_no'] = WasteCollectionListCtl.count

        if request.POST['operation'] == "Previous":
            WasteCollectionListCtl.count -= 1
            self.form['page_no'] = WasteCollectionListCtl.count

        if request.POST['operation'] == "Search":
            WasteCollectionListCtl.count = 1
            self.form['page_no'] = WasteCollectionListCtl.count

        self.page_list = self.get_service().search(self.form)

        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })

        return res

    def get_template(self):
        return "ors/WasteCollectionList.html"

    def get_service(self):
        return WasteCollectionService()