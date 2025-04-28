import os
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from ..tasks.taskregistry import TASK_REGISTRY


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_run_task(request, task_name):

    inputs = {}
    for k in request.data['inputs'].keys():
        input_dir = request.data['inputs'][k]
        inputs[k] = []
        for f in os.listdir(input_dir):
            inputs[k].append(os.path.join(input_dir, f))
    print(json.dumps(inputs, indent=4))

    outputs = {}
    for k in request.data['outputs'].keys():
        output_dir = request.data['outputs'][k]
        outputs[k] = output_dir
    print(json.dumps(outputs, indent=4))

    params = {}
    for k in request.data['params'].keys():
        value = request.data['params'][k]
        params[k] = value
    print(json.dumps(params, indent=4))

    task = TASK_REGISTRY[task_name]['class'](
        inputs=inputs,
        outputs=outputs,
        params=params,
        notify_finished_callback=False,
    )

    task.execute()

    return Response({'message': 'OK'}, status=201)