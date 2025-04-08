from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json, os
from home.response_processing_new import OptimizerResultProcessor


# Create your views here.
def index(request):
    """
    Renders the home page.

    Parameters:
    ----------
    request : HttpRequest
        The request object used to generate this response.

    Returns:
    -------
    HttpResponse
        The rendered home page.
    """
    return render(request, "home/index.html")


# post request from frontend
@csrf_exempt  # Only use for testing; use CSRF protection in production!
def process_scenario(request):
    """
    Processes the scenario based on the provided ID and filetype.

    Parameters:
    ----------
    request : HttpRequest
        The request object containing the scenario ID and filetype.

    Returns:
    -------
    JsonResponse or HttpResponse
        The JSON data or image file based on the filetype, or an error message.
    """
    if request.method == "GET":
        try:
            # request holds ID for scenario selection
            id = request.GET.get("id")
            filetype = request.GET.get("filetype")
            print(id, filetype)

            if not id:
                return JsonResponse({"error": "Missing 'id' parameter"}, status=400)

            if not filetype:
                return JsonResponse(
                    {"error": "Missing 'filetype' parameter"}, status=400
                )

            # Define the folder path relative to the current working directory
            folder_path = f"scenario/scenario{id}"

            if filetype == "json":
                graph_path = f"{folder_path}/graph.json"  # path for graph.json
                if not os.path.exists(graph_path):
                    return JsonResponse({"error": "Graph file not found"}, status=404)

                with open(
                    graph_path, "r"
                ) as graph:  # open the file so that it can be read
                    data = json.load(
                        graph
                    )  # deserializes opened json file to actual data that can be sent as a JsonResponse
                    return JsonResponse(data, status=200)

            if filetype == "png":
                img_path = f"{folder_path}/img.png"  # path for img.png
                if not os.path.exists(img_path):
                    return JsonResponse({"error": "Image file not found"}, status=404)

                with open(img_path, "rb") as img:
                    response = HttpResponse(
                        img.read(), content_type="image/png"
                    )  # Creates HTTPResponse with the binary data of the image
                    response["Content-Disposition"] = (
                        "attachment; filename=img.png"  # tells the frontend that the file should be treated as a download and not displayed
                    )
                    return response
            else:
                return JsonResponse(
                    {"error": "Invalid 'filetype' parameter. Use 'json' or 'png'."},
                    status=400,
                )

        except Exception as e:
            return JsonResponse(
                {f"error when trying to open and process data: {e}"}, status=500
            )
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def save_slider_data(request):
    """
    Saves the slider data sent from the frontend.

    Parameters:
    ----------
    request : HttpRequest
        The request object containing the slider data.

    Returns:
    -------
    JsonResponse
        The result of processing the slider data, or an error message.
    """
    if request.method == "POST":
        print("Request received:", request.body)
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            # Directly pass the data to process_response() instead of saving and then retrieving
            #result = process_response(data) #old implementation
            result = OptimizerResultProcessor(data).process_response()

            return JsonResponse(result, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
