import argparse
import json
import logging

from aws_inventory import get_instances as get_aws_instances
from gcp_inventory import get_instances as get_gcp_instances


logging.basicConfig(
    filename="cloud-automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def check_instance(instance, provider):

    if provider == "aws":

        state = instance["State"]["Name"]

        if state == "running":
            return "HEALTHY"
        else:
            return "NOT HEALTHY"

    elif provider == "gcp":

        if instance.status == "RUNNING":
            return "HEALTHY"
        else:
            return "NOT HEALTHY"


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--provider",
        required=True,
        choices=["aws", "gcp"]
    )

    parser.add_argument(
        "--output",
        default="report.json"
    )

    args = parser.parse_args()

    logging.info(f"Inventory started: {args.provider}")

    try:

        if args.provider == "aws":
            instances = get_aws_instances()

        elif args.provider == "gcp":
            instances = get_gcp_instances()

    except Exception as error:

        logging.error(f"Inventory failed: {error}")

        print(f"Inventory failed: {error}")

        return 1

    report = []

    for item in instances:

        if args.provider == "aws":

            instance = item

            instance_id = instance["InstanceId"]
            private_ip = instance.get("PrivateIpAddress")
            state = instance["State"]["Name"]

            tags = instance.get("Tags", [])

            name = "Unknown"

            for tag in tags:

                if tag["Key"] == "Name":
                    name = tag["Value"]

            health = check_instance(instance, "aws")

        elif args.provider == "gcp":

            zone, instance = item

            name = instance.name
            instance_id = instance.id
            state = instance.status

            private_ip = "Unknown"

            for interface in instance.network_interfaces:
                private_ip = interface.network_i_p

            health = check_instance(instance, "gcp")

        report.append({
            "provider": args.provider,
            "name": name,
            "instance_id": str(instance_id),
            "private_ip": private_ip,
            "state": state,
            "health": health
        })

        logging.info(
            f"Instance checked: {name} | {health}"
        )

    with open(args.output, "w") as file:

        json.dump(
            report,
            file,
            indent=4
        )

    logging.info(f"Report created: {args.output}")
    logging.info("Inventory finished")

    print(
        f"{args.provider.upper()} report created: {args.output}"
    )

    return 0


if __name__ == "__main__":
    main()