import json
from django.http import JsonResponse
from django.views import View
from django.utils.dateparse import parse_datetime
from .models import Robot

class RobotCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            model = body.get("model")
            version = body.get("version")
            created = body.get("created")

            if not model or not version or not created:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if not model.isalnum() or len(model) != 2:
                return JsonResponse({"error": "Invalid model format"}, status=400)

            if not version.isalnum() or len(version) != 2:
                return JsonResponse({"error": "Invalid version format"}, status=400)

            if not Robot.objects.filter(model=model).exists():
                return JsonResponse({"error": "Model does not exist in the system"}, status=400)

            try:
                created_date = parse_datetime(created)
                if not created_date:
                    raise ValueError
            except ValueError:
                return JsonResponse({"error": "Invalid created format"}, status=400)

            serial = f"{model}-{version}"

            robot = Robot.objects.create(
                serial=serial,
                model=model,
                version=version,
                created=created_date,
            )
            return JsonResponse(
                {
                    "serial": robot.serial,
                    "model": robot.model,
                    "version": robot.version,
                    "created": robot.created.isoformat(),
                },
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
