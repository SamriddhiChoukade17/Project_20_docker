from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import SmartDevice
from service.service.SmartDeviceService import SmartDeviceService


class SmartDeviceCtl(BaseCtl):


    def preload(self, request):
        return self.preload_data


    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["device_id"] = request_form.get("deviceId", "").strip()
        self.form["device_name"] = request_form.get("deviceName", "").strip()
        self.form["room"] = request_form.get("room", "").strip()
        self.form["status"] = request_form.get("status", "").strip()
        self.form["power_usage"] = request_form.get("powerUsage", "").strip()


    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.device_id = self.form.get("device_id")
        obj.device_name = self.form.get("device_name")
        obj.room = self.form.get("room")
        obj.status = self.form.get("status")
        obj.power_usage = self.form.get("power_usage")

        return obj


    def model_to_form(self, obj):
        if obj is None:
            return

        self.form["id"] = obj.id
        self.form["device_id"] = obj.device_id
        self.form["device_name"] = obj.device_name
        self.form["room"] = obj.room
        self.form["status"] = obj.status
        self.form["power_usage"] = obj.power_usage

    def input_validation(self):
        super().input_validation()

        input_error = self.form.get("input_error", {})
        self.form["input_error"] = input_error

        if DataValidator.isNull(self.form.get("device_id")):
            input_error["device_id"] = "Device ID can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("device_name")):
            input_error["device_name"] = "Device Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("room")):
            input_error["room"] = "Room can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("status")) or self.form.get("status") == "0":
            input_error["status"] = "Status can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("power_usage")):
            input_error["power_usage"] = "Power Usage can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        device_id = int(params.get("id", 0))

        if device_id > 0:
            obj = self.get_service().get(device_id)
            self.model_to_form(obj)

        return render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })


    def submit(self, request, params={}):
        pk = int(self.form.get("id", 0))

        duplicate = self.get_service().get_model().objects.filter(
            device_id=self.form.get("device_id")
        )

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():

            self.form["error"] = True
            self.form["message"] = "Device ID already exist"

        else:

            obj = self.form_to_model(SmartDevice())

            self.get_service().save(obj)

            self.form["id"] = obj.id
            self.form["error"] = False

            if pk > 0:
                self.form["message"] = "Smart Device updated successfully"
            else:
                self.form["message"] = "Smart Device added successfully"

        return render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })


    def get_template(self):
        return "ors/SmartDevice.html"


    def get_service(self):
        return SmartDeviceService()
