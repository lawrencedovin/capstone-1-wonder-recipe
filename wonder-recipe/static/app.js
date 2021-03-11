const logo = 'Wonder Recipe'.split(' ');
for(let i = 0; i < logo.length; i++) {
    let word = logo[i];
    for(let j = 0; j < word.length; j++) {
        let letter = word[j]
        let letterSpan = $("<span />")
        .text(letter)
        .css("color", j % 2 == 0 ? "#009B49" : "#8CDC09");
        $("#logo").append(letterSpan);
    }
    $("#logo").append('<span> </span>');
}