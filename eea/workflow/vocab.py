from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

class ReasonsVocabulary(object):
    """ Reasons vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
	items = []
	items.append(SimpleTerm(
	    value='Content is outdated',
	    token='Content is outdated',
	    title='Content is outdated'))
	items.append(SimpleTerm(
	    value='No more updates will be done',
	    token='No more updates will be done',
	    title='No more updates will be done'))
	items.append(SimpleTerm(
	    value='Data sources and references are not verifiable',
	    token='Data sources and references are not verifiable',
	    title='Data sources and references are not verifiable'))

	return SimpleVocabulary(items)

ReasonsVocabularyFactory = ReasonsVocabulary()

