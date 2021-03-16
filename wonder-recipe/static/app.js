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

const userListsTitleUnderline = document.querySelector('#userListsTitleUnderline');

const colors = ["#089F46", "#32B232", "#1CA83C", "#3AB630", "#4FB23", "#8CDC09", "#94E80D", "#A5FF13",
                "#A5FF13", "#94E80D", "#8CDC09", "#4FB23", "#3AB630", "#1CA83C", "#32B232", "#089F46"];

function changeColor(colors, i) {
    const userListsTitleUnderline = document.querySelector('#userListsTitleUnderline');
    setInterval(() => {
      let linearGradient = `linear-gradient(90deg, ${colors[i]} 0%, #089F46 50%, ${colors[i]} 100%)`;
      if(userListsTitleUnderline) userListsTitleUnderline.style.background = linearGradient;
      i++;
      i %= colors.length;
    }, 250);
  }
  changeColor(colors, 0);
