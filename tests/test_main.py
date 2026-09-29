from main import check_instance


def test_aws_instance_healthy():

    instance = {
        "State": {
            "Name": "running"
        }
    }

    assert check_instance(instance, "aws") == "HEALTHY"


def test_aws_instance_not_healthy():

    instance = {
        "State": {
            "Name": "stopped"
        }
    }

    assert check_instance(instance, "aws") == "NOT HEALTHY"


def test_gcp_instance_healthy():

    class Instance:
        status = "RUNNING"

    instance = Instance()

    assert check_instance(instance, "gcp") == "HEALTHY"


def test_gcp_instance_not_healthy():

    class Instance:
        status = "TERMINATED"

    instance = Instance()

    assert check_instance(instance, "gcp") == "NOT HEALTHY"