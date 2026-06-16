from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.models import SmartDevice
from service.service.SmartDeviceService import SmartDeviceService


class SmartDeviceListCtl(BaseCtl):


    count = 1


    def request_to_form(self, request_form):
        self.form["device_id"] = request_form.get("deviceId", "").strip()
        self.form["device_name"] = request_form.get("deviceName", "").strip()
        self.form["room"] = request_form.get("room", "").strip()
        self.form["status"] = request_form.get("status", "").strip()


    def display(self, request, params={}):
        SmartDeviceListCtl.count = self.form['page_no']

        self.page_list = self.get_service().search(self.form)

        return render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })


    def submit(self, request, params={}):
        self.form['page_no'] = SmartDeviceListCtl.count

        if request.POST['operation'] == "Next":
            SmartDeviceListCtl.count += 1
            self.form['page_no'] = SmartDeviceListCtl.count

        if request.POST['operation'] == "Previous":
            SmartDeviceListCtl.count -= 1
            self.form['page_no'] = SmartDeviceListCtl.count

        if request.POST['operation'] == "Search":
            SmartDeviceListCtl.count = 1
            self.form['page_no'] = SmartDeviceListCtl.count

        self.page_list = self.get_service().search(self.form)

        return render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })


    def get_template(self):
        return "ors/SmartDeviceList.html"


    def get_service(self):
        return SmartDeviceService()
