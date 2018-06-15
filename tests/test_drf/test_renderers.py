from django.urls import reverse
from rest_framework.test import APIClient
from tablib import Dataset

import pytest

from demo.factories import DemoModelFactory, UserFactory


@pytest.mark.django_db
def test_friendly_renderer():
    user = UserFactory(is_superuser=True)
    DemoModelFactory(boolean_field=True)
    DemoModelFactory(boolean_field=False)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('sample:list') + '?format=csv')

    dataset = Dataset().load(response.content.decode('utf-8'), 'csv')
    assert len(dataset._get_headers()) == 6
    assert dataset[0] == ('Yes', '', '1', 'Random', '', '')
    assert dataset[1] == ('', '', '2', 'Random', '', '')
