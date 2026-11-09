"""Los borradores se guardan por usuario: la página debe identificar a quien escribe."""
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_la_pagina_identifica_al_usuario_para_sus_borradores(client, bombero):
    client.force_login(bombero)
    pagina = client.get(reverse("revisiones:mis_revisiones")).content.decode()
    assert f'data-usuario="{bombero.pk}"' in pagina


def test_sin_sesion_no_se_guardan_borradores(client):
    assert "data-usuario" not in client.get(reverse("accesos:login")).content.decode()
