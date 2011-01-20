from Products.CMFCore import DirectoryView
from zope.i18nmessageid import MessageFactory
from eea.workflow.config import *

PortletReadinessMessageFactory = MessageFactory('eea.workflow')

#hack to register the skins path
from Products.CMFCore import utils
from Globals import package_home
from os.path import dirname
ppath = utils.ProductsPath
utils.ProductsPath.append(dirname(package_home(product_globals)))
DirectoryView.registerDirectory('skins', product_globals)
utils.ProductsPath = ppath
#endhack


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


import patches  #install patches
patches         #pyflakes warning
