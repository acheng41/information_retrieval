function displayResults() {
    document.getElementById("results").style.display = "block";
  }

function sortPriceDown() {
    document.getElementById("pricedownbtn").style.display = "none";
    document.getElementById("priceupbtn").style.display = "block";
    var value = 1;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/sort', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('value=' + value);
  }
function sortPriceUp() {
    document.getElementById("pricedownbtn").style.display = "block";
    document.getElementById("priceupbtn").style.display = "none";
    var value = 2;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/sort', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('value=' + value);
  }

function sortBedDown() {
    document.getElementById("beddownbtn").style.display = "none";
    document.getElementById("bedupbtn").style.display = "block";
    var value = 3;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/sort', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('value=' + value);
  }
function sortBedUp() {
    document.getElementById("beddownbtn").style.display = "block";
    document.getElementById("bedupbtn").style.display = "none";
    var value = 4;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/sort', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('value=' + value);
  }

  function sortBathDown() {
    document.getElementById("bathdownbtn").style.display = "none";
    document.getElementById("bathupbtn").style.display = "block";
    var value = 5;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/sort', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('value=' + value);
  }
function sortBathUp() {
    document.getElementById("bathdownbtn").style.display = "block";
    document.getElementById("bathupbtn").style.display = "none";
    var value = 6;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/sort', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('value=' + value);
  }
