from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def home(request):
    return render(request, 'reel/home.html')

@api_view(['POST'])
def download_reel_api(request):
    reel_url = request.data.get('url')  # Use JSON data for API requests
    if not reel_url:
        return Response({'error': 'No URL provided.'}, status=400)

    try:
        # Placeholder for downloading the video
        video_data = requests.get(reel_url)

        if video_data.status_code == 200:
            # Respond with a success message
            return Response({'message': 'Reel downloaded successfully!', 'url': reel_url})
        else:
            return Response({'error': 'Failed to fetch video.'}, status=500)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def download_reel(request):
    if request.method == 'POST':
        reel_url = request.POST.get('url')  # Retrieve the URL from the form
        if not reel_url:
            return JsonResponse({'error': 'No URL provided.'})

        try:
            # Attempt to download the video (this is placeholder logic)
            video_data = requests.get(reel_url)  # Replace with real reel downloading logic

            # Check if the request was successful
            if video_data.status_code == 200:
                # Respond with the video file as a download
                response = HttpResponse(video_data.content, content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="reel.mp4"'
                return response
            else:
                return JsonResponse({'error': 'Failed to fetch video. Invalid response from server.'})
        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method. Use POST instead.'})

