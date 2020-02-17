$(document).ready(function() {
    fetch_devices();
    var global_get_data =[];
    var content =""
    /* populate the device details got from backend */
    function populate_device_detail(db_data)
    {
        global_get_data = db_data;
        $('#username').text("Hi " + $.cookie('user') +" !!" );
        for(i =0;i<db_data.length;i++)
        {
            var entry = db_data[i]
            row_str =""
            var row_str = "<tr> <td> <input type=radio name = dev_id_radio id=" + entry.dev_id + ">" + entry.dev_id + "</td> \
             <td>" + entry.dev_name+"</td> \
             <td>" + entry.dev_console+"</td> \
             <td>" + entry.dev_mgmt+"</td> \
             <td>" + entry.dev_power+"</td> \
             <td>" + entry.dev_topo+"</td> \
             <td>" + entry.used_by+"</td> \
             </tr>"
            $("#display_details_tbody").append(row_str);

        }

    }

    $('#display_details').on('click', 'tbody tr', function (event) {
       content = $(this).text().split(' ');
       $(this).addClass('highlight').siblings().removeClass('highlight');
       $(this).find('input:radio').prop('checked', true);
       toggle_button();
    });
    /* Edit the device details */
    $('#edit_device').on('click', function(){
       var entry  = '';
        entry = get_entry();
        if(check_valid_oper(entry))
        {
          $('#dev_id_id').val(entry.dev_id)
          $('#dev_name_id').val(entry.dev_name);
          $('#dev_console_id').val(entry.dev_console)
          $('#dev_mgmt_id').val(entry.dev_mgmt)
          $('#dev_power_id').val(entry.dev_power)
          $('#dev_topo_id').val(entry.dev_topo)
         }

    });
    $('#add_device').on('click',function(){
        var entry ={};
        entry.dev_id = $('#dev_id_id').val();
        entry.dev_name=  $('#dev_name_id').val();
        entry.dev_console= $('#dev_console_id').val();
        entry.dev_mgmt= $('#dev_mgmt_id').val();
        entry.dev_power =  $('#dev_power_id').val();
        entry.dev_topo= $('#dev_topo_id').val();
        add_edit_device(entry);
    });
    function reset_fields()
    {
       $('#dev_id_id').val("0");
       $('#dev_name_id').val("");
       $('#dev_console_id').val("");
       $('#dev_mgmt_id').val("");
       $('#dev_power_id').val("");
       $('#dev_topo_id').val("");


    }
/* clear the device details form*/
    $('#reset').on('click', function(){
       reset_fields();
    });
/* operation to reserve the device */
$('#reserve_dev').on('click', function(){
       var entry  = '';
       entry = get_entry();
       if ($('#reserve_dev').hasClass('reserve'))
       {
         entry.used_by = $.cookie('user');
         console.log(entry);
         reserve_device(entry);
       }
       else if ($('#reserve_dev').hasClass('request'))
       { /* send a mail  */
            request_device(entry);
       }
       else
       {
         entry.used_by = null
         console.log(entry);
         reserve_device(entry);

       }
});

$('#logout').on('click',function(){
        action_logout();

});
/* get the entry/device that user want to perform action on.
Right now this is messy, see if we can get a better  way to do it */
    function get_entry()
    {
     var entry = ''
     for(i=0;i< global_get_data.length;i++)
       {
         if(content[2] == global_get_data[i].dev_id)
         {
            entry = global_get_data[i]
            break;
         }
       }
        return entry
    }

    function check_valid_oper(entry)
    {
       if (entry.used_by == null  || entry.used_by == ""  || entry.used_by == 'None' )
       {
        return true
       }

       alert("Cannot Edit/Delete when device is being used.")
       return false;
    }
/* Toggle the text on the button from reserve->request->release based on the user. */
    function toggle_button()
    {
        var entry = ''
        entry = get_entry();
        console.log(entry.used_by)
        if(entry.used_by == $.cookie('user'))
        {
            $('#reserve_dev').val('Release')
            $('#reserve_dev').removeClass("request");
            $('#reserve_dev').removeClass("reserve");
            $('#reserve_dev').addClass('release');

        }
        else if( entry.used_by == null || entry.used_by == ""  || entry.used_by == 'None' )
        {

         $('#reserve_dev').val('Reserve')
             $('#reserve_dev').removeClass("request");
             $('#reserve_dev').removeClass("release");
              $('#reserve_dev').addClass("reserve");

        }
        else
        {
            $('#reserve_dev').val('Request');
            $('#reserve_dev').removeClass("release");
            $('#reserve_dev').removeClass("reserve");
            $('#reserve_dev').addClass("request");

        }
    }
      /* Ajax call for the get info all devices.*/
    function fetch_devices()
    {
    $.ajax({
            url: '/device_detail/get_device',
            type: 'GET',
            success: function(response){
                console.log('response' + response);
                populate_device_detail(response)
            },
            error: function(error){
                console.log(error);
            }
        });
    }

  /* Ajax call for the deleting the device details.*/
    $('#del_device').on('click', function(){


        var entry = get_entry();

        if(check_valid_oper(entry) == false)
        {
            return false;
        }
        if(confirm("Are you sure you want to delete the Device Details?") == false)
        {
            alert("Bravo ;)")
            return false;
        }
        var str =
        {
         "dev_id" : content[2]
        }
        $.ajax({
            url: '/device_detail/get_device',
            contentType: 'application/json',
            type: 'DELETE',
            data: JSON.stringify(str),
            success: function(response){
              location.reload();
            },
            error: function(error){
                console.log(error);
            }
        });

      });

    /* Ajax call for the reserving the device.*/
    function reserve_device(entry)
    {
    $.ajax({
            url: '/device_detail/reserve_device',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(entry),
            success: function(response){
               console.log('response' + response);
               location.reload();
            },
            error: function(error){
                console.log(error);
            }
        });
    }

        /* Ajax call for the requesting the device.*/
    function request_device(entry)
    {
    $.ajax({
            url: '/device_detail/request_device',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(entry),
            success: function(response){
               console.log('response' + response);
               location.reload();
            },
            error: function(error){
                console.log(error);
            }
        });
    }

        /* Ajax call for the requesting the device.*/
    function add_edit_device(entry)
    {
         $.ajax({
            cache: false,
            url: '/device_detail/save_edit_device',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(entry),
            success: function(response){
               console.log('response' + response);
               location.reload();
               reset_fields();
               reset_fields();
            },
            error: function(error){
                console.log(error);
            }
            });

    }
    function get_device_detail_page()
    {
         $.ajax({
            url: '/device_detail',
            contentType: 'application/json',
            type: 'GET',
            success: function(response){
              location.reload();
            },
            error: function(error){
                console.log(error);
            }
        });
    }

    function action_logout()
    {
            $.ajax({
            url: '/logout',
            contentType: 'application/json',
            type: 'POST',
            success: function(response){
            location.reload();
            },
            error: function(error){
                console.log(error);
            }
        });
    }
})
