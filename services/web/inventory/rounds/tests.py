import json
from unittest.mock import patch

from django.core import serializers
from django.core.exceptions import ValidationError
from django.test import TestCase
from wrf_standard.models import WRFStandardEmission

from .models import WRFRound


class WRFRoundManagerTests(TestCase):
    def setUp(self):
        self.emission = WRFStandardEmission.objects.create(
            fuel="Gasoline", fraction=0.3, mileage=2000, subcategory="A"
        )

    @patch("rounds.models.django_rq.get_queue")
    def test_send_to_queue_enqueues_job(self, mock_get_queue):
        mock_queue = mock_get_queue.return_value

        WRFRound.queue.send_to_queue(self.emission)

        emission_data = serializers.serialize("json", (self.emission,))[1:-1]

        mock_queue.enqueue.assert_called_once_with(
            "app.tasks.process_emission", emission_data
        )

    @patch("rounds.models.django_rq.get_queue")
    def test_send_to_queue_withe_valid_fields(self, mock_get_queue):
        mock_queue = mock_get_queue.return_value

        WRFRound.queue.send_to_queue(self.emission)

        args, _ = mock_queue.enqueue.call_args

        # Dados enviados
        queued_emission_data = args[1]
        data = json.loads(queued_emission_data)

        # Verifica se o JSON contém o modelo correto e o pk
        self.assertEqual(data["pk"], self.emission.pk)
        self.assertIn("model", data)
        self.assertIn("fields", data)

    @patch("rounds.models.django_rq.get_queue")
    def test_send_to_queue_invalid_emission(self, mock_get_queue):
        invalid_emission = WRFStandardEmission(fraction=0.5)

        with self.assertRaises(ValidationError):
            invalid_emission.full_clean()  # força validação do Django

        # Certifica que enqueue não é chamado
        mock_queue = mock_get_queue.return_value
        if invalid_emission.pk:  # só se tivesse sido salvo
            WRFRound.queue.send_to_queue(invalid_emission)
            mock_queue.enqueue.assert_not_called()
