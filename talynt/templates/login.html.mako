        <div class="login">
            <div id="login">
            % if message is not None:
                <p class="error">
                    ${message}
                </p>
            % endif
                <form method="POST" action="/login">
                    <input name="email" type="email" autofocus placeholder="email" required size=20/>
                    <input name="password" type="password" placeholder="password" required size=20 minlength=6/>
                    <input type="submit" value="login"/>
                </form>
                <p style="text-align:right">
                    <a onclick="show_create_account()" href="#">Create Account</a>
                </p>
            </div>
            <div id="create_account" style="display:none">
                <form method="POST" action="/create_account">
                    <input name="email" type="email" autofocus placeholder="email" required size=20/><br/>
                    <input oninput="validate_passwords()" id="password_1" name="password" type="password" placeholder="password" required size=20 minlength=6/><br/>
                    <input oninput="validate_passwords()" id="password_2" name="password_2" type="password" placeholder="verify password" required size=20 minlength=6/><br/>
                    <p style="text-align:right">
                        <input id="create" type="submit" value="create"/>
                    </p>
                </form>
                <p style="text-align:right">
                    <a onclick="show_login()" href="#">Already have an account</a>
                </p>
            </div>
        </div>
