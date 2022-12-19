odoo.define('basic_snippet_blog.dynamic', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   var Dynamic = PublicWidget.Widget.extend({
       selector: '.dynamic_snippet_blog',
       start: function () {
           var self = this;
           rpc.query({
               route: '/eLearning',
               params: {},
           }).then(function (result) {
               self.$target.empty().append(result)
           });
       },
   });
   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});