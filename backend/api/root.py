from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response(
        {
            "Get All Courses": reverse(
                "get_all_courses",  request=request, format=format

            ),
            "Submit Selection": reverse(
                "submit_selection", request=request, format=format

            ),
        }
    )