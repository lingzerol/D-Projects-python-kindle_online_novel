function Content() { }
Content.prototype.layout = {
    "font_size": 20,
    "line_weight": 30,
    "font_weight": "normal",
    "color": "black",
    "font_style": "normal",
    "font_family": "STSong",
    "letter_spacing": 1
};
Content.prototype.line_text_num = 0;
Content.prototype.line_num = 0;
Content.prototype.text = new Array();
Content.prototype.page = 0;
Content.prototype.set_content_layout = function () {
    var doc = document.getElementById("content");
    doc.style.fontSize = this.layout["font_size"].toString() + "px";
    doc.style.lineHeight = this.layout["line_height"].toString() + "px";
    doc.style.fontWeight = this.layout["font_weght"];
    doc.style.color = this.layout["color"];
    doc.style.fontStyle = this.layout["font_style"];
    doc.style.fontFamily = this.layout["font_family"];
    doc.style.letterSpacing = this.layout["letter_spacing"].toString() + "px";
    get_text_length_bound();
}

Content.prototype.get_text_length_bound = function () {
    if (this.line_text_num == 0) {
        this.line_text_num = document.getElementById("content").offsetWidth / ((this.layout["font_size"] + this.layout["letter_spacing"]));
        this.line_text_num = Math.floor(this.line_text_num);
    }
    if (this.line_num == 0) {
        this.line_num = document.getElementById("content").offsetHeight / this.layout["line_weight"];
        this.line_num = Math.floor(this.line_num);
    }
}

Content.prototype.split_text = function (text) {
    result = new Array();
    this.get_text_length_bound()
    var text_num = 0;
    var prev_text_num = 0;
    var prev_i = 0;
    for (var i = 0; i < text.length; ++i) {
        if (text.charAt(i) == '\n') {
            text_num += this.line_text_num - text_num % this.line_text_num + 1;
        }
        else if (text.charAt(i) == '\t') {
            text_num += 4;
        }
        else {
            ++text_num;
        }
        if ((text_num - prev_text_num) >= this.line_text_num * this.line_num || text_num == text.length - 1) {
            var print_text = text.substring(prev_i, Math.min(text_num, i));
            result.push(print_text);
            prev_i = i;
            prev_text_num = text_num;
        }
    }
    return result;
}

Content.prototype.set_content = function (text) {
    this.text = this.split_text(text)
    this.page = 0;
    document.getElementById("content").innerHTML = this.text[0];
    document.getElementById("page_info").innerHTML = (this.page + 1).toString() + "/" + this.text.length.toString()
}

Content.prototype.next_page = function () {
    this.page = Math.min(this.page + 1, this.text.length - 1)
    document.getElementById("content").innerHTML = this.text[this.page];
    document.getElementById("page_info").innerHTML = (this.page + 1).toString() + "/" + this.text.length.toString()
}

Content.prototype.prev_page = function () {
    this.page = Math.max(this.page - 1, 0)
    document.getElementById("content").innerHTML = this.text[this.page];
    document.getElementById("page_info").innerHTML = (this.page + 1).toString() + "/" + this.text.length.toString()
}

var content = new Content();

