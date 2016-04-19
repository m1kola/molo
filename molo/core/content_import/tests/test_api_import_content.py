import mock
import pytest

from elasticgit.tests.base import ModelBaseTest

from molo.core.models import SiteLanguage, SectionPage, ArticlePage, FooterPage
from molo.core.tests.base import MoloTestCaseMixin
from molo.core.content_import.tests.base import ElasticGitTestMixin
from molo.core.content_import.errors import ImportError
from molo.core.content_import.api import Repo
from molo.core.content_import import api

from unicore.content import models as eg_models

from wagtail.wagtailimages.tests.utils import get_test_image_file


@pytest.mark.django_db
class TestImportContent(
        ModelBaseTest, MoloTestCaseMixin, ElasticGitTestMixin):

    def setUp(self):
        self.english = SiteLanguage.objects.create(
            locale='en',
        )
        self.spanish = SiteLanguage.objects.create(
            locale='es',
        )
        self.mk_main()

        self.repo1 = Repo(self.create_workspace(), 'repo1', 'Repo 1')
        self.ws1 = self.repo1.workspace

    def test_import_sections_for_primary_language(self):
        lang1 = eg_models.Localisation({'locale': 'eng_GB'})
        lang2 = eg_models.Localisation({'locale': 'spa_ES'})

        self.ws1.save(lang1, 'Added english language')
        self.ws1.save(lang2, 'Added french language')

        [cat_eng_1, cat_eng_2] = self.create_categories(
            self.ws1, locale='eng_GB', count=2)
        [cat_spa_1, cat_spa_2] = self.create_categories(
            self.ws1, locale='spa_ES', count=2)

        # section with invalid source
        self.create_categories(
            self.ws1, locale='spa_ES', source='an-invalid-uuid', count=1)
        # section with no source
        self.create_categories(
            self.ws1, locale='spa_ES', source=None, count=1)

        self.ws1.save(cat_spa_1.update({
            'source': cat_eng_1.uuid,
            'position': 4,
        }), 'Added source to category.')
        self.ws1.save(cat_spa_2.update({
            'source': cat_eng_2.uuid,
            'position': 4,
        }), 'Added source to category.')

        en_pages1 = self.create_pages(
            self.ws1, count=10, locale='eng_GB',
            primary_category=cat_eng_1.uuid)

        en_pages2 = self.create_pages(
            self.ws1, count=10, locale='eng_GB',
            primary_category=cat_eng_2.uuid)

        # main language page with invalid primary category
        self.create_pages(
            self.ws1, count=1, locale='eng_GB',
            primary_category='an-invalid-uuid')

        en_footer_pages = self.create_pages(
            self.ws1, count=2, locale='eng_GB',
            primary_category=None)

        es_pages1 = self.create_pages(
            self.ws1, count=10, locale='spa_ES',
            primary_category=cat_eng_1.uuid)

        es_pages2 = self.create_pages(
            self.ws1, count=10, locale='spa_ES',
            primary_category=cat_eng_2.uuid)

        es_footer_pages = self.create_pages(
            self.ws1, count=2, locale='spa_ES',
            primary_category=None)

        # translation page without a source and primary category
        self.create_pages(
            self.ws1, count=1, locale='spa_ES',
            primary_category=None)

        # page with linked page
        [page_en] = self.create_pages(
            self.ws1, count=1, locale='eng_GB',
            primary_category=cat_eng_1.uuid)
        [page_with_linked_page] = self.create_pages(
            self.ws1, count=1, locale='eng_GB',
            linked_pages=[page_en.uuid], primary_category=cat_eng_1.uuid)

        for i in range(0, 10):
            self.ws1.save(es_pages1[i].update({
                'source': en_pages1[i].uuid,
                'author_tags': ['love'],
            }), 'Added author_tags and source to page.')

            self.ws1.save(es_pages2[i].update({
                'source': en_pages2[i].uuid,
            }), 'Added source to page.')

        for i in range(0, 2):
            self.ws1.save(es_footer_pages[i].update({
                'source': en_footer_pages[i].uuid,
            }), 'Added source to page.')

        self.assertEquals(
            self.ws1.S(eg_models.Category).all().count(), 6)

        self.assertEquals(
            self.ws1.S(eg_models.Page).all().count(), 48)
        self.assertEquals(
            self.ws1.S(eg_models.Localisation).all().count(), 2)

        self.assertEquals(SectionPage.objects.all().count(), 0)
        self.assertEquals(ArticlePage.objects.all().count(), 0)

        api.import_content([self.repo1], [
            {'locale': 'eng_GB', 'site_language': 'en', 'is_main': True},
            {'locale': 'spa_ES', 'site_language': 'es', 'is_main': False}])

        self.assertEquals(SectionPage.objects.all().count(), 4)
        self.assertEquals(ArticlePage.objects.all().count(), 46)
        self.assertEquals(
            ArticlePage.objects.filter(metadata_tags__name='love').count(), 10)

        page = ArticlePage.objects.get(uuid=page_with_linked_page.uuid)
        linked_page = ArticlePage.objects.get(uuid=page_en.uuid)
        self.assertEquals(page.body.stream_data[2],
                          {u'type': u'page', u'value': linked_page.pk})

        # run import twice
        api.import_content([self.repo1], [
            {'locale': 'eng_GB', 'site_language': 'en', 'is_main': True},
            {'locale': 'spa_ES', 'site_language': 'es', 'is_main': False}])

        self.assertEquals(SectionPage.objects.all().count(), 4)
        self.assertEquals(ArticlePage.objects.all().count(), 46)
        self.assertEquals(FooterPage.objects.all().count(), 4)

        # check that the main language no longer
        # needs to be first in the list of locales
        api.import_content([self.repo1], [
            {'locale': 'eng_GB', 'site_language': 'en', 'is_main': False},
            {'locale': 'spa_ES', 'site_language': 'es', 'is_main': True}])
        self.assertEquals(str(SiteLanguage.objects.filter(
            is_main_language=True).first()), 'English')
        self.assertEquals(str(SiteLanguage.objects.filter(
            is_main_language=False).first()), 'Spanish')

        # check that an ImportError is raised if
        # locales has more than one language with is_main == True
        error_occured = False
        try:
            api.import_content([self.repo1], [
                {'locale': 'eng_GB', 'site_language': 'en', 'is_main': True},
                {'locale': 'spa_ES', 'site_language': 'es', 'is_main': True}])
        except ImportError:
            error_occured = True
        self.assertTrue(error_occured)

        # check that an ImportError is raised
        # if none of the locales have is_main == True
        error_occured = False
        try:
            api.import_content([self.repo1], [
                {'locale': 'eng_GB', 'site_language': 'en', 'is_main': False},
                {'locale': 'spa_ES', 'site_language': 'es', 'is_main': False}])
        except ImportError:
            error_occured = True

        self.assertTrue(error_occured)

    @mock.patch(
        'molo.core.content_import.helpers.get_image.get_thumbor_image_file')
    def test_image_import(self, mock_get_thumbor_image_file):
        mock_get_thumbor_image_file.return_value = get_test_image_file()

        lang1 = eg_models.Localisation({'locale': 'eng_GB'})
        self.ws1.save(lang1, 'Added english language')

        [cat_eng] = self.create_categories(
            self.ws1, locale='eng_GB', count=1)

        [en_page] = self.create_pages(
            self.ws1, count=1, locale='eng_GB',
            primary_category=cat_eng.uuid,
            image_host='http://thumbor', image='some-uuid-for-the-image')

        api.import_content([self.repo1], [
            {'locale': 'eng_GB', 'site_language': 'en', 'is_main': True}])

        self.assertEquals(ArticlePage.objects.all().count(), 1)
        self.assertEquals(
            ArticlePage.objects.all().first().image.title,
            'some-uuid-for-the-image')
