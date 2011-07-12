from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implements

class IReadinessPortlet(IPortletDataProvider):
    """Readiness portlet
    """

class Assignment(base.Assignment):
    """Readiness portlet assignment
    """
    implements(IReadinessPortlet)

    title = u'Readiness Info'


class Renderer(base.Renderer):
    """Readiness portlet renderer
    """
    render = ViewPageTemplateFile('portlet_readiness.pt')
