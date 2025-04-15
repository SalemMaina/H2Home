from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Device, SensorData
import json

@api_view(['POST'])
def esp_data_receive(request):
    try:
        # Get data from ESP
        device_id = request.data.get('device_id')
        sensor_value = request.data.get('value')
        
        # Validate
        if not device_id or not sensor_value:
            return Response({"error": "Missing device_id or value"}, status=400)
        
        # Get or create device
        device, created = Device.objects.get_or_create(device_id=device_id)
        
        # Save sensor data
        SensorData.objects.create(device=device, value=sensor_value)
        
        # Prepare response
        response_data = {
            "status": "success",
            "device_id": device_id,
            "assigned_user": device.user.username if device.user else None,
            "message": "Data received successfully"
        }
        
        return Response(response_data)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def esp_data_send(request, device_id):
    try:
        # Get latest command for this device
        device = Device.objects.get(device_id=device_id)
        latest_command = device.commands.last()  # Assuming you have a Command model
        
        response_data = {
            "device_id": device_id,
            "command": latest_command.text if latest_command else None,
            "timestamp": latest_command.timestamp if latest_command else None
        }
        
        return Response(response_data)
    
    except Device.DoesNotExist:
        return Response({"error": "Device not registered"}, status=404)