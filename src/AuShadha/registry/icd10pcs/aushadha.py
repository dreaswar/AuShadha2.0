##########################################################################
# Create a Registration with the UI for a Role.
# Each module's aushadha.py is screened for this
#
# Each Class is registered for a Role in UI
# These can be used to generate Role based UI elements later.
#
# As of now string base role assignement is done.
# This can be later extended to class based role
##########################################################################

from .models import Section, BodySystem, Operation
from aushadha_ui.ui import ui as UI

UI.register('ProcedureCodes', Section)
UI.register('RegistryApp', Section)
UI.register('ReferenceApp', Section)
