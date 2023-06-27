function change_visibility(div, show) {
    div.style.display = show ? "block" : "none";
}

function show_create_account() {
    var login = document.getElementById("login");
    var create = document.getElementById("create_account");

    change_visibility(login, false);
    change_visibility(create, true);
}

function show_login() {
    var login = document.getElementById("login");
    var create = document.getElementById("create_account");

    change_visibility(login, true);
    change_visibility(create, false);
}

function has_whitespace(s) {
    return /\s/g.test(s);
}

function has_lowercase(s) {
    return /[a-z]/g.test(s);
}

function has_uppercase(s) {
    return /[A-Z]/g.test(s);
}

function has_numbers(s) {
    return /[0-9]/g.test(s);
}

function has_special(s) {
    return /[!@#$%^&*()_+={}[\]:;"'<>,./?-]/g.test(s);
}

function password_valid(password_text) {
    return (password_text.length >= 16) ||
            has_lowercase(password_text)
            && has_uppercase(password_text)
            && has_numbers(password_text)
            && has_special(password_text)
            && (password_text.length >= 6)
}

function validate_passwords() {
    var p1 = document.getElementById("password_1");
    var p2 = document.getElementById("password_2");
    var create = document.getElementById("create");
    var valid = false;
    var p1_color = "white";
    var p2_color = "white";

    if (!password_valid(p1.value)) {
        p1_color = "#FFEEEE";
    } else if (p1.value != p2.value) {
        p1_color = "#EEFFEE";
        p2_color = "#FFEEEE";
    } else {
        p1_color = "#EEFFEE";
        p2_color = "#EEFFEE";
        valid = true;
    }
    p1.style.backgroundColor = p1_color;
    p2.style.backgroundColor = p2_color;
    create.disabled = !valid;
}
