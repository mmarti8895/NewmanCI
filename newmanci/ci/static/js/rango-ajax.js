/**
 * Created by mmartin on 4/28/14.
 */
$(document).ready(function(){
    // jQuery stuff put here.
    // Likes AJAX
    $('#likes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
         $.get('/like_category/',
             {category_id: catid},
             function(data){
                $('#like_count').html(data);
                $('#likes').hide();
          });
    });
    // Suggestions AJAX
    $('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/suggest_category/', {suggestion: query}, function(data){
            $('#cats').html(data);
        });
    });
    // Page Add
    $('.rango-add').click(function(){
	    var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var me = $(this)
	    $.get('/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
            $('#pages').html(data);
	        me.hide();
	    });
	});
});