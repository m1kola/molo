from django.test import TestCase
from molo.core.tests.base import MoloTestCaseMixin


class TestEffectiveStyleHints(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.new_section = self.mk_section(
            self.section_index,
            title="New Section",
            extra_style_hints='primary')

        self.new_section2 = self.mk_section(
            self.new_section, title="New Section 2")

        self.new_section3 = self.mk_section(
            self.section_index, title="New Section 3", slug="new-section-3")

        self.new_section4 = self.mk_section(
            self.new_section2, title="New Section 4", slug="new-section-4")

        self.new_section5 = self.mk_section(
            self.new_section,
            title="New Section 5", slug="new-section-5",
            extra_style_hints='secondary')

    def extra_css_set_on_current_section(self):
        self.assertEquals(
            self.new_section.get_effective_extra_style_hints(), 'primary')

    def extra_css_not_set_to_use_inherited_value(self):
        self.assertEquals(
            self.new_section2.get_effective_extra_style_hints(), 'primary')

    def extra_css_not_set_on_either_so_should_be_blank(self):
        self.assertEquals(
            self.new_section3.get_effective_extra_style_hints(), '')

        self.client.get('/locale/fr/')
        self.mk_section_translation(
            self.new_section3, self.french,
            title=self.new_section3.title + ' in french')

        response = self.client.get(
            '/sections/new-section-3-in-french/')
        self.assertContains(response, '<div class="articles nav ">')

        new_section6 = self.mk_section(
            self.new_section3,
            title="New Section 6", slug="new-section-6")

        self.mk_section_translation(
            new_section6, self.french, title=new_section6.title + ' in french')
        response = self.client.get(
            '/sections/new-section-3/new-section-6-in-french/')
        self.assertContains(response, '<div class="articles nav ">')

    def extra_css_not_set_on_child_so_should_use_parent_value(self):
        self.assertEquals(
            self.new_section4.get_effective_extra_style_hints(), 'primary')

    def extra_css_is_set_on_child_so_should_use_child_value(self):
        self.assertEquals(
            self.new_section5.get_effective_extra_style_hints(), 'secondary')

    def translated_page_so_should_use_main_lang_page_value(self):
        self.client.get('/locale/fr/')
        self.mk_section_translation(
            self.new_section4, self.french,
            title=self.new_section4.title + ' in french')

        response = self.client.get(
            '/sections/new-section/new-section-2/new-section-4-in-french/')
        self.assertContains(response, '<div class="articles nav primary">')

        new_section7 = self.mk_section(
            self.new_section3, title="New Section 7",
            slug="new-section-7", extra_style_hints='en-hint')
        self.mk_section_translation(
            new_section7, self.french, title=new_section7.title + ' in french')
        response = self.client.get(
            '/sections/new-section-3/new-section-7-in-french/')
        self.assertContains(response, '<div class="articles nav en-hint">')

    def translated_page_so_should_use_translated_page_value(self):
        self.client.get('/locale/fr/')
        self.mk_section_translation(
            self.new_section5, self.french,
            title=self.new_section5.title + ' in french',
            extra_style_hints='french-hint')
        response = self.client.get(
            '/sections/new-section/new-section-5-in-french/')
        self.assertContains(response, '<div class="articles nav french-hint">')
