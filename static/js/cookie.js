function check_cookie() {
    $.ajax({
        url: "cookie",
        type: "POST",
        data: {  },
        success: function (result) {
            if (result.message == "fail!") {
                window.location.href = "/"
            }
        }
    });
}