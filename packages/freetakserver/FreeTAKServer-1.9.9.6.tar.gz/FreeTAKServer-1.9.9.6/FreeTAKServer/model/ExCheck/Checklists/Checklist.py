# pylint: disable=invalid-name
"""this module contains the Checklist class"""
from FreeTAKServer.model.ExCheck.Checklists.checklistDetails import checklistDetails  # pylint: disable=invalid-name
from FreeTAKServer.model.ExCheck.Checklists.checklistColumns import checklistColumns  # pylint: disable=invalid-name
from FreeTAKServer.model.ExCheck.Checklists.checklistTasks import checklistTasks  # pylint: disable=invalid-name


class Checklist:  # pylint: disable=too-few-public-methods
    """this model class contains only references
     to the children classes a it has no known attributes"""
    def __init__(self):
        self.checklistDetails = checklistDetails()
        self.checklistColumns = checklistColumns()
        self.checklistTasks = checklistTasks()
