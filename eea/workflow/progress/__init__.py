""" Progress bar
"""
from Products.DCWorkflow.States import StateDefinition

def extendState(context):
    """ State definition
    """
    options = StateDefinition.manage_options
    for option in options:
        if option['action'] == 'manage_progressbar':
            return
    StateDefinition.manage_options += (
        {'label': 'Progress Bar', 'action': 'manage_progressbar'},
    )

def initialize(context=None):
    """ Zope2 initialize
    """
    return extendState(context)
