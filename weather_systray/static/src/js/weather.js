/** @odoo-module **/
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
var ExampleWidget = Widget.extend({
   template: 'WeatherSystray',
   events: {
       'click #create_so': '_onClick',
   },

   _onClick: function(){
   console.log("123456789iuytredfgh")
   const successCallback = (position) => {
   var a = position.coords.latitude;
   var b = position.coords.longitude;
   var APIKey = "1e6592e3041a39d1a9d225b2f4a9463a";
   var city = "Kozhikode"
   const date = new Date();
//   var apikey = 8fd1afe73bd884bb0fb77f9f83a48324;
  console.log(a);
  console.log(b);
  console.log(APIKey);
  var queryURL = "http://api.openweathermap.org/data/2.5/weather?lat=" + a + "&lon=" + b + "&appid=" + APIKey;
//  var queryURL = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + APIKey;
  fetch(queryURL)
  console.log(queryURL)
  $.getJSON(queryURL, function( data ) {
//  console.log(city)
  console.log(b)
  var temp = Math.round(data.main.temp -273.15)
  var cloud = data.weather[0].main
  console.log(temp)
  console.log(cloud)
console.log(data)
swal({
  title: "Weather",
  text: date+ " \n temp=" +temp+ "°C " +cloud+ "\n Near:" +data.name+ "\n lat=" +data.coord.lat+ "\n lon=" +data.coord.lon,
  button: "OK",
});
})
console.log("2345rtyui",a);
};
navigator.geolocation.getCurrentPosition(successCallback);
},
});
SystrayMenu.Items.push(ExampleWidget);
export default ExampleWidget;