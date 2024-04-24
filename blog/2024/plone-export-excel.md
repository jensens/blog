---
blogpost: true
date: Feb 16, 2024
author: Jens W. Klein
location: Austria
category: Plone, Zope
language: en
---

# Exporting Plone content to Excel

I have customers who want to export some contents of a Plone site to Excel.
Since this is a database-like site, there are different areas resulting in different Excel files.

## OpenPyXL

I found the [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/) library for Python very useful as a base for my export.
With OpenPyXL you create an Workbook, add Sheets and fill them with data.

## Base Class

Because I need this in different parts of my project, I created a base class for the export.
It contains the logic needed to create the Excel file and to send it to the browser.
The actual data is provided by the `sheet_info_factory` method generator.
It needs to be implemented by the subclass and returns a generator of "sheets": each a dict with the sheet `name`, the `header` and the `rows`.

```python
from Products.Five.browser import BrowserView
from plone import api
from tempfile import NamedTemporaryFile

import openpyxml

class ExcelGenericView(BrowserView):
    def sheet_info_factory(self):
        """Generator returning dicts with:
        - name: callable returning string
        - header: callable expecting view as parameter returning a list of strings (first row)
        - rows: callable expecting view as parameter returning an iterable with lists of data
        """
        raise NotImplemented("implement me")

    @property
    def fileprefix(self):
        return "export"

    @property
    def filename(self):
        return f"{self.fileprefix}-{self.now():%Y-%m-%d %H:%M}.xslx"

    def __call__(self):
        workbook = openpyxl.Workbook(write_only=True)
        workbook.iso_dates = True
        for sheet_info in self.sheet_info_factory():
            sheet = workbook.create_sheet(sheet_info["name"]())
            sheet.append(sheet_info["header"](self))
            for row in sheet_info["rows"](self):
                sheet.append(row)
        self.request.response.setHeader(
            "Content-Type",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.request.response.setHeader(
            "Content-Disposition", f"attachment;filename={self.filename}"
        )
        with NamedTemporaryFile() as tmp:
            workbook.save(tmp.name)
            tmp.seek(0)
            self.request.response.write(tmp.read())
```

## Example subclasses

Here is a simple example of a subclass for an export of items in a folder with title, description and type:

```python
class ExcelExportView(ExcelGenericView):
    def sheet_info_factory(self):
        yield {
            "name": lambda: f"Folder {self.context.id}",
            "header": lambda view: ["Title", "Description", "Type"]
            "rows": lambda view: (
                [brain.Title, brain.Description, brain.portal_type]
                for item in api.content.find(context=self.context, depth=1)
            ),
        }
```

Here is an example from a project:

```python
def kurs_header(view):
    return [
        "Nachname",
        "Vorname",
        "Titel (vor)",
        "Titel (nach)",
        "Strasse",
        "PLZ",
        "Ort",
        "Land",
        "E-Mail",
        "Geburtsdatum",
        "Newsletter",
        "Bezahlt",
        "Teilgenommen",
        "Prüfungsanmeldung",
        "Stripe Invoice Status",
        "Stripe Customer ID",
        "Stripe Invoice ID",
        "Stripe Invoice URL",
    ]


def kurs_rows(view):
    with api.env.adopt_roles(["Manager"]):
        for anmeldung_ref in api.relation.get(target=view.context, relationship="kurs"):
            anmeldung = anmeldung_ref.from_object
            tn = aq_parent(aq_inner(anmeldung))
            yield [
                tn.nachname,
                tn.vorname,
                tn.titel_vorn,
                tn.titel_hinten,
                tn.strasse,
                tn.plz,
                tn.ort,
                tn.land,
                anmeldung.email,
                tn.geburtsdatum.strftime("%d.%m.%Y"),
                "Ja" if anmeldung.newsletter else "Nein",
                (
                    "Bar"
                    if anmeldung.barzahlung
                    and anmeldung.stripe_status not in ("paid", "void")
                    else (
                        "Bezahlt"
                        if anmeldung.stripe_status == "paid"
                        else (
                            "Storniert"
                            if anmeldung.stripe_status == "void"
                            else "Unbezahlt"
                        )
                    )
                ),
                anmeldung.teilgenommen,
                "Ja" if anmeldung.pruefungsanmeldung else "Nein",
                anmeldung.stripe_status,
                tn.stripe_customer,
                anmeldung.stripe_invoice_number,
                anmeldung.stripe_hosted_invoice_url,
            ]


class ExcelKursExportView(ExcelGenericView):
    @property
    def fileprefix(self):
        basicadapter = IKursBasicBehavior(self.context)
        return f"kurs-{basicadapter.title.replace(' ', '')}"

    def sheet_info_factory(self):
        yield {
            "name": lambda: "Kursteilnehmer_innen",
            "header": kurs_header,
            "rows": kurs_rows,
        }
```

This can be implemented much more dynamic, as the header and rows can be constructed from the context and the view if needed. But you get the idea.

