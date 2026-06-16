from datetime import datetime

from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import WasteCollection
from service.service.WasteCollectionService import WasteCollectionService


class WasteCollectionCtl(BaseCtl):

    def preload(self, request):
        return self.preload_data

    def request_to_form(self, request_form):

        self.form["id"] = request_form.get("id", 0)
        self.form["collection_id"] = request_form.get("collectionId", "").strip()
        self.form["vehicle_id"] = request_form.get("vehicleId", "").strip()
        self.form["driver_id"] = request_form.get("driverId", "").strip()
        self.form["collection_time"] = request_form.get("collectionTime", "").strip()
        self.form["route"] = request_form.get("route", "").strip()

    def form_to_model(self, obj):

        obj.id = int(self.form.get("id", 0) or 0)

        obj.collection_id = self.form.get("collection_id")
        obj.vehicle_id = self.form.get("vehicle_id")
        obj.driver_id = self.form.get("driver_id")

        obj.collection_time = (
            datetime.strptime(
                self.form.get("collection_time"),
                "%Y-%m-%dT%H:%M"
            )
            if self.form.get("collection_time")
            else None
        )

        obj.route = self.form.get("route")

        return obj

    def model_to_form(self, obj):

        if obj is None:
            return

        self.form["id"] = obj.id
        self.form["collection_id"] = obj.collection_id
        self.form["vehicle_id"] = obj.vehicle_id
        self.form["driver_id"] = obj.driver_id

        self.form["collection_time"] = (
            obj.collection_time.strftime("%Y-%m-%dT%H:%M")
            if obj.collection_time
            else ""
        )

        self.form["route"] = obj.route

    def input_validation(self):

        super().input_validation()

        input_error = self.form.get("input_error", {})

        if DataValidator.isNull(self.form.get("collection_id")):
            input_error["collection_id"] = "Collection ID can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("vehicle_id")):
            input_error["vehicle_id"] = "Vehicle ID can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("driver_id")):
            input_error["driver_id"] = "Driver ID can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("collection_time")):
            input_error["collection_time"] = "Collection Time can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("route")):
            input_error["route"] = "Route can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):

        collection_id = int(params.get("id", 0))

        if collection_id > 0:
            obj = self.get_service().get(collection_id)
            self.model_to_form(obj)

        return render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })

    def submit(self, request, params={}):

        pk = int(self.form.get("id", 0))

        duplicate = self.get_service().get_model().objects.filter(
            collection_id=self.form.get("collection_id")
        )

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():

            self.form["error"] = True
            self.form["message"] = "Collection ID already exist"

        else:

            obj = self.form_to_model(WasteCollection())

            self.get_service().save(obj)

            self.form["id"] = obj.id
            self.form["error"] = False

            if pk > 0:
                self.form["message"] = "Waste Collection updated successfully"
            else:
                self.form["message"] = "Waste Collection added successfully"

        return render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })

    def get_template(self):
        return "ors/WasteCollection.html"

    def get_service(self):
        return WasteCollectionService()