Waves.displayEffect();

$(".push-sidebar").click(function() {
        var e = $(".sidebar");
        e.hasClass("visible") ? (e.removeClass("visible"), $(".page-inner").removeClass("sidebar-visible")) : (e.addClass("visible"), $(".page-inner").addClass("sidebar-visible"))
    })