// map
var map = L.mapbox.map('map', 'fcc.map-kzt95hy6,fcc.cni885mi,fcc.zrbgwrk9,fcc.j5v4e7b9,fcc.55bchaor,fcc.0iesif6r,fcc.pj3mobt9', {legendControl: false, attributionControl: false, gridControl: false, maxZoom: 12})
          .setView([38.82, -94.96], 4);
map.scrollWheelZoom.disable();
var hash = L.hash(map);      
//alert (map.getZoom());

// Display the map tooltip
map.gridLayer.on('click',function(o) {
  var data;
  if (o.data != undefined) {
    data = o.data;   
    // Populate location other stats (teaser fields from map)
    $('#stat-cnty').text(data.county_name);
    $('#stat-state').text(data.state);    
    $('#stat-tract').text(data.tract);
    $('#stat-totloc').text(data.total_locations);
    $('#stat-totsup').text(formatComma(data.total_annual_support));
    // Additional Cost Stats (teaser fields from map)   
    $('#stat-pclocbtwn').text(data.pc_locations_between);
    $('#stat-rorlocbtwn').text(data.ror_locations_between);
    $('#stat-pclocabv').text(data.pc_locations_above_ttc);
    $('#stat-rorlocabv').text(data.ror_locations_above_ttc);
    $('#stat-pcannsup').text(formatComma(data.pc_annual_support));
    $('#stat-rorannsup').text(formatComma(data.ror_annual_support));    
  } else { // Reset the text labels
    $('#stat-tract').text('---------');
    $('#stat-cnty').text('------');
    $('#stat-state, #stat-pcannsup, #stat-rorannsup').text('--');
    $('#stat-totloc, #stat-totsup').text('----');
    $('#dl-numLocs').find('span').text('-----');  
  }
});

// Format dummy data with commas
function formatComma(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

$(document).ready(function () {
  map.on('zoomend', function() {
    if (map.getZoom() >= 9) {
      $('#help-text').text("You can now click / touch tracts to display details.");
      $('#help-text').addClass('good');
    } else {
      $('#help-text').text("Zoom in to display tract level details on click / touch below.");
      $('#help-text').removeClass('good');
    }
  });
});