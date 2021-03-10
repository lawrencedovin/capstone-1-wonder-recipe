const logo = 'Wonder Recipe';
for(let i = 0; i < logo.length; i++) {
    let newSpan = $("<span />")
                        .text(logo[i])
                        .css("color", i % 2 == 0 ? "#009B49" : "#8CDC09");
    $("#logo").append(newSpan);
}