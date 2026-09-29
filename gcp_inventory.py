from google.cloud import compute_v1


def get_instances():

    client = compute_v1.InstancesClient()

    request = compute_v1.AggregatedListInstancesRequest(
        project="project-aed44365-ff0a-48b4-b75"
    )

    response = client.aggregated_list(request=request)

    instances = []

    for zone, scoped_list in response:

        if scoped_list.instances:

            for instance in scoped_list.instances:
                instances.append((zone, instance))

    return instances