var text = "\t    海外网3月28日电 据中国驻纽约\n\n\n\t总领馆官微消息，新冠\n\t肺炎疫情以来，美国一些城\t市连续发生针对亚裔\n的歧视和暴力犯罪\n事件，近期再次出现上升趋势。3月16日，亚特兰大市内及周边地区接连发生三起枪击事件，致死8人，其中6人是亚裔女性，包括1名华人、1名中国公民。3月20日，美国多地举行了主题为“停止仇恨亚裔”的游行和集会，以此抗议亚特兰大枪击案和针对亚裔的恶性事件。据了解，有关亚裔团体准备举行更多反仇恨亚裔的活动。多地发生的针对亚裔的仇恨事件加深了在美亚裔群体的忧惧，在美中国公民的安全受到威胁。此外，美国枪击案频发，3月22日，科罗拉多州博尔德一家超市发生枪击案10人死亡，其中包括一名警察。此类事件也使在美中国公民安全状况堪忧。中国驻美使馆特别提醒广大在美中国公民包括企业员工、留学人员、华侨等务必加强安全防范，警惕针对亚裔的歧视和暴力。遭遇此类情况务必保持冷静，妥善应对，尽量避免发生口角和肢体冲突，确保自身安全。如遇暴力行为和安全威胁，请立即拨打美国报警、求助电话：911（可要求中文服务），或请求他人协助报警，并及时向校方、雇佣方反映和寻求帮助，要求依法依规公正处理。必要时，可循法律途径维护自身合法权益。如涉及领事协助，可联系外交部全球领事保护与服务应急热线或相应使领馆领事保护与协助电话。外交部全球领事保护与服务应急热线（24小时）：+86-10-12308或+86-10-59913991海外网3月28日电 据中国驻纽约总领馆官微消息，新冠肺炎疫情以来，美国一些城市连续发生针对亚裔的歧视和暴力犯罪事件，近期再次出现上升趋势。3月16日，亚特兰大市内及周边地区接连发生三起枪击事件，致死8人，其中6人是亚裔女性，包括1名华人、1名中国公民。3月20日，美国多地举行了主题为“停止仇恨亚裔”的游行和集会，以此抗议亚特兰大枪击案和针对亚裔的恶性事件。据了解，有关亚裔团体准备举行更多反仇恨亚裔的活动。多地发生的针对亚裔的仇恨事件加深了在美亚裔群体的忧惧，在美中国公民的安全受到威胁。此外，美国枪击案频发，3月22日，科罗拉多州博尔德一家超市发生枪击案10人死亡，其中包括一名警察。此类事件也使在美中国公民安全状况堪忧。中国驻美使馆特别提醒广大在美中国公民包括企业员工、留学人员、华侨等务必加强安全防范，警惕针对亚裔的歧视和暴力。遭遇此类情况务必保持冷静，妥善应对，尽量避免发生口角和肢体冲突，确保自身安全。如遇暴力行为和安全威胁，请立即拨打美国报警、求助电话：911（可要求中文服务），或请求他人协助报警，并及时向校方、雇佣方反映和寻求帮助，要求依法依规公正处理。必要时，可循法律途径维护自身合法权益。如涉及领事协助，可联系外交部全球领事保护与服务应急热线或相应使领馆领事保护与协助电话。外交部全球领事保护与服务应急热线（24小时）：+86-10-12308或+86-10-59913991海外网3月28日电 据中国驻纽约总领馆官微消息，新冠肺炎疫情以来，美国一些城市连续发生针对亚裔的歧视和暴力犯罪事件，近期再次出现上升趋势。3月16日，亚特兰大市内及周边地区接连发生三起枪击事件，致死8人，其中6人是亚裔女性，包括1名华人、1名中国公民。3月20日，美国多地举行了主题为“停止仇恨亚裔”的游行和集会，以此抗议亚特兰大枪击案和针对亚裔的恶性事件。据了解，有关亚裔团体准备举行更多反仇恨亚裔的活动。多地发生的针对亚裔的仇恨事件加深了在美亚裔群体的忧惧，在美中国公民的安全受到威胁。此外，美国枪击案频发，3月22日，科罗拉多州博尔德一家超市发生枪击案10人死亡，其中包括一名警察。此类事件也使在美中国公民安全状况堪忧。中国驻美使馆特别提醒广大在美中国公民包括企业员工、留学人员、华侨等务必加强安全防范，警惕针对亚裔的歧视和暴力。遭遇此类情况务必保持冷静，妥善应对，尽量避免发生口角和肢体冲突，确保自身安全。如遇暴力行为和安全威胁，请立即拨打美国报警、求助电话：911（可要求中文服务），或请求他人协助报警，并及时向校方、雇佣方反映和寻求帮助，要求依法依规公正处理。必要时，可循法律途径维护自身合法权益。如涉及领事协助，可联系外交部全球领事保护与服务应急热线或相应使领馆领事保护与协助电话。外交部全球领事保护与服务应急热线（24小时）：+86-10-12308或+86-10-59913991";
content.set_content(text);