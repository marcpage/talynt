<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Job Description Assistant</title>
        <style>
            <%include file="styles.css"/>
        </style>
        <script>
            <%include file="scripts.js"/>
        </script>
    </head>
    <body>
        <h1>Job Description Assistant</h1>
        % if user_id is None:
            <%include file="login.html.mako"/>
        % else:
            <%include file="logout.html.mako"/>
        % endif
    </body>
</html>
