from modeltranslation.translator import TranslationOptions, register

from common import models


@register(models.AboutUs)
class AboutUsTranslationOption(TranslationOptions):
    fields = ['title', 'description']