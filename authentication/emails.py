def get_register_confirmation_email(username, confirmation_link):
    return """
<h1>Thanks {} to register to APP_NAME</h1>
<p>Please click on link below to confirm you registration</p>
<a href="{}">Confirm email</a>
""".format(
        username, confirmation_link
    )
