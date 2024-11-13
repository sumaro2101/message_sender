from django.http import Http404
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from pytils.translit import slugify

from datetime import datetime, timezone

from mess.models import MessageInfo
from mail_center.services import (check_message,
                                  _unique_name_task,
                                  _convert_unique_name_to_id,
                                  )


class TestValidators(TestCase):

    def setUp(self):
        user = (get_user_model().objects
                .create(username='root',
                        email='root@gmail.com',
                        ))
        title = 'Test'
        MessageInfo.objects.create(
            employee=user,
            title_message=title,
            text_message='This is test',
            slug=f'{slugify(user.pk)}-{slugify(title)}',
            time_create=datetime.now(timezone.utc),
            time_edit=datetime.now(timezone.utc),
            actual=True,
            )

    def test_mess_exists(self):
        mess = MessageInfo.objects.all()
        self.assertTrue(mess.exists())

    def test_check_message(self):
        mess = MessageInfo.objects.first()
        check = check_message(MessageInfo, mess.slug)
        self.assertIsInstance(check, MessageInfo)

    def test_check_message_fail(self):
        with self.assertRaises(TypeError):
            check_message(MessageInfo, 200)

    def test_check_message_fail2(self):
        with self.assertRaises(Http404):
            check_message(MessageInfo, '2-not-test')

    def test_check_message_fail3(self):
        mess = MessageInfo.objects.first()
        mess.actual = False
        mess.save()
        with self.assertRaises(PermissionDenied):
            check_message(MessageInfo, mess.slug)

    def test_check_unique_render(self):
        unique = _unique_name_task(MessageInfo.objects.first())
        self.assertEqual('mess.messageinfo_9', unique)

    def test_check_unique_fail(self):
        with self.assertRaises(TypeError):
            _unique_name_task(200)

    def test_check_unique_convert(self):
        unique = _convert_unique_name_to_id('mess.messageinfo_2')
        self.assertEqual('2', unique)

    def test_check_unique_convert_fail(self):
        with self.assertRaises(TypeError):
            _convert_unique_name_to_id(200)

    def test_check_unique_convert_fail2(self):
        with self.assertRaises(ValueError):
            _convert_unique_name_to_id('dff.ffds_')
