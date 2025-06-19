import io
import re

import six

from .commands import call_command


def get_current_branch():
    return call_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def retrieve_branch_type(branch, regex):
    matches = re.match(regex, branch)
    if matches:
        branch_type = matches.group("branch_type")
        return branch_type


def is_branch_type_in_message(contents, branch_type):
    for line in contents.splitlines():
        stripped = line.strip().lower()

        if stripped == "" or stripped.startswith("#"):
            continue

        if branch_type.lower() in stripped:
            return True


def add_branch_type(filename, regex, format_template):
    branch = get_current_branch()
    branch_type = retrieve_branch_type(branch, regex)

    if branch_type:
        with io.open(filename, "r+") as fd:
            contents = fd.read()

            if (
                is_branch_type_in_message(contents, branch_type)
                or not contents[:contents.find("\n")]
            ):
                return

            branch_type_msg = format_template.format(message=contents, branch_type=branch_type)
            fd.seek(0)
            fd.write(six.text_type(branch_type_msg))
            fd.truncate()
