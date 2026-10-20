from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

DATA = {'username': 'jugador1', 'email': 'a@b.com', 'password1': 'Clave$egura2026', 'password2': 'Clave$egura2026'}
FAKE = {'results': [{'name': 'Zelda', 'background_image': None, 'released': '2023-05-12', 'rating': 4.6, 'genres': [{'name': 'Aventura'}]}]}


class RegisterTests(TestCase):
    def test_registro_valido_cifra_la_contrasena(self):
        r = self.client.post(reverse('register'), DATA)
        self.assertRedirects(r, reverse('login'))
        self.assertTrue(User.objects.get(username='jugador1').password.startswith('pbkdf2_'))

    def test_contrasena_debil_o_distinta_se_rechaza(self):
        self.assertEqual(User.objects.count(), 0)
        for bad in ({'password1': '12345678', 'password2': '12345678'}, {'password2': 'otra'}):
            r = self.client.post(reverse('register'), {**DATA, **bad})
            self.assertEqual(r.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_correo_duplicado_o_invalido(self):
        self.client.post(reverse('register'), DATA)
        r = self.client.post(reverse('register'), {**DATA, 'username': 'otro'})
        self.assertContains(r, 'Ya existe una cuenta con ese correo')
        r = self.client.post(reverse('register'), {**DATA, 'username': 'x2', 'email': 'no-es-correo'})
        self.assertEqual(User.objects.count(), 1)


class GamesTests(TestCase):
    def setUp(self):
        User.objects.create_user('ana', 'ana@x.com', 'Clave$egura2026')

    def test_requiere_login(self):
        r = self.client.get(reverse('games'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('/login/', r.url)

    @override_settings(RAWG_API_KEY='clave-de-prueba')
    @patch('core.services.requests.get')
    def test_muestra_juegos_de_la_api(self, get):
        get.return_value.json.return_value = FAKE
        get.return_value.raise_for_status.return_value = None
        self.client.login(username='ana', password='Clave$egura2026')
        r = self.client.get(reverse('games') + '?q=zelda-test')
        self.assertContains(r, 'Zelda')

    @override_settings(RAWG_API_KEY='')
    def test_sin_clave_muestra_aviso(self):
        self.client.login(username='ana', password='Clave$egura2026')
        self.assertContains(self.client.get(reverse('games')), 'RAWG_API_KEY')

    def test_paginas_publicas(self):
        for name in ('home', 'register', 'login'):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
