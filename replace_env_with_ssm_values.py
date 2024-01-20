import sys
import boto3
import re

region = "<?aws-region>"
ssm_client = boto3.client("ssm", region_name=region)


def get_ssm_parameter(parameter_name):
    response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    if response is not None:
        return response["Parameter"]["Value"]
    raise NameError(f"Ssm Parameter with name {parameter_name} is not found.")


def replace_placeholders(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    placeholders_pattern = r"\{\{resolve:ssm:(.*?)\}\}"
    placeholders_to_replace = re.findall(placeholders_pattern, content)

    modified_content = content

    for matched_patterns in placeholders_to_replace:
        parameter_name = matched_patterns.strip()
        parameter_value = get_ssm_parameter(parameter_name=parameter_name)
        modified_content = modified_content.replace(
            f"{{{{resolve:ssm:{parameter_name}}}}}", parameter_value
        )

    with open(file_path, "w") as file:
        file.write(modified_content)

    return "Parameters successfully replaced!"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage python main.py <file_path>")
    else:
        env_file_path = sys.argv[1]
        print(replace_placeholders(env_file_path))
