$(function() {
  $(".l-side__list .l-side__item").click(function () {
    if ($(this).find("dd").hasClass("is-open")) {
      $(".l-side__list .l-side__item").find("dd").removeClass("is-open");
    } else {
      $(".l-side__list .l-side__item").find("dd").removeClass("is-open");
      $(this).find("dd").addClass("is-open");
    }
  });
  /*  */
  $(".l-side__list .l-side__item").hover(
    function () {},
    function () {
      $(".l-side__list .l-side__item").find("dd").removeClass("is-open");
    }
  );
  /*  */
});