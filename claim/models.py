# -*- coding: utf-8 -*-
import datetime
import json

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class OrganizationType(models.Model):
    # TODO(vegasq) should we use AMENITY as keys here?
    ORG_TYPES = (
        ("0", _("Unknown")),
        ("1", _("Міністерство фінансів України")),
        ("2", _("Міністерство соціальної політики України")),
        ("3", _("Міністерство регіонального розвитку, "
                "будівництва та житлово-комунального господарства України")),
        ("4", _("Міністерство охорони здоров'я України ")),
        ("5", _("Міністерство освіти і науки України")),
        ("6", _("Міністерство оборони України")),
        ("7", _("Міністерство молоді та спорту України")),
        ("8", _("Міністерство культури України")),
        ("9", _("Міністерство інфраструктури України")),
        ("10", _("Міністерство інформаційної політики України")),
        ("11", _("Міністерство закордонних справ України")),
        ("12", _("Міністерство енергетики та вугільної промисловості "
                 "України")),
        ("13", _("Міністерство економічного розвитку і торгівлі України")),
        ("14", _("Міністерство екології та природних ресурсів України")),
        ("15", _("Міністерство внутрішніх справ України")),
        ("16", _("Міністерство аграрної політики та продовольства України")),
        ("17", _("Міністерство юстиції України")),
    )

    org_type = models.CharField(choices=ORG_TYPES,
                                max_length=10,
                                default=ORG_TYPES[0][0],
                                unique=True)

    def __str__(self):
        for org_type in self.ORG_TYPES:
            if org_type[0] == str(self.org_type):
                return org_type[1]


class Organization(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    org_type = models.ForeignKey(OrganizationType, null=True)

    @property
    def total_claims(self):
        return self.claim_set.all().count()

    def json_claims(self):
        claims = self.claim_set.all()

        claims_list = []

        if claims:
            for claim in claims:
                username = claim.complainer.username if\
                    claim.complainer else _("Anon")
                claims_list.append({
                    'organization_id': self.id,
                    'organization_name': self.name,
                    'text': claim.text,
                    'servant': claim.servant,
                    'complainer': username
                })

        return json.dumps(claims_list)

    def __str__(self):
        return self.name


class InCharge(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    organizations = models.ManyToManyField(Organization)
    organization_types = models.ManyToManyField(OrganizationType)

    def __str__(self):
        return self.name


class Claim(models.Model):
    text = models.CharField(max_length=2550)
    created = models.DateTimeField(default=datetime.datetime.now)
    live = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization)
    # polygon_id = models.CharField(max_length=250)
    servant = models.CharField(max_length=550)
    complainer = models.ForeignKey(User, null=True, blank=True, default=None)
