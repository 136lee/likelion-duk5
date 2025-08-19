// 카카오 지도 생성
(function () {
  const container = document.getElementById('map');
  if (!container || !window.kakao || !kakao.maps) {
    console.error('카카오 지도 스크립트가 로드되지 않았습니다.');
    return;
  }

  const map = new kakao.maps.Map(container, {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 5,
  });

  let marker = null;

  // 지도 클릭 → 마커 이동 + 폼 좌표 주입
  kakao.maps.event.addListener(map, 'click', function (mouseEvent) {
    const latlng = mouseEvent.latLng;
    const lat = latlng.getLat().toFixed(6);
    const lng = latlng.getLng().toFixed(6);

    if (!marker) {
      marker = new kakao.maps.Marker({ position: latlng });
      marker.setMap(map);
    } else {
      marker.setPosition(latlng);
    }

    document.getElementById('lat').value = lat;
    document.getElementById('lng').value = lng;
    document.getElementById('coord').textContent = `${lat}, ${lng}`;
  });
})();
