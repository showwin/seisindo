$(function(){
  $("input[data-validate-at-blur='true']").blur(function(){
    var content = $(this).val()
    if (content === "") {
      alert("入力が必須のフォームです");
    }
  });
});
