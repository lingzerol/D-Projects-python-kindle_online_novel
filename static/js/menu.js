function Menu() {
}
Menu.prototype.set_item_layout = function (doc) {
    return doc;
}

function ContentMenu() {
    Menu.call(this)
}

ContentMenu.prototype = new Menu();

ContentMenu.prototype.menu = {
    "目录": "menu.catalog()",
    "上一章": "menu.next_chapter()",
    "下一章": "menu.last_chapter()",
    "返回书架": "menu.back_to_shelf()"
};

ContentMenu.prototype.set_menu = function () {
    var target = document.getElementById("menu_container");

    for (var key in this.menu) {
        var doc = document.createElement("div");
        doc = this.set_item_layout(doc);
        doc.innerHTML = key;
        doc.setAttribute("onClick", this.menu[key])
        doc.setAttribute("style", "margin-top:5px;margin-bottom:5px;")
        target.appendChild(doc);
    }
}

ContentMenu.prototype.catalog = function () {
    document.getElementById("menu").style.visibility = "hidden";
}

ContentMenu.prototype.next_chapter = function () {
    document.getElementById("menu").style.visibility = "hidden";
}

ContentMenu.prototype.last_chapter = function () {
    document.getElementById("menu").style.visibility = "hidden";
}

ContentMenu.prototype.back_to_shelf = function () {
    document.getElementById("menu").style.visibility = "hidden";
}