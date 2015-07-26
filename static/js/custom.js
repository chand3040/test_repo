$(document).ready(function(){
    var file_element = $("#upload_csv_only");
    file_element.change(function(){
        file_val = $(this).val();
        file_val_arr = file_val.split('.');
        if (file_val_arr[file_val_arr.length-1]!='csv'){
            file_element.replaceWith( file_element = file_element.clone( true ) );
        }else{
            //Do nothing
        }
    });
    
    //Submit data from here when select fields are selected
    $('#select_tab_form').submit(function(event){
        reset_data();//Will reset the html and some vars
        event.preventDefault();
        $.ajax({
            'url'  : window.tabulation_data_url,
            'type' : 'POST',
            'data' : $('#select_tab_form').serialize(),
            'success': function(responseData){
                $('#response_tab_data').html(responseData.tab_data);
                $('#save_tab_data').show();
                window.tab_data_jsonresponse = responseData.json_data
            },
        })
    });
    
    
    
    $('#save_tab_data').click(function(event){
        if (typeof(window.tab_data_jsonresponse) !='undefined'){
            $.ajax({
                'url'  : window.savetabulation_data_url,
                'type' : 'POST',
                'data' : {'tab_json_data':window.tab_data_jsonresponse,'csrfmiddlewaretoken':window.csrf},
                'success': function(responseData){
                    var tab_data = $('#save_tab_data').val()
                    $('#save_tab_data').val('Selected data saved');
                    setTimeout(function(){ $('#save_tab_data').val(tab_data); }, 2000);
                },
            })
        }
    });
});


function reset_data(){
    $('#response_tab_data').html('');
    $('#save_tab_data').hide();
    window.tab_data_jsonresponse = undefined;
}