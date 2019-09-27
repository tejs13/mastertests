from django.contrib import admin
from api.models.country import country
from api.models.company import company
from api.models.department import department
from api.models.district import district
from api.models.gate import gate
from api.models.service_category import service_category
from api.models.shift import shift
from api.models.state import state
from api.models.subarea import subarea
from api.models.skill import skill
from api.models.Audit_trails import Audit
from api.models.composite import composite
from api.models.ui_demo import ui_demo


admin.site.register(country)
admin.site.register(company)
admin.site.register(department)
admin.site.register(district)
admin.site.register(gate)
admin.site.register(service_category)
admin.site.register(shift)
admin.site.register(state)
admin.site.register(subarea)
admin.site.register(skill)
admin.site.register(Audit)
admin.site.register(composite)
admin.site.register(ui_demo)

