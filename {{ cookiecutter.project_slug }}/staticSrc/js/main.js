var app = (function(o, $) {

    const self = this;

    o.main = {

        onHcaptchaSubmit: function onHcaptchaSubmit(token) {
            document.getElementById("id_captcha_response").value = token;
            document.querySelector("form").submit();
        },

        getCookie: function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },

        temporaryDisable: function (elem, timeout = 3000) {
            elem.disabled = true;
            setTimeout(() => {
                elem.disabled = false;
            }, timeout);
        },

        init: function initMain() {
            window.onHcaptchaSubmit = this.onHcaptchaSubmit;
        },

    }

    return o;
})(app || {});
