from xonsh.built_ins import XonshSession


def _load_xontrib_(xsh: XonshSession, **_):
    aliases['assume'] = _assume

def _assume(args):
    AWS_VARIABLE_NAMES = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        "AWS_PROFILE",
        "AWS_REGION",
        "AWS_SESSION_EXPIRATION"
    ]

    $GRANTED_ALIAS_CONFIGURED = "true"

    $GRANTED_OUTPUT = $(assumego @(args))

    granted_flag, *aws_variable_values = $GRANTED_OUTPUT.strip('\n').split(' ')

    if granted_flag == "GrantedOutput":
        # Remove the first line of output
        granted_output = '\n'.join($GRANTED_OUTPUT.split('\n')[1:])
        print(granted_output)
        exit()

    for aws_variable_name, aws_variable_value in zip(AWS_VARIABLE_NAMES, aws_variable_values):
        if granted_flag == "GrantedDesume" or aws_variable_value == "None":
            ${...}.pop(aws_variable_name, None)
            continue
        if granted_flag == "GrantedAssume":
            ${...}[aws_variable_name] = aws_variable_value

    if granted_flag == "GrantedOutput":
        for aws_variable_name, aws_variable_value in zip(AWS_VARIABLE_NAMES, aws_variable_values):
            if aws_variable_value == "None":
                ${...}.pop(aws_variable_name, None)
                continue
            ${...}[aws_variable_name] = aws_variable_value

    del $GRANTED_ALIAS_CONFIGURED
