function initMap() {
  // 지도 생성
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.651, lng: 127.016 },
    zoom: 15
  });

  // 마커 생성
  const marker = new google.maps.Marker({
    position: { lat: 37.651, lng: 127.016 },
    map: map,
    title: "덕성여대"
  });

  // 마커 클릭 시 div 보이기
  marker.addListener("click", function() {
    document.getElementById("spot_information").style.display = "block";
    document.getElementById("close_infomation").style.display = "flex";
    document.getElementById("search_div").style.display = "none";
    document.getElementById("recommend").style.display = "none";

  });
}
  document.getElementById("feed_button_img").addEventListener("click", function() {
    window.location.href = "/DBTB/templates/feed/feed.html";
  });
  document.getElementById("move_to_feed").addEventListener("click", function() {
    window.location.href = "/DBTB/templates/feed/feed.html";
  });

  document.getElementById("My_activity").style.display = "none";
  
  document.getElementById("move_to_myact").addEventListener("click", function() {
    document.getElementById("My_activity").style.display = "block";
    document.getElementById("close_My_activity").style.display = "flex";
    document.getElementById("search_div").style.display = "none";
    document.getElementById("recommend").style.display = "none";


  });
  document.getElementById("goto_ex").addEventListener("click", function() {
    window.location.href = "/DBTB/templates/explore/explore.html";
  });
  document.getElementById("close_My_activity").addEventListener("click", function() {
    document.getElementById("My_activity").style.display = "none";
    document.getElementById("close_My_activity").style.display = "none";
    document.getElementById("search_div").style.display = "flex";
    document.getElementById("recommend").style.display = "block";
  });

  document.getElementById("close_infomation").addEventListener("click", function() {
    document.getElementById("spot_information").style.display = "none";
    document.getElementById("close_infomation").style.display = "none";
 document.getElementById("recommend").style.display = "block";
 document.getElementById("search_div").style.display = "flex";

  });
