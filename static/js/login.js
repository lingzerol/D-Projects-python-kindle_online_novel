var password_index = 0
var password = new Array([0, 0, 0, 0, 0, 0])
var public_key = "-----BEGIN PUBLIC KEY-----\n" +
    "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDCyWusGPvfFn9aMSvxxmO86Wyl\n" +
    "e0x6BJ4ctwUVKh+2wx0s7OY+dB279E1lORmhK3hOS34XRMIYcRsPZXpnALSe0iqP\n" +
    "zU++6FXUSP0NZDsiKofmbTjU3AxeIALEb4r8B1Ujhtss4PN41WIq3z1WsiO+w4nI\n" +
    "1oZaxlVOSUup0he5mQIDAQAB\n" +
    "-----END PUBLIC KEY-----\n"
function encrypt(str) {
    let jse = new JSEncrypt();
    jse.setPublicKey(public_key);
    var result = jse.encrypt(str);
    return result
}
function change_password_point(index, empty) {
    if (empty)
        button_color = "white"
    else
        button_color = "black"
    document.getElementById(index.toString() + "_password").style.backgroundColor = button_color
}
function click_button(button) {
    if (button == 11) {
        password_index = Math.max(0, password_index - 1)
        change_password_point(password_index, true)
        password[password_index] = 0
    }
    else if (button == 10) {
        for (var i = 0; i < password_index; i++) {
            change_password_point(i, true)
            password[i] = 0
        }
        password_index = 0
    }
    else {
        if (password_index >= 6) {
            return
        }
        change_password_point(password_index, false)
        password[password_index] = button
        password_index += 1
    }
    if (password_index >= 6) {
        ps = ""
        for (var i = 0; i < password.length; i++) {
            ps += password[i].toString()
        }
        var send_password = encrypt(ps)
        login(send_password)
    }
}
function login(password) {
    $.ajax({
        url: "login",
        type: "POST",
        data: { "password": password },
        success: function (result) {
            if (result.message == "success!") {
                document.getElementById("tips").innerText = "Password pass."
                document.cookie = result.cookie
                window.location.href="index"
            }
            else {
                document.getElementById("tips").innerText = "Please re-enter the password!"
            }
        }
    });
}