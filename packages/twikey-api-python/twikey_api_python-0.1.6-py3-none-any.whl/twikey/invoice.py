import requests
import logging


class Invoice(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.logger = logging.getLogger(__name__)

    def create(self, data, origin=False, purpose=False, manual=False):
        url = self.client.instance_url("/invoice")
        data = data or {}
        self.client.refreshTokenIfRequired()
        headers = self.client.headers("application/json")
        if origin:
            headers["X-PARTNER"] = origin
        if purpose:
            headers["X-Purpose"] = purpose
        if manual:
            headers["X-MANUAL"] = "true"
        response = requests.post(url=url, json=data, headers=headers)
        json_response = response.json()
        if "ApiErrorCode" in response.headers:
            error = json_response
            raise Exception("Error creating : %s" % error)
        self.logger.debug("Added invoice : %s" % json_response["url"])
        return json_response

    def feed(self, invoice_feed, *includes):
        _includes = ""
        for include in includes:
            _includes += "&include=" + include

        url = self.client.instance_url("/invoice?include=customer" + _includes)

        self.client.refreshTokenIfRequired()
        response = requests.get(url=url, headers=self.client.headers())
        response.raise_for_status()
        if "ApiErrorCode" in response.headers:
            raise Exception(
                "Error feed : %s - %s"
                % (response.headers["ApiErrorCode"], response.headers["ApiError"])
            )
        feed_response = response.json()
        while len(feed_response["Invoices"]) > 0:
            self.logger.debug("Feed handling : %d" % (len(feed_response["Invoices"])))
            for invoice in feed_response["Invoices"]:
                self.logger.debug("Feed handling : %s" % invoice)
                invoice_feed.invoice(invoice)
            response = requests.get(url=url, headers=self.client.headers())
            if "ApiErrorCode" in response.headers:
                error = response.json()
                raise Exception("Error feed : %s" % error)
            feed_response = response.json()

    def geturl(self, invoice_id):
        return "%s/%s/%s" % (
            self.client.api_base.replace("api", "app"),
            self.client.merchant_id,
            invoice_id,
        )


class InvoiceFeed:
    def invoice(self, invoice):
        pass
