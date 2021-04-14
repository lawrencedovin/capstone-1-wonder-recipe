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

async function getCard() {
  try {
    const url = 'https://api.spoonacular.com/recipes/complexSearch';
    const apiKey = 'secret123';

    
    const response = await axios.get(url, {
      params: {
        apiKey: apiKey,
        cuisine: 'african',
        number: 5,
      },
    });

    console.log("getCard resp=", response);
    $("#card").html(response.data);
  } catch(e) {
    alert(`Error: ${e}`);
  }
}

$("#card-btn").on("click", getCard);


$('#clearButton').on("click", () => {
  $('#q').val('');
});

$(document).ready(function() {
  setTimeout(function() {
      $('.flash').fadeOut('slow');
  }, 2000); // <-- time in milliseconds
});