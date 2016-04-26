$(document).ready(function(){
    // Волны на кнопках
    Waves.displayEffect();

    // Сайдбар выдвижение/заезжание
$(".push-sidebar").click(function() {
        var e = $(".sidebar");
        e.hasClass("visible") ? (e.removeClass("visible"), $(".page-inner").removeClass("sidebar-visible")) : (e.addClass("visible"), $(".page-inner").addClass("sidebar-visible"))
    });

    // удаление
    window.obj_delete = function(obj_name, del_url){
    document.getElementById("object").innerHTML = obj_name ;
    document.delete_form.action = del_url;}
});

// Сортировка элементов
$(".sortable").sortable({
        connectWith: ".sortable",
        items: ".panel",
        helper: "original",
        revert: !0,
        placeholder: "panel-placeholder",
        forcePlaceholderSize: !0,
        opacity: .95,
        cursor: "move"
    });