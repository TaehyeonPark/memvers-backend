def error_template(error_code: int, title: str, desc: str, redirect_url: str, redirect_desc: str) -> str:
    f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
        <title>admin.memvers</title>
        <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i&amp;display=swap">
    </head>

    <body>
        <div class="text-center mt-5">
            <div class="error mx-auto" data-text="{error_code}">
                <p class="m-0">{error_code}</p>
            </div>
            <p class="text-dark mb-5 lead">{title}</p>
            <p class="text-black-50 mb-0">{desc}</p><a href="{redirect_url}">{redirect_desc}</a>
        </div>
        <script src="assets/bootstrap/js/bootstrap.min.js"></script>
        <script src="assets/js/bs-init.js"></script>
        <script src="assets/js/hashlib.js"></script>
        <script src="assets/js/login.js"></script>
        <script src="assets/js/register.js"></script>
        <script src="assets/js/search.js"></script>
        <script src="assets/js/theme.js"></script>
        <script src="assets/js/validate.js"></script>
    </body>
</html>"""